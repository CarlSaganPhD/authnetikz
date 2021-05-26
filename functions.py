import streamlit as st
from random import randrange
from random import randint
import time

#The preview function for displaying the uploaded CSV file. Highlight "On" will select 4 random records and color them green, "Off" will just display data.
def previewFunction(csv, csv_records, csv_records_count, highlight):

    # Define multiple columns 
    csv_col1, csv_col2, csv_col3, csv_col4 = st.beta_columns(4) # Unlightlighted dataframe
    pagenum1, pagenum2, pagenum3, pagenum4 = st.beta_columns(4) # Page Number text
    preview_col_1, preview_col_2, preview_col_3, preview_col_4 = st.beta_columns(4) # Highlighted dataframe

    # Define the dataframes for the preview. See the paginate function at the bottom. Optimal size right now is 10 rows with 4 columns.
    csv_page1 = paginate_dataframe(csv, 10, 1)
    csv_page2 = paginate_dataframe(csv, 10, 2)
    csv_page3 = paginate_dataframe(csv, 10, 3)
    csv_page4 = paginate_dataframe(csv, 10, 4)

    # For no highlight, define the four cases where the filesize is less than 40 records. Write out the page number and display the single column dataframe for each.
    if highlight == "Off":
        if 1 <= csv_records_count <= 10: #Case 1, 0-9 records
            csv_col1.write(csv_page1) # Show dataframe
            pagenum1.write("Page 1") # Page Number

        elif 10 < csv_records_count <= 20: #Case 2: 10-19 records
            csv_col1.write(csv_page1) # Dataframes
            csv_col2.write(csv_page2)
            pagenum1.write("Page 1") #Page Numbers
            pagenum2.write("Page 2")

        elif 20 < csv_records_count <= 30: #Case 3: 20-29 records
            csv_col1.write(csv_page1) # Dataframes
            csv_col2.write(csv_page2)
            csv_col3.write(csv_page3)
            pagenum1.write("Page 1") #Page Numbers
            pagenum2.write("Page 2")
            pagenum3.write("Page 3")

        elif csv_records_count > 30:
            csv_col1.write(csv_page1) #Dataframes
            csv_col2.write(csv_page2)
            csv_col3.write(csv_page3)
            csv_col4.write(csv_page4) 
            pagenum1.write("Page 1") #Page Numbers
            pagenum2.write("Page 2")
            pagenum3.write("Page 3")
            pagenum4.write("Page 4")

    elif highlight == "On":

        if 1 <= csv_records_count <= 10:          
            rand_ten = randrange(csv_records_count)
            random_record_page1 = csv_records[rand_ten]
            st.markdown(f'**Records Selected:** {random_record_page1}')
            preview_1_HL = csv_page1.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page1 else ['background-color: default'], axis=1)

            preview_col_1.dataframe(preview_1_HL)

        elif 10 < csv_records_count <= 20:

            rand_ten = randrange(10)
            rand_twenty = randrange(csv_records_count)

            random_record_page1 = csv_records[rand_ten]
            random_record_page2 = csv_records[rand_twenty]

            st.markdown(f'**Records Selected:** {random_record_page1} , {random_record_page2}')

            preview_1_HL = csv_page1.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page1 else ['background-color: default'], axis=1)

            preview_2_HL = csv_page2.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page2 else ['background-color: default'], axis=1)

            preview_col_1.dataframe(preview_1_HL)
            preview_col_2.dataframe(preview_2_HL)

        elif 20 < csv_records_count <= 30:

            rand_ten = randrange(10)
            rand_twenty = randint(10,19)
            rand_thirty = randrange(csv_records_count)

            random_record_page1 = csv_records[rand_ten]
            random_record_page2 = csv_records[rand_twenty]
            random_record_page3 = csv_records[rand_thirty]
            st.markdown(f'**Records Selected:** {random_record_page1} , {random_record_page2} , {random_record_page3}' )
            preview_1_HL = csv_page1.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page1 else ['background-color: default'], axis=1)

            preview_2_HL = csv_page2.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page2 else ['background-color: default'], axis=1)

            preview_3_HL = csv_page3.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page3 else ['background-color: default'], axis=1)

            preview_col_1.dataframe(preview_1_HL)
            preview_col_2.dataframe(preview_2_HL)
            preview_col_3.dataframe(preview_3_HL)

        elif csv_records_count > 30:   

            rand_ten = randrange(10)
            rand_twenty = randint(10,19)
            rand_thirty = randint(20,29)
            rand_forty = randint(30, 39)   

            random_record_page1 = csv_records[rand_ten]
            random_record_page2 = csv_records[rand_twenty]
            random_record_page3 = csv_records[rand_thirty]
            random_record_page4 = csv_records[rand_forty]

            st.markdown(f'**Records Selected:** {random_record_page1} , {random_record_page2} , {random_record_page3} , {random_record_page4}') 
            preview_1_HL = csv_page1.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page1 else ['background-color: default'], axis=1)

            preview_2_HL = csv_page2.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page2 else ['background-color: default'], axis=1)

            preview_3_HL = csv_page3.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page3 else ['background-color: default'], axis=1)

            preview_4_HL = csv_page4.style.apply(lambda x: ['background-color: lightgreen'] if x.iloc[0] == random_record_page4 else ['background-color: default'], axis=1)

            preview_col_1.dataframe(preview_1_HL)
            preview_col_2.dataframe(preview_2_HL)
            preview_col_3.dataframe(preview_3_HL)
            preview_col_4.dataframe(preview_4_HL)

            #Select the record corresponding to each random number generated and store them in variables

        time.sleep(0.5)
        st.write('Confirming upload to Authnetikz.com')
        time.sleep(0.4)

#A function for selecting pages out of a dataframe by size and page number (pagenum = df_size/page_size)
def paginate_dataframe(dataframe, page_size, page_num):
    page_size = page_size
    if page_size is None:
        return None
    offset = page_size*(page_num-1)
    return dataframe[offset:offset + page_size]