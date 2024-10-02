

""
 # @author: Oussama BENABBOU
 #
 #
 # NB : Go to the line 182 and add your secret code as well as your client_id in order to use this script
 # output_{i}.json : refers to the whole output 
 # data_{i}.json : refers to the data which we're interested

""


import json
import sys
import time

import requests


class Patent:
    def __init__(
        self,
        title,
        code,
        publication_date,
        application_date,
        applicants,
        inventors,
        abstract=None,
    ) -> None:
        self.title = title
        self.code = code
        self.publication_date = publication_date
        self.application_date = application_date
        self.url = f"https://worldwide.espacenet.com/patent/search?q=pn%3D{self.code}"
        self.applicants = applicants
        self.inventors = inventors
        self.abstract = (
            abstract  # Added abstract as an attribute with a default value of None
        )

    def patent_to_dict(self):
        return {
            "title": self.title,
            "code": self.code,
            "publication_date": self.publication_date,  # Changed key name to match convention
            "application_date": self.application_date,  # Changed key name to match convention
            "link": self.url,
            "applicants": self.applicants,
            "inventors": self.inventors,
            "abstract": self.abstract,  # Added abstract to the dictionary representation
        }


class APIData:
    def __init__(self, json_data) -> None:
        self.data = json_data
        self.patents = []

    def patent_to_json(self):
        patents_list = []
        for p in self.patents:
            patents_list.append(p.patent_to_dict())
        with open("data_7.json", "w") as f:
            json.dump(patents_list, f, indent=4)

    def get_all_patents(self):
        exchange_documents = self.data["ops:world-patent-data"]["ops:biblio-search"][
            "ops:search-result"
        ]["exchange-documents"]

        for doc in exchange_documents:
            exchange_doc = doc["exchange-document"]
            titles = exchange_doc["bibliographic-data"]["invention-title"]
            if isinstance(titles, list):
                title = None
                for i in titles:
                    if i["@lang"] == "en":
                        title = i["$"]
                if title is None:
                    title = titles[0][
                        "$"
                    ]  # Take the first title if no English title is found
            else:
                title = titles["$"]

            applicants = []
            applicant = exchange_doc["bibliographic-data"]["parties"]["applicants"][
                "applicant"
            ]
            applicant_data_format = applicant[0]["@data-format"]

            for appli in applicant:
                if appli.get("@data-format") == applicant_data_format:
                    name = appli["applicant-name"]["name"]["$"].replace("\u2002", " ")
                    applicants.append(name)
                else:
                    break

            inventors = []
            if exchange_doc["bibliographic-data"]["parties"].get("inventors"):
                inventor = exchange_doc["bibliographic-data"]["parties"]["inventors"][
                    "inventor"
                ]
                if (
                    isinstance(inventor, list) and inventor
                ):  # Check if inventor is a non-empty list
                    inventor_data_format = inventor[0].get("@data-format")
                    for invent in inventor:
                        if invent.get("@data-format") == inventor_data_format:
                            name = invent["inventor-name"]["name"]["$"].replace(
                                "\u2002", " "
                            )
                            inventors.append(name)
                        else:
                            break
            else:
                inventor_data_format = (
                    None  # Handle the case when there are no inventors
                )

            # Retrieving abstract
            abstracts = exchange_doc.get("abstract", [])
            english_abstract = None

            # Check if abstracts is a list of dictionaries or just a string
            if isinstance(abstracts, list):
                for abstract in abstracts:
                    if isinstance(abstract, dict) and abstract.get("@lang") == "en":
                        english_abstract = abstract.get("p", {}).get("$")
                        break
            else:
                # If abstracts is a string, assume it's the English abstract
                english_abstract = abstracts

            # Creating Patent object
            country = exchange_doc["@country"]
            code = exchange_doc["@doc-number"]
            kind = exchange_doc["@kind"]
            publication_date = exchange_doc["bibliographic-data"][
                "publication-reference"
            ]["document-id"][0]["date"]["$"]
            application_date = exchange_doc["bibliographic-data"][
                "application-reference"
            ]["document-id"][1]["date"]["$"]

            print("Title:", title)
            print("Country:", country)
            print("Code:", code)
            print("Kind:", kind)
            print("Publication Date:", publication_date)
            print("Application Date:", application_date)
            print("Applicants:", applicants)
            print("Inventors:", inventors)
            print("Abstract:", english_abstract)  # Printing the retrieved abstract

            print()
            self.patents.append(
                Patent(
                    title,
                    f"{country}{code}{kind}",
                    publication_date,
                    application_date,
                    applicants,
                    inventors,
                    english_abstract,  # Passing abstract to Patent constructor
                )
            )


class Oauth:
    def __init__(self) -> None:
        self.token = None

    def get_token(self) -> str:
        if self.token == None:
            self.set_new_token()
        return self.token

    def set_new_token(self):

        auth_server_url = "https://ops.epo.org/3.2/auth/accesstoken"
        client_id = "" # Add your client ID here
        client_secret = ""  # Add your client secret here

        token_req_payload = {"grant_type": "client_credentials"}

        token_response = requests.post(
            auth_server_url,
            data=token_req_payload,
            verify=False,
            allow_redirects=False,
            auth=(client_id, client_secret),
        )

        if token_response.status_code != 200:
            print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
            sys.exit(1)

        print("Successfuly obtained a new token")
        tokens = json.loads(token_response.text)
        self.token = tokens["access_token"]


def get_response(oauth, url):
    token = oauth.get_token()

    api_call_headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
    }
    api_call_response = requests.get(url, headers=api_call_headers, verify=False)
    print(api_call_response.status_code)
    response = None
    if api_call_response.status_code == 401:
        oauth.set_new_token()
        token = oauth.get_token()
        time.sleep(2)
        response = get_response(oauth, url)
        return response

    print(api_call_response.text)
    return api_call_response.json()


oauth = Oauth()
response = get_response(
    oauth,
    "http://ops.epo.org/3.2/rest-services/published-data/search/biblio.json?q=%22Remote%20sensing%22",
)
with open("output_7.json", "w") as f:
    json.dump(response, f, indent=4)

data = APIData(response)
data.get_all_patents()
data.patent_to_json()
