import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales & Revenue Dashboard",layout="wide")
st.title("📊 Sales & Revenue Analysis Dashboard")

uploaded=st.file_uploader("Upload CSV/Excel",type=["csv","xlsx"])

if uploaded:
    if uploaded.name.endswith(".csv"):
        df=pd.read_csv(uploaded)
    else:
        df=pd.read_excel(uploaded)
else:
    df=pd.read_csv("sales_data.csv")

df["Date"]=pd.to_datetime(df["Date"])

st.sidebar.header("Filters")
regions=st.sidebar.multiselect("Region",df["Region"].unique(),default=df["Region"].unique())
cats=st.sidebar.multiselect("Category",df["Category"].unique(),default=df["Category"].unique())
df=df[df["Region"].isin(regions)]
df=df[df["Category"].isin(cats)]

c1,c2,c3=st.columns(3)
c1.metric("Total Sales",int(df["Sales"].sum()))
c2.metric("Total Revenue",f"₹{df['Revenue'].sum():,.0f}")
c3.metric("Orders",len(df))

trend=df.groupby("Date",as_index=False)["Revenue"].sum()
st.plotly_chart(px.line(trend,x="Date",y="Revenue",title="Revenue Trend"),use_container_width=True)

top=df.groupby("Product",as_index=False)["Revenue"].sum().sort_values("Revenue",ascending=False).head(10)
st.plotly_chart(px.bar(top,x="Product",y="Revenue",title="Top Products"),use_container_width=True)

reg=df.groupby("Region",as_index=False)["Sales"].sum()
st.plotly_chart(px.pie(reg,names="Region",values="Sales",title="Region-wise Sales"),use_container_width=True)

cat=df.groupby("Category",as_index=False)["Revenue"].sum()
st.plotly_chart(px.bar(cat,x="Category",y="Revenue",color="Revenue",title="Category Revenue"),use_container_width=True)

st.subheader("Dataset")
st.dataframe(df)
