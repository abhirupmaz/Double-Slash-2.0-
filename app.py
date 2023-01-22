import streamlit as st
import pickle
import numpy as np
import pandas as pd
import joblib
from fpdf import FPDF
import random
import matplotlib.pyplot as plt

#Importing the trained model
classifer = joblib.load("model.pkl")
model = pickle.load(open('/content/model.pkl','rb'))

#Importing Prediction Dataset
df = pd.read_csv('/content/Working3.csv')

#Batch Code
batchid=100

#Function to predict from the dataset
def pred(a,b,c,d,e,f,g,h,i):
  input = np.array([[a,b,c,d,e,f,g,h,i]])
  p=classifer.predict(input)
  return p

def main():
  st.title("Predictive Performance Report Generator For Tutors")
  html_temp = """
  <div style = "background-color:#024246;padding:10px;margin-bottom:20px">
  <h2 style = "color:white;text-align:center;">Performance Prediction </h2?
  </div>
  """
  st.caption('_Developed by Abhirup, Debjyoti, Rohan |   Version: 0.1._')
  batchtext=st.text_input('Enter the Batch ID:', batchid)
  st.write('Batch ID: ', f":green[{batchtext}]")
  st.markdown(html_temp,unsafe_allow_html = True)

#   print(df)
  fl = open("failed.txt", "w")
  if st.button("Generate"):
    for j in range(0,len(df)):
        a = df['QMock1'].iloc[j]
        b = df['QMock2'].iloc[j]
        c = df['QMock3'].iloc[j]
        d = df['QMock4'].iloc[j]
        e = df['GrandMock'].iloc[j]
        f = df['DPP_Solving'].iloc[j]
        g = df['Attendance'].iloc[j]
        h = df['Interaction_Level'].iloc[j]
        i = df['School_Performance'].iloc[j]
        output = pred(a,b,c,d,e,f,g,h,i)

        if output == ['0']:
            fail = df.iloc[j,0]
            fl.write(f"{fail}\n")
        else:
            pass

    fl.close()
    fl = open("failed.txt", "r")
    ids = fl.readlines()

    #PDF Report Generation
    pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 22)

    #Heading
    pdf.cell(100,20,"Predictive Report on the Performance of Students", ln=1)
    pdf.set_font('Arial', 'B', 16)

    #Sections
    pdf.set_text_color(r=255, g=255, b=255)
    pdf.set_fill_color(r=255, g=0, b=0)
    pdf.cell(110, 12, f"  POTENTIAL LOW PERFORMANCES", ln=1, fill=True)


    pdf.set_font('Arial', 'B', 14)
    pdf.cell(40, 5, "", ln=1)
    pdf.set_text_color(r=0, g=0, b=0)

    #Statistic variables
    n_mock=0
    n_attendance=0
    n_dpp=0
    n_school=0
    total=0.0
    attend1 = []
    grandmock = []
    qmockmin = []
    school1 = []

    #Suggestion messages
    mockmessage=["Mocks might be difficult for some students. Enquire students to address this issue.", "Focus on improving the seriousness of students for mocks.", "Conduct daily quizzes so that students are updated with the syllabus contents."]
    attmessage=["Persuade students to attend lectures on a regular basis.",
    "Make classes interesting enough to capture the attention.",
    "Show live demonstrations and practical applications.",
    "Interact and  engage witht students more.",
    "Explain importance of being a regular attendee to class."]    
    dppmessage=["Advice the students to fix a particular time to solve the DPP",
    "Ensure that the students have a fixed number of  target questions to solve",
    "Make sure to Clear the doubts on student's unsolved questions",
    "Provide the steps to  approaches a problem in different ways",
    "Encourage students to come up with short tricks"]
    schoolmessage=["Advice students to learn from the Mock Tests and Grand Mock Test",
    "Understand the problems of student via one-on-one interaction",
    "Keep a track of students to Solve DPP regularly",
    "Provide extra classes for enabling better school performance"] 

    #Iterate through failed list of students
    for cid in ids:
        total+=1
        current_id=cid.strip()
        current_row = df.loc[df['ID'] == int(current_id)]
        name = current_row.iloc[0,1]
        qmock = min(current_row.iloc[0,2],current_row.iloc[0,3],current_row.iloc[0,4],current_row.iloc[0,5])
        gmock = current_row.iloc[0,6]
        dpp = current_row.iloc[0,7]
        attendance = current_row.iloc[0,8]
        school = current_row.iloc[0,10]
        print(name)
        temp=f"{name} "
        if(qmock<30 and gmock<65):
            temp=temp+"   -MOCK"
            n_mock+=1
        if(attendance<55):
            temp=temp+"   -ATTENDANCE"
            n_attendance+=1
        if(dpp<28):
            temp=temp+"   -DPP"
            n_dpp+=1
        if(school<60):
            temp=temp+"   -SCHOOL"
            n_school+=1

        #Individual drawbacks    
        pdf.cell(100, 7.5, f"{temp}", ln=1)
        pdf.cell(40, 5, "", ln=1)
        grandmock.append(gmock)
        attend1.append(attendance)
        qmockmin.append(qmock*2)
        school1.append(school)

    #Aggregate Statistics    
    if(total>0):
        mock_per=(n_mock/total)*100 
        att_per=(n_attendance/total)*100 
        dpp_per=(n_dpp/total)*100
        school_per=(n_school/total)*100
        pdf.cell(40, 10, "", ln=1) #Spacing
        pdf.set_fill_color(r=0, g=0, b=255)
        pdf.set_text_color(r=255, g=255, b=255)
        pdf.cell(70, 12, f"  AGGREGATE STATISTICS", ln=1, fill=True)
        pdf.set_text_color(r=0, g=0, b=0)
        pdf.cell(40, 5, "", ln=1)
        pdf.cell(100, 7.5, f"{mock_per:.2f}% of predicted failed students did not score well in the mocks.", ln=1)
        pdf.cell(100, 7.5, f"{att_per:.2f}% of predicted failed students did not attend classes regularly.", ln=1)
        pdf.cell(100, 7.5, f"{dpp_per:.2f}% of predicted failed students did not solve enough dpps.", ln=1)
        pdf.cell(100, 7.5, f"{school_per:.2f}% of predicted failed students did not score well in the school exams.", ln=1)
        pdf.cell(40, 10, "", ln=1) #Spacing
        pdf.set_fill_color(r=0, g=0, b=255)
        pdf.set_text_color(r=255, g=255, b=255)

        #Suggestions
        pdf.cell(45, 12, f"  SUGGESTIONS", ln=1, fill=True)
        pdf.set_text_color(r=0, g=0, b=0)
        pdf.cell(40, 5, "", ln=1)
        pdf.set_text_color(r=14, g=55, b=20)
        pdf.cell(100, 7.5, random.choice(mockmessage), ln=1)
        pdf.cell(100, 7.5, random.choice(attmessage), ln=1)
        pdf.cell(100, 7.5, random.choice(dppmessage), ln=1)
        pdf.cell(100, 7.5, random.choice(schoolmessage), ln=1)

    #Graphical statistics    
    pdf.add_page()
    pdf.set_fill_color(r=0, g=0, b=255)
    pdf.set_text_color(r=255, g=255, b=255)
    pdf.cell(90, 12, f"  SOME GRAPHICAL STATISTICS", ln=1, fill=True)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.cell(40, 5, "", ln=1)

    #Trend in School Performance with GrandMocks
    x = np.array(grandmock)  
    y = np.array(school1)  
    plt.scatter(x, y,c ="red")
    plt.title("Trend in School Performance with GrandMocks")
    plt.grid()
    plt.legend()
    plt.xlabel("Grandmock")
    plt.ylabel("School Performance")
    plt.show() 
    plt.savefig('scatter1.png')
    pdf.image(name ='/content/scatter1.png', x = None, y = None, w = 180, h = 120, type = 'PNG')

    #Trend in Grand Mocks with Attendance
    plt.scatter(np.array(attend1), np.array(grandmock),c ="red")  
    plt.title("Trend in Grand Mocks with Attendance")
    plt.legend()
    plt.xlabel("Attendance")  
    plt.ylabel("Grand Mock") 
    plt.show() 
    plt.savefig('scatter2.png')
    pdf.image(name ='/content/scatter2.png', x = None, y = None, w = 180, h = 120, type = 'PNG')

    #Save pdf
    pdf.output(f'report_{batchtext}.pdf', 'F')
    st.success('Performance report successfully generated!')
    
    with open(f'report_{batchtext}.pdf', "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    #Download Button for Report
    st.download_button(label="Download",
        data=PDFbyte,
        file_name=f'report_{batchtext}.pdf',
        mime='application/octet-stream')
    

if __name__=='__main__':
  main()