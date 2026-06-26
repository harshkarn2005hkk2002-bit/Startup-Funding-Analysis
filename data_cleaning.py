import pandas as pd

def clean_kaggle_data(df):
    df = df.drop_duplicates()

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = df['Date'].dt.year

    df['Funding Amount'] = df['Funding Amount'].replace(',', '', regex=True)
    df['Funding Amount'] = pd.to_numeric(df['Funding Amount'], errors='coerce')

    df.fillna("Unknown", inplace=True)

    return df


def clean_news_data(df):
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Year"] = df["Date"].dt.year
    return df