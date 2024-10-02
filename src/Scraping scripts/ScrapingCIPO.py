from bs4 import BeautifulSoup
import requests
import json
import re

with open("CIPOPATENTSLINKS.txt", "r") as file:
    links = file.readlines()


scrappedData = {}

counter = 0
for link in links:
    print(link.strip())
    url = link.strip()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')


    summaryTable = soup.find('table', id='patentSummaryTable')
    detailsTable = soup.find('table', id='patentDetailsTable')
    pctTable = soup.find('table', id='pctTable')
    appPriorityTable = soup.find('table', id='appPriorityTable')
    claims_summary = soup.find(id="tabs1_3").find_next('div', class_='tgl-panel')
    description_summary = soup.find(id="tabs1_3b").find_next('div', class_='tgl-panel')
    img_tag  = soup.find('details', id='tabs1_4').find('img')
    administrativeStatusTable = soup.find('table', id='administrativeStatusTable')
    currentOwnersTable = soup.find('table', id='currentOwnersTable')
    documentsTable = soup.find('table', id='documentsTable')

    summary_data = {}
    details_data = {}
    pct_data = {}
    headersPriorityTable =[]
    dataPriorityTable =[]
    priority_data = {}
    abstracts = {}
    claims = {}
    description = {}
    representative_drawing = {}
    administrativeStatus= {}
    currentOwners = {}
    documents = {}

    rows = summaryTable.find_all('tr')
    for row in rows:
        # Extract key and value from each row
        key = row.find('th').text.strip()
        key = re.sub(r'\(\d+\)', '', key)  # Remove (any number) using regular expression
        value = row.find('td').text.strip()
        if key == " French Title:" or key == "Status:":
            continue
        summary_data[key] = value

    rows = detailsTable.find_all('tr')
    for row in rows:
        # Extract key and value from each row
        key = row.find('th').text.strip()
        key = re.sub(r'\(\d+\)', '', key)
        value_tags = row.find('td').find_all('li') if row.find('td') else None
        
        if value_tags:  # If there are multiple values in a list
            values = [tag.get_text(strip=True) for tag in value_tags]
            if len(values) == 1:
                values = values[0]  # If only one value exists, just store it as a string
        else:
            value = row.find('td').get_text(strip=True)
            values = value
        if key == " International Patent Classification (IPC):":
            continue

        details_data[key] = values

    rows = pctTable.find_all('tr')
    for row in rows:
    # Extract key and value from each row
        key = row.find('th').text.strip()
        key = re.sub(r'\(\d+\)', '', key)
        value_tags = row.find('td').find_all('li') if row.find('td') else None
        
        if value_tags:  # If there are multiple values in a list
            values = [tag.get_text(strip=True) for tag in value_tags]
            if len(values) == 1:
                values = values[0]  # If only one value exists, just store it as a string
        else:
            value = row.find('td').get_text(strip=True)
            values = value
        if key=="Patent Cooperation Treaty (PCT):" or key==" PCT Filing Number:":
            continue
        pct_data[key] = values

    if appPriorityTable:
        headers_table = appPriorityTable.find_all('th')
        data_table = appPriorityTable.find_all('td')

        for header in headers_table:
            headersPriorityTable.append(header.get_text(strip=True))
        for data in data_table:
            dataPriorityTable.append(data.get_text(strip=True))

        priority_data = dict(zip(headersPriorityTable, dataPriorityTable))
    else:
        priority_data['Application No.'] = "not found"
        priority_data['Country/Territory'] = "not found"
        priority_data['Date'] = "not found"

    abstract = soup.find(id="tabs1_2")
    h2_tags = abstract.find_all('h2')

    for h2_tag in h2_tags:
    # Extract the text after the <h2> tag
        abstract_text = h2_tag.find_next_sibling()
        if abstract_text.name == 'p':
            abstract_text = abstract_text.get_text(strip=True)
    # Use the text of the <h2> tag as the key in the dictionary
        abstract_key = h2_tag.get_text(strip=True)
        # Store the key-value pair in the dictionary
        if (abstract_key =="French Abstract"):
            next_div = h2_tag.find_next_sibling('div')
            if next_div:
                abstract_text = next_div.find('p').get_text()
            else:
                abstract_text = None
        if abstract_key == "French Abstract":
            continue
        abstracts[abstract_key] = abstract_text

    if claims_summary:
        # Extract text and remove any <br> tags
        claims_summary = claims_summary.get_text(separator='\n', strip=True)
        # Print the extracted claims text
    else:
        claims_summary = "not found"
        print("No claims text found.")
    claims_summary = claims_summary.replace('\n', ' ')
    claims['claims'] = claims_summary

    if description_summary:
    # Replace <br> tags with newline characters
        for br in description_summary.find_all("br"):
            br.replace_with("\n")
        
        # Extract text and remove any remaining HTML tags
        description_summary = description_summary.get_text(separator='\n', strip=True)
    else:
        description_summary = "not found"
        print("No description text found.")

    # Remove extra whitespace and add the description to the 'description' dictionary
    description_summary = description_summary.replace('\n', ' ')
    description['description'] = description_summary

    if img_tag:
        # Extract text and remove any <br> tags
        img_src = img_tag['src']
        # Print the extracted claims text
    else:
        img_src = "not found"
        print("No claims text found.")

    representative_drawing['representativeDrawing'] = "https://brevets-patents.ic.gc.ca"+img_src


    administrativeStatusTable = administrativeStatusTable.find('tbody')
    administrativeStatusTable = administrativeStatusTable.find_all('tr')
    for tr in administrativeStatusTable:
        # Extract text from the first <td> as key
        key = tr.find('td').get_text(strip=True)
        # Extract text from the second <td> as value
        key = re.sub(r'\(\d+\)', '', key)  # Remove (any number) using regular expression
        value = tr.find_all('td')[1].get_text(strip=True)
        # Store key-value pair in the dictionary
        administrativeStatus[key] = value

    currentOwnersTable = currentOwnersTable.find('tbody')
    currentOwnersTable = currentOwnersTable.find('td')
    currentOwner = currentOwnersTable.get_text(strip=True)
    currentOwners['currentOwners']=currentOwner

    documentsTable = documentsTable.find('tbody')
    documentsTable = documentsTable.find_all('td')
    for tdata in documentsTable:
        if tdata.find('a') != None:
            key = tdata.find('a').get_text(strip=True)
            value = "https://brevets-patents.ic.gc.ca"+tdata.find('a')['href']
            documents[key] = value

    combined_data = {}
    combined_data.update(summary_data)
    combined_data.update(details_data)
    combined_data.update(pct_data)
    combined_data.update(priority_data)
    combined_data.update(abstracts)
    combined_data.update(claims)
    #combined_data.update(description)
    #combined_data.update(representative_drawing)
    #combined_data.update(administrativeStatus)
    combined_data.update(currentOwners)
    #combined_data.update(documents)


    result_dict = {link.strip(): combined_data}

    scrappedData.update(result_dict)

    counter += 1

    if counter == 100:
        break
with open('combined_data.json', 'w') as json_file:
        json.dump(scrappedData, json_file, indent=4)
print(counter)
