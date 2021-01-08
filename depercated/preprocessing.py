import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def add_score_target(apps, score):
    '''
    This takes in the apps and score dataframes and returns apps_cred, which contains all applications with credit records with their score attached
    and apps_none, which are all applications that have no credit record
    '''
    # Reduces the score dataframe to only the id and score columns
    score = score[['id', 'score']]
    
    # Merges on the left, leaving many records with NaN for score
    apps = apps.merge(score, how='left', on = 'id')
    
    # Creates a dataframe where the score is not null (these applications have a credit record)
    apps_cred = apps[apps.score.notnull()]
    apps_cred.reset_index(drop=True, inplace=True)

    # Creates a dataframe where the score is null (these applications do not have a credit record)
    apps_none = apps[apps.score.isna()]
    apps_none = apps_none.drop(columns='score')
    apps_none.reset_index(drop=True, inplace=True)
    
    return apps_cred, apps_none

def add_apps_dummies(apps):
    '''
    This returns the apps dataframe with dummy variables
    '''
    # Create list of categorical variables to make dummies of
    dummies_list = ['name_income_type', 'name_education_type', 'name_family_status', 'name_housing_type', 'occupation_type'] 
    
    # Create dummies dataframe
    dummies = pd.get_dummies(apps[dummies_list])
    
    # Convert dummy column headers to snake case style
    dummies.columns = dummies.columns.str.lower()
    dummies.columns = dummies.columns.str.replace(" ", "_")
    
    # Concate with original dataframe
    apps_dummies = pd.concat([apps, dummies], axis=1)
    
    return apps_dummies

def encode_dummies(apps):
    '''
    This returns the apps dataframe with dummy variables
    '''
    # Create list of categorical variables to make dummies of
    dummies_list = ['name_income_type', 'name_education_type', 'name_housing_type', 'occupation_type'] 
    
    # Create dummies dataframe
    dummies = pd.get_dummies(apps[dummies_list])
    
    # Convert dummy column headers to snake case style
    dummies.columns = dummies.columns.str.lower()
    dummies.columns = dummies.columns.str.replace(" ", "_")
    
    # Concate with original dataframe
    apps_encoded = pd.concat([apps, dummies], axis=1)
    
    # Drop original columns
    apps_encoded.drop(columns=dummies_list, inplace=True)
    
    # Drop gender, age, and family status
    dropped = ['code_gender', 'name_family_status', 'age']
    apps_encoded.drop(columns=dropped, inplace=True)

    return apps_encoded   

def split_data(df, pct=0.10):
    '''
    Divides the dataframe into train, validate, and test sets.
        
    Parameters - (df, pct=0.10)
    df = dataframe you wish to split
    pct = size of the test set, 1/2 of size of the validate set

    Returns three dataframes (train, validate, test)
    '''
    train_validate, test = train_test_split(df, test_size=pct, random_state = 123)
    train, validate = train_test_split(train_validate, test_size=pct*2, random_state = 123)
    return train, validate, test

def split_stratify_data(df, stratify_tgt, pct=0.10):
    '''
    Divides the dataframe into train, validate, and test sets, stratifying on stratify. 
        
    Parameters - (df, pct=0.10)
    df = dataframe you wish to split
    pct = size of the test set, 1/2 of size of the validate set

    Returns three dataframes (train, validate, test)
    '''

    train_validate, test = train_test_split(df, stratify=df[stratify_tgt], test_size=pct, random_state = 123)
    train, validate = train_test_split(train_validate, stratify=train_validate[stratify_tgt], test_size=pct*2, random_state = 123)

    return train, validate, test

def standard_scaler(train, validate, test):
    '''
    Accepts three dataframes and applies a standard scaler to convert values in each dataframe
    based on the mean and standard deviation of each dataframe respectfully. 
    Columns containing object data types are dropped, as strings cannot be directly scaled.

    Parameters (train, validate, test) = three dataframes being scaled
    
    Returns (scaler, train_scaled, validate_scaled, test_scaled)
    '''
    # Remove columns with object data types from each dataframe
    train = train.select_dtypes(exclude=['object'])
    validate = validate.select_dtypes(exclude=['object'])
    test = test.select_dtypes(exclude=['object'])
    # Fit the scaler to the train dataframe
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(train)
    # Transform the scaler onto the train, validate, and test dataframes
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    validate_scaled = pd.DataFrame(scaler.transform(validate), columns=validate.columns.values).set_index([validate.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, validate_scaled, test_scaled

def scale_inverse(scaler, train_scaled, validate_scaled, test_scaled):
    '''
    Takes in three dataframes and reverts them back to their unscaled values

    Parameters (scaler, train_scaled, validate_scaled, test_scaled)
    scaler = the scaler you with to use to transform scaled values to unscaled values with. Presumably the scaler used to transform the values originally. 
    train_scaled, validate_scaled, test_scaled = the dataframes you wish to revert to unscaled values

    Returns train_unscaled, validated_unscaled, test_unscaled
    '''
    train_unscaled = pd.DataFrame(scaler.inverse_transform(train_scaled), columns=train_scaled.columns.values).set_index([train_scaled.index.values])
    validate_unscaled = pd.DataFrame(scaler.inverse_transform(validate_scaled), columns=validate_scaled.columns.values).set_index([validate_scaled.index.values])
    test_unscaled = pd.DataFrame(scaler.inverse_transform(test_scaled), columns=test_scaled.columns.values).set_index([test_scaled.index.values])
    return train_unscaled, validate_unscaled, test_unscaled

def create_scaled_x_y(train, validate, test, target):
    '''
    Accepts three dataframes (train, validate, test) and a target variable. 
    Separates the target variable from the dataframes, scales train, validate, and test
    and returns all 6 resulting dataframes.
    '''
    y_train = train[target]
    X_train = train.drop(columns=[target])
    y_validate = validate[target]
    X_validate = validate.drop(columns=[target])
    y_test = test[target]
    X_test = test.drop(columns=[target])
    scaler, X_train_scaled, X_validate_scaled, X_test_scaled = standard_scaler(X_train, X_validate, X_test)
    return X_train_scaled, y_train, X_validate_scaled, y_validate, X_test_scaled, y_test