import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px 

st.set_page_config(page_title="Employee Dashboard",
                    page_icon=None,
                    layout="wide",
                    initial_sidebar_state="expanded")
#upload the data
df=pd.read_excel("employee_data.xlsx")
##side bar
st.sidebar.title("Employee Dashboard")
st.sidebar.image("employee.jpg")
#ov=st.sidebar.button("Overview")
st.sidebar.header("Filters")
# Sidebar filters
department_filter = st.sidebar.selectbox("Department",options=["None"] + list(df["department"].unique()))
gender_filter =st.sidebar.selectbox("Gender", options=["None"] + list(df["gender"].unique()))
titles_filter=st.sidebar.selectbox("job_title", options=["None"] + list(df["job_title"].unique()))








st.header("Overview")
from streamlit_extras.metric_cards import style_metric_cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Departments", value="22")
    
with col2:
    st.metric(label="Total Employees", value="1000 ")
    
with col3:
    st.metric(label="Total Salaries", value="97.3M 💵")

style_metric_cards(
    background_color="#292929",  # Dark background for the boxes
    border_radius_px=9          # Rounded corners for the boxes
)

#second row
b1,b2,b3 = st.columns(3)
with b1:
    salary_sum_by_department = df.groupby('department')['salary'].sum().reset_index(name="Total Salary")
    salary_sum_by_department.columns = ['department', 'Total Salary']
    # Format the 'Total Salary' column to show the values as millions (M) or thousands (K)
    salary_sum_by_department['Total Salary'] = salary_sum_by_department['Total Salary'].apply(
        lambda x: f"{x/1_000_000:.1f}M" if x >= 1_000_000 else f"{x/1_000:.1f}K"
    )
    top_5_departments = salary_sum_by_department.head(5)
    st.subheader("Top 5 Salaries in each deparment")
    st.table(top_5_departments)

with b2:
    job_title_count = df['job_title'].value_counts()
    top_5_Titles = job_title_count.head(5)
    st.subheader("Top 5 Job Titles")
    st.table(top_5_Titles)

with b3:
    employees_with_24_years = df[df["experience_years"] == 24]
    experience_years_count_by_department = employees_with_24_years.groupby('department')['experience_years'].value_counts().reset_index(name="Total experience_years")
    experience_years_count_by_department.columns = ['department', 'experience_years', 'Total experience_years']
    top_5_experts = experience_years_count_by_department.head(5).drop(columns=['experience_years']).head(5).sort_values(by="Total experience_years", ascending=False)
    st.subheader("Total Employees with 24 Years")
    st.table(top_5_experts)
  
#row3
a1 ,a2 = st.columns(2)
with a1:
    st.subheader("Genders in each deparment")
    if department_filter == "None": #and gender_filter == "None":
        filtered_df = df  
    elif department_filter == "None":
        filtered_df = df[df['gender'] == gender_filter]  
    elif gender_filter == "None":
        filtered_df = df[df['department'] == department_filter]  
    else:
        filtered_df = df[(df['gender'] == gender_filter) & (df['department'] == department_filter)]
    fig2 = px.pie(data_frame=filtered_df, names='gender', hole=.4, color='gender')
    st.plotly_chart(fig2, use_container_width=True)


with a2:
    st.subheader("NO.employess VS Region")
    if department_filter == "None" and gender_filter == "None":
        filtered_df = df  
    elif department_filter == "None":
        filtered_df = df[df['gender'] == gender_filter]  
    elif gender_filter == "None":
        filtered_df = df[df['department'] == department_filter]  
    else:
        filtered_df = df[(df['gender'] == gender_filter) & (df['department'] == department_filter)]
    fig3 = px.pie(data_frame=filtered_df, names='region_id', hole=.4)
    st.plotly_chart(fig3, use_container_width=True)
    
#row4
c1  = st.columns(1)
st.subheader("Salaiers in each department regarding genders")
if department_filter == "None":
    filtered_df = df  
elif department_filter == "None":
    filtered_df = df[df['gender'] == gender_filter]  
elif gender_filter == "None":
    filtered_df = df[df['department'] == department_filter]  
else:
    filtered_df = df[(df['gender'] == gender_filter) & (df['department'] == department_filter)]
custom_colors = {
    'Male': 'brown',
    'Female': 'pink'
    }

fig4 = px.bar(
    data_frame=filtered_df,
    x='department',
    y='salary',
    color='gender',
    barmode='group',
    color_discrete_map=custom_colors
    )
st.plotly_chart(fig4, use_container_width=True)




c2 =st.columns(1)
st.subheader("Salaries VS Job Titles Regarding Genders")
custom_colors = {
    'Male': 'red',
    'Female': 'yellow'
}

if titles_filter == "None" and department_filter == "None":
    filtered_df = df
elif titles_filter == "None":
    filtered_df = df[df['department'] == department_filter]  
elif department_filter == "None":
    filtered_df = df[df['job_title'] == titles_filter] 
else:
    filtered_df = df[(df['job_title'] == titles_filter) & (df['department'] == department_filter)] 

if filtered_df.empty:
    st.write("No data available")
else:
    fig5 = px.bar(
        filtered_df,
        x='job_title',
        y='salary',
        color='gender',
        barmode='group',
        color_discrete_map=custom_colors
    )

st.plotly_chart(fig5, use_container_width=True)
