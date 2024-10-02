# # Les bibliothèques nécessaires
import random
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

URLs = []
Titles = []
IDs = []
Inventors = []
Publication_Dates = []
Current_Assignees = []
Original_Assignees = []
Abstracts = []
Descriptions = []
Claims = []
Patent_Offices = []
Filing_Dates = []
Priority_Dates = []
Applications_Number = []
Primary_Languages = []
Publications_Number = []
Countries_name = []
PDFs_URL = []


urls = pd.read_csv("gp-search.csv")
h={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
for url in urls["URL"][:100]:
    try:
        page = requests.get(url, headers=h)
        page.raise_for_status()  # Raise an exception for unsuccessful requests
        src = page.content

        soup = BeautifulSoup(src, 'html.parser')
        URLs.append(url)         

        title = "Null"
        title_tag = soup.find('meta', attrs={'name': 'DC.title'})
        if title_tag:
            title = title_tag.get('content')
        if title:
            title = title.strip()  
        Titles.append(title)

       
         
        publicationDate = "Null"
        publicationDate=soup.find("td", {"itemprop" :"publicationDate"})
        if publicationDate:
            publicationDate = publicationDate.text.strip()
        Publication_Dates.append(publicationDate)

        id = "Null"
        id = soup.find("span", {"itemprop": "publicationNumber"})

        if id:
            id = id.text.strip()
            if id not in IDs:
                IDs.append(id)
            else:
                del Publication_Dates[-1]
                del Titles[-1]
                del URLs[-1]
                continue
     
         
        
        current_assignee = "Null"
        current_assignee_tag = soup.find('meta', attrs={'name': 'DC.contributor', 'scheme': 'assignee'})
        if current_assignee_tag:
            current_assignee = current_assignee_tag.get('content')
        if current_assignee:
            current_assignee = current_assignee.strip()  
        Current_Assignees.append(current_assignee)


    

        original_assignee = "Null"
        original_assignee_tag =  soup.find('span', itemprop='assigneeOriginal')
        if original_assignee_tag:
            original_assignee = original_assignee_tag.text.strip()
        Original_Assignees.append(original_assignee)



        abstract = "Null"
        abstract = soup.find('section', {'itemprop': 'abstract'})

        if abstract:
            abstract_text = abstract.text.strip()
            if abstract_text.startswith("Abstract\n"):
                abstract_text = abstract_text[9:] 
            abstract_text = '\n'.join(line.strip() for line in abstract_text.splitlines() if line.strip())

            Abstracts.append(abstract_text)


        description_text= "Null"
        description = soup.find('section', {'itemprop': 'description'})

        if description:
            description_text = description.text.strip()
            description_text = description_text.replace('\n', '')
            description_text = ' '.join(description_text.split())  
            if description_text.startswith("Description"):
                description_text = description_text[11:]
            Descriptions.append(description_text)

        


        claims = "Null"
        claims_section = soup.find('section', {'itemprop': 'claims'})

        if claims_section:
            claims = claims_section.text.strip()
            claims = claims.replace('\n', '')  
            Claims.append(claims)

  


        all_inventors = soup.find_all('meta', attrs={'name': 'DC.contributor', 'scheme': 'inventor'})
        inventors = ""
        for inventor in all_inventors:
            inventor = inventor.get('content')
            if inventor:
               inventors = inventors + " " +inventor 
        Inventors.append(inventors)
    

         
        patent_office = "Null"
        patent_office=soup.find('dd',{'itemprop':'countryName'})
        if patent_office:
            patent_office = patent_office.text.strip()
        Patent_Offices.append(patent_office)
         


        filing_date= priority_date = "Null"
        filing_date = soup.find('td', itemprop='filingDate')
        if filing_date :
            filing_date = filing_date.text.strip()
    
        priority_date = soup.find('td', itemprop='priorityDate')
        if priority_date :
            priority_date = priority_date.text.strip()

        Filing_Dates.append(filing_date)
        Priority_Dates.append(priority_date)
  
         

        application_num = "Null"
        application_num = soup.find("span", itemprop = "applicationNumber")
        if application_num :
            application_num = application_num.text.strip()
        Applications_Number.append(application_num)
 

         
        primary_lan = "Null"
        primary_lan = soup.find("span", itemprop='primaryLanguage')
        if primary_lan:
            primary_lan = primary_lan.text.strip()
        Primary_Languages.append(primary_lan)
       


        publication_Number = "Null"
        publication_Number = soup.find("span", itemprop='publicationNumber')
        if publication_Number:
            publication_Number= publication_Number.text.strip()
        Publications_Number.append(publication_Number)
       

          
        country_name = "Null"
        country_name = soup.find("dd", itemprop='countryName')
        if country_name:
            country_name = country_name.text.strip()
        Countries_name.append(country_name)
 
          

        citation_pdf_url = "Null"
        citation_pdf_tag = soup.find('meta', attrs={'name': 'citation_pdf_url'})
        if citation_pdf_tag:
            citation_pdf_url = citation_pdf_tag.get('content')
        if citation_pdf_url:
            citation_pdf_url = citation_pdf_url.strip()
        PDFs_URL.append(citation_pdf_url)

        # sleep for 1min after each 1000 patent scrapped
        if len(URLs) % 1000 == 0:
            n= random.randint(10, 50)
            time.sleep(n)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
      

df = df = pd.DataFrame({

    'ID' : IDs,
    'Title': Titles,
    'Inventors': Inventors,
    'Publication Date': Publication_Dates,
    'Current Assignees': Current_Assignees,
    'Original Assignees': Original_Assignees,
    'Patent Office': Patent_Offices,
    'Filing Date': Filing_Dates,
    'Priority Date ': Priority_Dates,
    'Applications Number': Applications_Number,
    'Primary Language': Primary_Languages,
    'Publications Number': Publications_Number,
    'Country name': Countries_name,
    'Abstract': Abstracts,
    'Description': Descriptions,
    'Claims': Claims,
    'Patent URL': URLs,
    'PDF URL': PDFs_URL,
    
})

json_data = df.to_json(orient='records')

# Write JSON data to a file
with open('patent_data.json', 'w') as outfile:
    outfile.write(json_data)


