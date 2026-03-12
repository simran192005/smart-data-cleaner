import pandas as pd
def auto_clean_data(df):
    df=df.drop_duplicates()
    df.columns=(
        df.columns.str.strip().str.lower().str.replace(" ","_")
    )  
    for col in df.select_dtypes(include ="object").columns:
        df[col]=df[col].str.strip()
    for col in df.columns:
        if df[col].dtype=="object":
            df[col]=df[col].fillna("Unknown")
        elif df[col].dtype in ["int64","float64"]:
            df[col]=df[col].fillna(df[col].median())
    df=df.reset_index(drop=True)
    return df