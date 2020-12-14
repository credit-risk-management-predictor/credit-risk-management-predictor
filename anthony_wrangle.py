import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import math

def get_reports_data(creditrecordcsv):
    '''
    The function takes in the credit_record.csv and creates a data frame for:
    * expanded - for each account id find out the number of times each status occured throughout the history of the account
    * score - creates a scoring system and returns the Expanded DF with the aggergated score, a score for months, and the number of times each status occured by serverity and . The higher the score the more risk
    * full_history - for each account gives the full account's history starting at the most recent month of account going backwards 
    i.e. if an account has been active for 3 months the status of the account will the most recent month's status while 2 months ago will be the first month of the account's existence
    '''
    report = pd.read_csv(creditrecordcsv)
    # number of months of active credit account for each ID 
    months = report.groupby('ID').count().reset_index()
    # pull only the columns we care about
    months = months[['ID', 'MONTHS_BALANCE']]
    # rename the columns
    months.columns = ['ID', 'MONTHS_ACTIVE']
    # Number of times each ID had each status
    expanded = report.groupby(['ID', 'STATUS']).size().unstack().reset_index()
    # Merge the expanded data frame with the months data frame
    expanded = expanded.merge(months, how='left', on='ID')
    # fill all null values with 0 
    expanded.fillna(0, inplace=True)
    # rename the columns in a way that makes sense
    expanded.columns = ['id', '0-29', '120-149', '30-59', '60-89', '90-119',
        'bad_debt', 'no_debt', 'paid_off', 'months_active']
    # Reorders the columns for clarity    
    expanded = expanded[['id', '0-29', '30-59', '60-89', '90-119', '120-149', 'bad_debt', 'no_debt', 'paid_off', 'months_active']]

    # copy the expanded dataframe to maintain data intregity (for exploring and future data prepping as needed)
    score = expanded.copy()
    # multiply each lateness by n where n is the cronological order of the lateness i.e. being 30-59days is 2 and '120-149' is 5
    # for paid off multiple by -2
    score['30-59'] = score['30-59'] * 2
    score['60-89'] = score['60-89'] * 3
    score['90-119'] =  score['90-119'] * 4
    score['120-149'] = score['120-149'] * 5
    score['bad_debt'] = score['bad_debt'] * 6
    score['paid_off'] = score['paid_off'] * -2
    # convert the id to string
    score['id'] = score['id'].astype(str)
    # Creates a score for months active
    score['time_score'] = np.where(score['months_active'] < 18, 0, np.where(score['months_active'] < 47, -10, -20))
    # sum the values on the row level
    score['score'] = score.sum(axis=1)
 
    # create a range for the maxium number of months (60) in the data frame
    # use a for loop to put get the entire account's history to the current month by shifting status by n
    for n in range(1, 61):
        report.columns = report.columns.str.lower()
        report[f'{str(n)}month_ago'] = report.groupby('id')['status'].shift(n)
    # convert the months_balance column to positive number    
    report['months_balance'] = report['months_balance']*-1
    # get the max row for each id
    full_history = report.groupby('id')[['months_balance']].max().reset_index()
    # merge the full_history df with the report df (that has current history) so that each id only has 1 row
    full_history = full_history.merge(report, how='left', on=['months_balance', 'id'])
    # rename months_balance column to account_months for age
    full_history.rename(columns={"months_balance": "account_months"}, inplace=True)
    
    # return expanded, score, and full history data frames
    return expanded, score, full_history    

def pensioner_years_worked(row):
    '''
    This function takes in a row of a dataframe and checks if the row belongs to a pensioner that is permanently retired (days_employed = -365243)
    If the pensioner is male, then the number of years worked is equal to a career from age 17 to their age or age 60, whichever is smaller
    If the pensioner is female and is blue collar, then the number of years worked is equal to a career from age 17 to their age or age 50, whichever is smaller
    If the pensioner is female and is not blue collar, then the number of years worked is equal to a career from age 17 to their age or age 55, whichever is smaller
    The starting age of 17 is based on the minimum legal working age of 16, but considers the common practice of waiting until graduation from secondary school before working in cities
    '''
    # Sets the years worked to be equal to the starting value recorded in the employed_years column. If the row is not a retired pensioner, this value will be returned and nothing will be changed
    years_worked = row['employed_years']

    # Checks if the record is from a permanently retired pensioner
    if row['days_employed'] == -365243:

        # If the pensioner is male:
        if row['code_gender'] == 'M':

            # Find the number of years worked assuming they retired at 60, or if they aren't 60 yet, assume they just retired and have worked since they were 17
            if row['age'] > 60:
                years_worked = row['age'] - 17 - (row['age'] - 60)
            else:
                years_worked = row['age'] - 17

        # If the pensioner is female:
        elif row['code_gender'] == 'F':

            # Identify if the pensioner is blue collar and eligible for earlier retirement
            blue_collar = ['Laborers', 'Drivers', 'Cooking staff', 
                           'Security staff', 'Cleaning staff', 'Low-skill Laborers', 'Waiters/barmen staff']

            # If the pensioner is blue collar, find the number of years worked assuming they retired at 50, or if they aren't 50 yet, assume they just retired and have worked since they were 17
            if row['occupation_type'] in blue_collar:
                if row['age'] > 50:
                    years_worked = row['age'] - 17 - (row['age'] - 50)
                else:
                    years_worked = row['age'] - 17
            
            # If the pensioner is not blue collar, find the number of years worked assuming they retired at 55, or if they aren't 55 yet, assume they just retired and have worked since they were 17
            else:
                if row['age'] > 55:
                    years_worked = row['age'] - 17 - (row['age'] - 55)
                else:
                    years_worked = row['age'] - 17

    return years_worked

def pensioner_days_employed(row):
    days_employed = row['days_employed']
    if row['days_employed'] == -365243:
        days_employed = math.floor(row['employed_years'] * 365.25)
    return days_employed

def get_application_data(applicationrecordcsv):
    '''
    The function takes in the application_record.csv and returns a dataframe after basic cleaning
    '''
    apps = pd.read_csv('application_record.csv')

    # Converts all column headers to lowercase
    apps.columns = (apps.columns).str.lower()

    # Fills null values in occuptation type with 'Other'
    apps['occupation_type'].fillna('Other', inplace=True)

    # Convert days employed to years employed
    apps['employed_years'] = [round(val/(-365)) if val < -365 else val/(-365)  if val < 0 else round(val/365) for val in list(apps.days_employed)]

    # Convert days_birth to age in years
    apps['age'] = (apps['days_birth']/365 * -1).apply(np.floor)

    # Convert "Yes" and "No" throughout dataframe to 1s and 0s respectively
    apps.replace({'Y': 1, 'N': 0}, inplace=True)

    # Reverses sign on days birth
    apps['days_birth'] = apps['days_birth'] * -1

    # Reverses sign on days employed
    apps['days_employed'] = apps['days_employed'] * -1

    # Changes the employed_years value of retired pensioners from 1001 to an estimate based on their current age, gender, and occupation
    apps['employed_years'] = apps.apply(lambda row: pensioner_years_worked(row), axis = 1)

    # If days employed is a stand in value (-365243), convert that to a number of days equal to the estimated number of years worked
    apps['days_employed'] = apps.apply(lambda row: pensioner_days_employed(row), axis = 1)

    # Converts id to object type
    apps['id'] = apps['id'].astype(str)

    return apps
    
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
    ##apps_encoded.drop(columns=dummies_list, inplace=True)
    
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

def wrangle_credit():
    '''
    This function utlizes the above defined functions to create the train, validate, and test data sets for analysis. 
    Note - The create_scaled_x_y function will be used after EDA to avoid confusion
    '''
    # get the credit report data into a data frame
    expanded, score, full_history = get_reports_data('credit_record.csv')
    # get the apps data into a data frame
    apps = get_application_data('application_record.csv')
    # create the dummy varaibles for the apps data
    apps = encode_dummies(apps)
    # add the score to the apps data
    apps_cred, apps_none = add_score_target(apps, score)
    # split the apps_cred data (apps + credit report) into train, validate, and test sets and return the results
    train, validate, test  = split_data(apps_cred)
    return train, validate, test