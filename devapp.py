# Import libraries
import streamlit as st
import pandas as pd
import os
import re
import json
import time
from algoliasearch.search_client import SearchClient
import requests
from functions import previewFunction

#---------------------------------
# Authnetikz Admin Panel
#---------------------------------
#
# Creator: Ryan Dinubilo
# Creation Date: 3/11/2021
# Current Version: 1.14
#
#
# Changelog ---------------------
# Revision Dates:
# Version 1.12 - 3/12/2021
# See changelog doc
#
#
# Version 1.13 - 3/13/2021
# See changelog doc
#
# Version 1.14 - 3/16/2021
#
# - Added "Upload Verification" system. Grabs 4 random records in the uploaded file and checks them against the Algolia API. Highlights the dataframe with a                                    #   green background if successful. TODO build a rejection mechanism in case the serials are not properly uploaded?
#
# - Added function 
#
# - Added comments
#
# Version 1.15 - 3/21/2021
# 
# - Added comments
#
# - Created previewFunction for displaying the un/highlighted dataframe - currently needs to take in the csv(df), csv_records(list), csv_records_count(int) 
#   to work. Also requires the "highlight" parameter to be "On" or "Off"
#
#

def main():

    image = st.sidebar.markdown("![Alt Text](https://i.imgur.com/dN0puJM.png)")     #Logo Image
    sidebar = st.sidebar.title("Authnetikz Admin Panel")                            #Title Text
    sidebarselect = st.sidebar.radio("Select a Tool", options=["Upload","View Inventory", "Analytics"])    #Page Select

    #Initialzie Algolia Python client
    #todo: Don't store plaintext app ID and API Key. How do we safely deploy these things to Heroku? Maybe dotenv? Not sure
    client = SearchClient.create(os.environ["APP_ID"], os.environ["API_KEY"])
    index = client.init_index('test_Authnetikz')

    database = client.list_indices()

    database_select = database["items"][0]
    database_entries = database_select["entries"]

    query = '' # Empty query will match all records

    res = index.browse_objects({'query': query})

    results = []
    serial_results = []

    for hit in res:
        results.append(hit)
    
    for i in range(len(results)):
        serial_results.append(results[i]["Serial"])


    df = pd.DataFrame(serial_results, columns=["Serial"])

    #Page Definitions
    #
    #Upload Inventory Page
    if sidebarselect == "Upload":

        #Page Title
        st.title("Upload Inventory")
        st.markdown("**Status:**API Live ✔️")
        st.markdown("**Sharing:** On")
        #st.write("Use the file picker below to select a CSV of serial numbers. You will be asked to confirm before the information is fully uploaded.")
        #File picker for the user to upload CSV, store the CSV as a dataframe 
        csv_file = st.file_uploader("Upload a CSV file",  type='.csv') #Type must be CSV

        #If a CSV file is uploaded, display a message and button confirming the upload.
        #try: 
        if csv_file:

            #Use pandas to read CSV file as dataframe for further manipulation
            csv = pd.read_csv(csv_file, header=None, names=["Serial"])

            #Get the records into a list
            csv_records = csv["Serial"].to_list()

            #Count the list
            csv_records_count = len(csv_records)

            #Wait
            time.sleep(0.2)

            #Validation for user - text
            st.write("Is this the file you would like to upload?")
            
            # Data Preview Section --------------------------------------
            #
            # Preview Conditions - checks for record counts under 40. Displays the proper number of records if under (most uploads will be in the thousands- well above this limit, but I kept in the off chance a small file is used)
            #
            previewFunction(csv, csv_records, csv_records_count, "Off")
            #
            # End Preview Section

                # Display number of records
            st.markdown(f"**Serials Counted:** {csv_records_count}")

            # Whitespace
            st.text("")
            st.text("")
            st.text("")

            #Two columns, for verification text and button
            b1, b2 = st.beta_columns(2)
            b1.markdown("**Confirm Upload: **") #Verification text
            button = b2.button("Yes, upload the file.") #Verification button

            # When button is pressed, upload CSV file records to Algolia API. Display verified records.
            if button:

                #Loop through
                for item in csv_records:
                    record = [
                        {"Serial": item}
                    ]

                    index.save_objects(record, {'autoGenerateObjectIDIfNotExist': True})

                # Verification ----------------------------------------------------
                # 
                # Display a progress bar for the user. See function for details
                progress_bar()
                time.sleep(0.5)
                st.title("Verifying Upload")
                time.sleep(0.3)
                st.write("Selecting random records...")
                time.sleep(0.5)

                # Display the CSV preview but with the randomly selected records highlighted - highlight On. See function for details
                previewFunction(csv, csv_records, csv_records_count, "On")

                st.header("Upload Verified ✔️")

       # except:
       #     st.write("This CSV file is not in the correct format. It should only contain one column of serial numbers. Please try again.")

    elif sidebarselect == "View Inventory":
        st.markdown(f"There are currently {database_entries} products in the database.")
        st.title("View Inventory")
        st.text("")
        st.markdown('''
        <iframe class="airtable-embed" src="https://airtable.com/embed/shrj9OB3IimD9PJAg?backgroundColor=green&viewControls=on" frameborder="0" onmousewheel="" width="100%" height="800" style="background: transparent; border: 1px solid #ccc;"></iframe>
        ''', unsafe_allow_html=True)

    elif sidebarselect == "Update Mode":
        st.title("Down for maintenance - check back in a few hours")

    elif sidebarselect == "Analytics":

        text = st.text_input("Enter search term")

        new_df = df[df['Serial'].str.contains(text)]

        if text in new_df:
            print("yay")
        else:
            print("nay")

        if text:
            st.write(new_df)
        else:
            st.write(df)

    
#The preview function for displaying the CSV data - checks for files containing records < 40 and adjusts display accordingly

#A function for defining an animated progress bar
def progress_bar():
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

def request_call():

    requestURL = f'https://XUSRPGATQR-dsn.algolia.net/1/indexes/test_Authnetikz?query=test&queryType=prefixNone'

    headers = {
    "X-Algolia-API-Key": ALGOLIA_API_KEY,
    "X-Algolia-Application-Id": ALGOLIA_APP_ID
    }

    response = requests.get(requestURL, headers=headers)

    responsjson = response.json()

    print(responsjson)

if __name__ == "__main__":
    main()
