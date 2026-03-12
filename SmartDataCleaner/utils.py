import pandas as pd
def data_quality_score(df):
    total_cells=df.shape[0]*df.shape[1]
    missing=df.isnull().sum().sum()
    duplicates=df.duplicated().sum()
    score=100
    if total_cells>0:
        score-=(missing/total_cells)*50
    if len(df)>0:
        score-=(duplicates/len(df))*50
    return round(score,2)
def suggest_chart(column_dtype):
    if column_dtype in ["int64","float64"]:
        return "Histogram"
    elif column_dtype=="object":
        return "Bar Chart"
    else:
        return "Scatter Plot"
def generate_insights(df):
    insights = []
    numeric_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(include="object").columns
    for col in numeric_cols:
        avg = df[col].mean()
        insights.append(f"Average {col} is {round(avg,2)}")
    for col in cat_cols:
        top = df[col].mode()[0]
        insights.append(f"Most common {col} is {top}")
    insights.append(
        f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns"
    )
    return insights
def detect_outliers(df):
    outlier_info=[]
    numeric_cols=df.select_dtypes(include="number").columns
    for col in numeric_cols:
        Q1=df[col].quantile(0.25)
        Q3=df[col].quantile(0.75)
        IQR=Q1-Q3
        lower=Q1-1.5*IQR
        upper=Q3+1.5*IQR
        outliers=df[(df[col]<lower)|(df[col]>upper)]
        if len(outliers)>0:
            outlier_info.append(
                f"{col} has {len(outliers)} potential outliers"
            )
    return outlier_info
def generate_story(df):
    rows = df.shape[0]
    cols = df.shape[1]
    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    story = f"""
This dataset contains {rows} rows and {cols} columns. 
After cleaning, the dataset has {missing} missing values and {duplicates} duplicate rows.

The dataset mainly contains {len(df.select_dtypes(include='number').columns)} numeric columns 
which makes it suitable for statistical analysis and visualization.

Exploring the dataset can reveal trends, relationships between variables, 
and potential outliers that may affect analysis.
"""
    return story