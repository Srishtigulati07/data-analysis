import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

@st.cache_data()
def load_data():
    return pd.read_csv('datasets/data.csv')

with st.spinner("loading datasets..."):
  df=load_data()

st.title('My Datascience App')
st.dataframe(df)

st.header('Data Visualisation')
st.subheader('Top 10 Job titles of the employee')
job_count=df['job_title'].value_counts().head(10)
fig1=px.bar(job_count,
            job_count.index,
            job_count.values,
            title='job titles of the employee')
st.plotly_chart(fig1,use_container_width=True)
st.subheader("these are the popular jobs")
st.info(",".join(job_count.index.tolist()))


categories=df.select_dtypes(exclude=np.number).columns.tolist()
st.success(f'there are following categories:{", ".join(categories)}')
for col in categories:
   counts=df[col].value_counts()
   if df[col].nunique()>10:
      fig=px.bar(counts,
                 counts.index,
                 counts.values,
                 log_y=True,
                 text=counts.values,
                 title=f'Distribution of{col}')
      fig.update_traces(texttemplate='%{text:.25}',textposition='outside')
   else:
      fig=px.pie(counts,
                 counts.index,
                 counts.values,
                 title=f'Distribution of {col}')
      st.plotly_chart(fig,use_container_width=True)

year_wise_df=df.groupby('work_year')[['salary','salary_in_usd']].sum().reset_index()
year_wise_df=df.groupby('work_year')[['salary','salary_in_usd']].mean().reset_index() 
st.dataframe(year_wise_df)

fig=px.bar(year_wise_df,
           'work_year','salary_in_usd',
           title='Mean salary trend over the years')
c1,c2=st.columns(2)
c1.plotly_chart(fig,use_container_width=True)
c2.plotly_chart(fig,use_container_width=True)


c1,c2=st.columns(2)
cats = c1.multiselect('select categories',categories)
graphs=['box','violin','swarp','sunburst','trreemap']
graph=c2.selectbox('select graph',graphs)

for col in cats:
   if graph == graphs[0]:
      fig=px.box(df,x=col,y='salary_in_used',title=f'salary distribution of{col}')
   elif graph== graphs[1]:
      fig=px.violin(df,x=col,y='salary_in_usd',theta=col,title=f'salary distribution of{col}')
   elif graph==graphs[2]:
      fig=px.bar_barpolar(df,r='salary_in_usd',title=f'salary distribution of col{col}')
      st.pylot(fig,use_container_width=True)
if graph == graphs[3]:
   fig=px.sunburst(df,path=cats,values='salary_in_usd',title=f'salary distribution of{col}')
if graph==graphs[4]:
   fig=px.treemap(df,path=cats,values='salary_in_usd',title=f'salary distribution of {col}')
   st.plotly_chart(fig,use_conatainer_width=True)