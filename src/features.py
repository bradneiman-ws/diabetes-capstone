import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def basic_preprocess(df: pd.DataFrame, numeric_strategy="median"):
    num_cols = df.select_dtypes(include=[float, int, "number"]).columns.tolist()
    cat_cols = [c for c in df.columns if c not in num_cols]

    numeric = Pipeline([
        ('imputer', SimpleImputer(strategy=numeric_strategy)),
        ('scaler', StandardScaler())
    ])
    categoric = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    pre = ColumnTransformer(
        transformers=[('num', numeric, num_cols),
                      ('cat', categoric, cat_cols)],
        remainder='drop'
    )
    return pre
