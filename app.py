import streamlit as st
import pandas as pd
import base64,random
import time,datetime 

#libraries to parse the resume pdf files
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from courses import ds_course,web_course,android_course,ios_course,uiux_course

# import pafy #for uploading youtube videos
import plotly.express as px #to create visualisations at the admin session
import nltk
#nltk.download('stopwords')


#CONNECT TO DATABASE
connection = pymysql.connect(host='localhost',user='root',password='root',db='resume')
cursor = connection.cursor()

def insert_data(name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (name, email, str(res_score), timestamp,str(no_of_pages), reco_field, cand_level, skills,recommended_skills,courses)
    cursor.execute(insert_sql, rec_values)

st.set_page_config(
   page_title="AI Resume Analyzer",
   page_icon='./Logo/logo2.png',
)

# Create the DB
db_sql = """CREATE DATABASE IF NOT EXISTS resume;"""
cursor.execute(db_sql)

# Create table
DB_table_name = 'user_data'
table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                (ID INT NOT NULL AUTO_INCREMENT,
                    Name varchar(500) NOT NULL,
                    Email_ID VARCHAR(500) NOT NULL,
                    resume_score VARCHAR(8) NOT NULL,
                    Timestamp VARCHAR(50) NOT NULL,
                    Page_no VARCHAR(5) NOT NULL,
                    Predicted_Field BLOB NOT NULL,
                    User_level BLOB NOT NULL,
                    Actual_skills BLOB NOT NULL,
                    Recommended_skills BLOB NOT NULL,
                    Recommended_courses BLOB NOT NULL,
                    PRIMARY KEY (ID));
                """
cursor.execute(table_sql)


def run():
    img = Image.open('./Logo/logo2.png')
    st.image(img)
    st.title("AI Resume Analyser")
    st.sidebar.markdown("# Choose User")
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)

    if choice == 'User':
        st.markdown('''<h5 style='text-align: left; color: #021659;'> Upload your resume, and get smart recommendations</h5>''',
                    unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            with st.spinner('Uploading your Resume...'):
                time.sleep(4)
            save_image_path = './Uploaded_Resumes/'+pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                ## Get the whole resume data
                resume_text = pdf_reader(save_image_path)

                st.header("**Resume Analysis**")
                st.success("Hello "+ resume_data['name'])
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: '+resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Resume pages: '+str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >=3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)


run()