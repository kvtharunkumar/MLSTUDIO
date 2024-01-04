import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from linear import linear

def selectioned(independent, dependent, user_email):
    df = pd.read_csv('dataset.csv')

    selected_columns = list(independent)  # Convert independent to a list

    # Check data types correctly
    is_dependent_numerical = df[dependent].dtypes == 'int64' or df[dependent].dtypes == 'float64'

    is_selected_numerical = all(df[col].dtypes == 'int64' or df[col].dtypes == 'float64' for col in selected_columns)

    # Handle missing values and encoding
    if df[selected_columns].isna().any().any():
        if is_selected_numerical:
            imp = SimpleImputer(strategy='mean')
            df[selected_columns] = imp.fit_transform(df[selected_columns])
        else:
            imp = SimpleImputer(strategy='most_frequent')
            df[selected_columns] = imp.fit_transform(df[selected_columns])

        if is_dependent_numerical:
            imp = SimpleImputer(strategy='mean')
            df[[dependent]] = imp.fit_transform(df[[dependent]])  # Pass dependent as a list
        else:
            imp = SimpleImputer(strategy='most_frequent')
            df[[dependent]] = imp.fit_transform(df[[dependent]])

        le = LabelEncoder()
        for col in selected_columns:
            if df[col].dtype == 'O':
                df[col] = le.fit_transform(df[col])

        if df[dependent].dtype == 'O':
            df[dependent] = le.fit_transform(df[dependent])

    else:
        # Encoding for non-numerical columns
        le = LabelEncoder()
        for col in selected_columns:
            if df[col].dtype == 'O':
                df[col] = le.fit_transform(df[col])

        if df[dependent].dtype == 'O':
            df[dependent] = le.fit_transform(df[dependent])

    x = df[independent]
    y = df[dependent]
    return linear(x, y, user_email)
