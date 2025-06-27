import pandas as pd

def load_csv_data(csv_path):
    """Load CSV into DataFrame"""
    df = pd.read_csv(csv_path)
    return df

if __name__ == "__main__":
    df = load_csv_data("../data/fake_data.csv")
    print(df.head())
