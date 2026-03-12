import streamlit as st
import pandas as pd

from cleaning import auto_clean_data
from visualization import histogram, bar_chart, scatter_plot, correlation_heatmap
from utils import data_quality_score, suggest_chart, generate_insights, detect_outliers, generate_story

st.set_page_config(
    page_title="Smart Data Cleaner",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
            <style>
            [data-testid="stMetricValue"]{
            font-size:32px;
            }
            [data-testid="stMetricLabel"]{
            font-size:16px
            }
            </style>""",unsafe_allow_html=True)
st.markdown("""
# 📊 Smart Data Cleaner & Visualizer
 
Upload messy datasets → Automatically clean them → Get their Analysis → Generate insights instantly.

---
""")

st.sidebar.header("Upload Dataset")
uploaded_file= st.sidebar.file_uploader(
    "Upload CSV  or Excel file",
    type=["csv","xlsx"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df= pd.read_csv(uploaded_file)
    else:
        df=pd.read_excel(uploaded_file)
    st.success("Dataset Uploaded Sucessfully...!")

    with st.expander("Dataset Information"):
        st.write("Columns:")
        st.write(list(df.columns))
        st.write("DataTypes:")
        st.write(df.dtypes)

    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = df
    if st.button("🧹 Clean Data"):
        st.session_state.cleaned_df = auto_clean_data(df)
        st.success("Dataset Cleaned Successfully")
    df = st.session_state.cleaned_df
    score= data_quality_score(df)
    st.subheader("Data Quality Score")
    st.metric("Quality Score",f"{score}%")
    st.markdown("---")
    st.header("📊 Data Dashboard")
    col1,col2,col3,col4= st.columns(4, gap="large")
    col1.metric("Rows",df.shape[0])
    col2.metric("Columns",df.shape[1])
    col3.metric("Missing Values",df.isnull().sum().sum())
    col4.metric("Duplicate Rows",df.duplicated().sum())
    
    tab1,tab2,tab3=st.tabs(
        ["📊 Data Preview", "📈 Visualizations", "📑 Summary"]
    )
    with tab1:
        st.subheader("Cleaned Dataset Preview")
        st.dataframe(df.head(20), hide_index=True)
        st.subheader("Download Cleaned Dataset")
        csv=df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Cleaned Dataset",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv")
    with tab2:
        st.subheader("VIsualizations")
        chart_type=st.selectbox(
            "Select Chart Type",
            ["Histogram", "Bar Chart", "Scatter Plot"]
        )
        numeric_cols=df.select_dtypes(include="number").columns
        all_cols=df.columns
        if chart_type=="Histogram":
            column=st.selectbox("Column",numeric_cols)
            suggestion=suggest_chart(str(df[column].dtype))
            st.write(f"Suggested Chart Type: {suggestion}")
            fig=histogram(df,column)
            st.plotly_chart(fig, width="stretch")
        elif chart_type=="Bar Chart":
            x_col=st.selectbox("X Axis",all_cols)
            y_col=st.selectbox("Y Axis",numeric_cols)
            fig=bar_chart(df, x_col, y_col)
            st.plotly_chart(fig, width="stretch")
        elif chart_type=="Scatter Plot":
            x_col=st.selectbox("X Axis",numeric_cols)
            y_col=st.selectbox("Y Axis",numeric_cols)
            fig=scatter_plot(df, x_col, y_col)
            st.plotly_chart(fig, width="stretch")
        st.subheader("Correlation Heatmap")
        heatmap=correlation_heatmap(df)
        st.plotly_chart(heatmap, width="stretch")
    with tab3:
        st.subheader("Statistical Summary")
        st.dataframe(df.describe())
        st.subheader("🔎Insights")
        insights = generate_insights(df)
        for insight in insights:
            st.write("•", insight)
        st.subheader("⚠Outlier Detection")
        outliers=detect_outliers(df)
        if len(outliers)==0:
            st.success("No significant outliers detected in numeric columns.")
        else:
            for item in outliers:
                st.warning(item)
        st.subheader("📖 Dataset Story")
        story = generate_story(df)
        st.write(story)
else:
    st.info("Upload a dataset from the sidebar to begin.")