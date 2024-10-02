import json
import sys
import time
import random
import requests
comp=0

class Patent:
    def __init__(self,title,code,publication_date,application_date,applicants,inventors,abstract) -> None:
        self.title=title
        self.code=code  
        self.publication_date=publication_date
        self.application_date=application_date
        self.url=f"https://worldwide.espacenet.com/patent/search?q=pn%3D{self.code}"
        self.applicants=applicants
        self.inventors=inventors
        self.abstract =abstract

    def patent_to_dict(self):
        return{"title":self.title,
               "code":self.code,
               "publication date":self.publication_date,
               "application date":self.application_date,
               "link":self.url,
               "applicants":self.applicants,
               "inventors":self.inventors,
               "abstract":self.abstract}



class APIData:
    patents=[]
    def __init__(self,json) -> None:
        self.data=json
        
    
    def patent_to_json(self):
        patents_list=[]
        for p in APIData.patents:
            patents_list.append(p.patent_to_dict())
        with open("data3.json","w")as f:
            json.dump(patents_list,f,indent=4)


    def get_all_patents(self):
        global comp
        comp=+1
        # Extract relevant information from exchange-documents
        exchange_documents = self.data['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']

        for doc in exchange_documents:
            exchange_doc = doc['exchange-document']
            # titles = exchange_doc['bibliographic-data']['invention-title'][0]['$']
            titles = exchange_doc['bibliographic-data']['invention-title']
            if isinstance(titles,list):
                title=None
                for i in titles :
                    if i["@lang"]=="en":
                        title=i["$"]
                if title==None:
                    title=titles["$"]
            else:
                title=titles["$"]

            try:
                abstracts = exchange_doc['abstract']
                if isinstance(abstracts,list):
                    abstract=None
                    for j in abstracts :
                        if j["@lang"]=="en":
                            abstract=j["p"]["$"]
                    if abstract==None:
                        abstract=abstracts["p"]["$"]
                else:
                    abstract=abstracts["p"]["$"]
            except:
                abstract =None
                print("No abstract")            
            
            applicants = []
            applicant = exchange_doc['bibliographic-data']['parties'].get('applicants')

            if applicant is not None:
                applicant = exchange_doc['bibliographic-data']['parties'].get('applicants')['applicant']
                try:
                    applicant_data_format=applicant[0]["@data-format"]
                except KeyError:
                        inventor_data_format=applicant["@data-format"]
                        applicant =[applicant]

                for appli in applicant:
                    if appli.get('@data-format') == applicant_data_format:
                        name = appli['applicant-name']['name']['$'].replace("\u2002"," ")
                        applicants.append(name)
                    else :
                        break
                    
                inventors = []
                if exchange_doc['bibliographic-data']['parties'].get('inventors') is not None:
                    inventor = exchange_doc['bibliographic-data']['parties']['inventors']['inventor']
                    try:
                        inventor_data_format=inventor[0]["@data-format"]
                    except KeyError:
                        inventor_data_format=inventor["@data-format"]
                        inventor =[inventor]

                    for invent in inventor:
                        if invent.get('@data-format') == inventor_data_format:
                            name = invent['inventor-name']['name']['$'].replace("\u2002"," ")
                            inventors.append(name)
                        else :
                            break

            
            country = exchange_doc['@country']
            code = exchange_doc['@doc-number']
            kind = exchange_doc['@kind']
            publication_date = exchange_doc['bibliographic-data']['publication-reference']['document-id'][0]['date']['$']
            application_date = exchange_doc['bibliographic-data']['application-reference']['document-id'][1]['date']['$']
            
            
            print("Title:", title)
            print("Country:", country)
            print("Code:", code)
            print("Kind:", kind)
            print("Publication Date:", publication_date)
            print("Application Date:", application_date)
            print("Applicants:", applicants)
            print("Inventors:", inventors)
            print("abstract: ",abstract)

            print()
            APIData.patents.append(Patent(title,f"{country}{code}{kind}",publication_date,application_date,applicants,inventors,abstract))

    
    
class Oauth :
    def __init__(self) -> None:
         self.token=None
        
    def get_token(self) -> str:
        if self.token==None:
            self.set_new_token()
        return self.token

    def set_new_token(self):

        auth_server_url = "https://ops.epo.org/3.2/auth/accesstoken"
        client_id = 'RaGABiAEg34DUGHXc3e1r6TzbYaANCcQ'
        client_secret = 'rX49O0qq3BMrmXll'

        token_req_payload = {'grant_type': 'client_credentials'}

        token_response = requests.post(auth_server_url,
        data=token_req_payload, verify=False, allow_redirects=False,
        auth=(client_id, client_secret))
                    
        if token_response.status_code !=200:
            print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
            sys.exit(1)

        print("Successfuly obtained a new token")
        tokens = json.loads(token_response.text)
        self.token=tokens['access_token']



def get_response(oauth,url):
    token = oauth.get_token()

    api_call_headers = {'Authorization': 'Bearer ' + token,'Accept': 'application/json'}
    api_call_response = requests.get(url, headers=api_call_headers, verify=False)
    print(api_call_response.status_code)
    response=None
    if	api_call_response.status_code == 401:
        # oauth.set_new_token() I thik that it's a repetition
        token = oauth.get_token()
        time.sleep(2)
        response=get_response(oauth,url)
        return response
    
    print(api_call_response.text)
    return api_call_response.json()
    
oauth=Oauth()

start,end =1,100
while True:
   
    
    response=get_response(oauth,f"http://ops.epo.org/3.2/rest-services/published-data/search/biblio.json?q=(IA%20OR%20AI%20OR%20(%22Deep%20Learning%22)%20OR%20(%22artificial%20intelligence%22)%20OR%20NLP)%20AND%20(Agriculture%20OR%20Farming)&Range={str(start)}-{str(end)}")
    with open("output.json","w") as f :
        json.dump(response,f,indent=4)




        
    data=APIData(response)
    data.get_all_patents()

    if end==473:
        data.patent_to_json()
        break

    start=start +100

    if end==400:
        end=end+73
        print(end)
        continue
    
    end=end+100

    print(end)


    sleep_time = random.randint(3, 10)
    time.sleep(sleep_time)



data.patent_to_json()