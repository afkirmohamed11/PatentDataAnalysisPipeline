import streamlit as st
import streamlit.components.v1 as stc
from pymongo import MongoClient
from datetime import datetime


def get_data(search_term, source):
    # Connect to MongoDB
    client = MongoClient('mongodb',
                username='admin',
                password='admin',
                authMechanism='SCRAM-SHA-256')
    results = {}
    for provider in source:
        provider = provider.lower().replace(" ", "")       
        db = client[provider]
        collection = db['data'+provider]

        results[provider] = collection.find({'title': {'$regex': search_term, '$options': 'i'}})  # Case-insensitive search
    total_length = 0
    for value in results.values():
        value = value.rewind()
        value = list(value)
        # Parse the JSON string and calculate its length
        num_documents = len(value)
        total_length = total_length +num_documents
    return results , total_length


PATENT_HTML_TEMPLATE = """
<div style="width:100%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;
box-shadow:0 0 1px 5px #eee; background-color: #31333F;
border-left: 5px solid #6c6c6c;color:white;">
<h4 style="color: white;">Patent Title: {}</h4>
<h4 style="color: white;">Open to Public Inspection:  {}</h4>
<h6 style="color: white;">Inventors: {}</h6>
<h6 style="color: white;">Provider: {}</h6>
</div>
"""

def format_date(date_string):
    date_obj = datetime.strptime(date_string, '%Y%m%d')
    return date_obj.strftime('%Y/%m/%d')



def main():

    st.title("Patents Search")

    # Nav Search Form
    with st.form(key='searchform'):
        nav1, nav3 = st.columns([6,1])

        with nav1:
            search_term = st.text_input("Search Patent")
            
        with nav3:
            
            st.text("Search")
            submit_search = st.form_submit_button(label='Search')

        col1, col2, col3, col4, col5  = st.columns(5)
        selected_options = []
    
        with col1:
            option1 = st.checkbox('Google Patent')
        with col2:
            option2 = st.checkbox('EPO')
        with col3:
            option3 = st.checkbox('CIPO')
        with col4:
            option4 = st.checkbox('USPTO')
        with col5:
            option5 = st.checkbox('ESPACENET')

        if option1:
            selected_options.append('Google Patent')
        if option2:
            selected_options.append('EPO')
        if option3:
            selected_options.append('CIPO')
        if option4:
            selected_options.append('USPTO')
        if option5:
            selected_options.append('ESPACENET')

        
        
    if submit_search:
        st.success("You searched for {} in {}".format(search_term, ', '.join(selected_options)))
        search_results , num_of_results = get_data(search_term,selected_options)
        #search_results.rewind()
        #Number of Results
        st.subheader("Showing {} Patents".format(num_of_results))

        for key, value in search_results.items():
            data = value.rewind()
            for document in data:
                # Access id, title, and other fields
                provider = key
                patent_id = document.get('id')
                title = document.get('title')
                code = document.get('code')
                publication_date = document.get('publication_date')
                application_date = document.get('application_date')
                link = document.get('link')
                applicants = document.get('applicants')
                inventors = document.get('inventors')
                abstract = document.get('abstract')

                st.markdown(PATENT_HTML_TEMPLATE.format(title, publication_date, inventors, provider), unsafe_allow_html=True)

                with st.expander("Abstract"):
                    stc.html(abstract, scrolling=True)

                st.link_button("Go to Patent", link)
                
        
            

if __name__ == '__main__':
    main()