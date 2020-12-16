import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import math

def get_reports_data(creditrecordcsv):
    '''
    The function takes in the credit_record.csv and creates a DF that:
    * Extracts IDs that have defaulted and have 11 months of history before defaulting
    * Extracts IDs that have not defaulted and have at least 12 months of history 
    * For defaulted IDs pulls the 11 months of data before defaulting
    * For not_defaulted IDs pull the most recent 12 months of data
    * Finds the counts of each status type during the 12months of data present for both deafult and not_defaulted ids
    Note - Each row is single ID and has the 12 month's of history as noted above
    '''
    
    # Read in the DF
    report = pd.read_csv(creditrecordcsv)
    # Convert the columns to lower case
    report.columns = report.columns.str.lower()
    
    # create a DF that pulls in all the default IDs and the month they defaulted
    default = report[report['status']=='5'][['months_balance', 'id']].groupby('id').min().reset_index()
    default.columns = ['id', 'first_deafult_month']

    # create a DF that has all the ids and their minimum month of existence
    min_month = report[['months_balance', 'id']].groupby('id').min().reset_index()
    min_month.columns = ['id', 'first_month']
    
    # merge the default DF with the min_month DF
    default = default.merge(min_month, on='id', how='left')
    # find the number of months that existed in the data before the first default
    default['months_before_default'] = abs(default['first_month']) - abs(default['first_deafult_month'])
    # pull out all default ids to drop from the reports DF
    default_ids = list(default.id.unique())
    # reassign the default DF to only those accounts that had 12 or more months of info before a default
    default = default[default['months_before_default'] >= 12]
    # merge the default DF onto the reports DF to get everything into a single DF
    default_report = report.merge(default, on='id', how='left')

    # create a new DF that only contains the 12 months of data for the ids that had defaults
    default_data =(
        default_report[(default_report['months_balance'] >= default_report['first_deafult_month'] - 11) 
            & (default_report['months_balance'] <= default_report['first_deafult_month'])]
    )
    # then reduce the DF to only contain the first 6 months of that data to have a blind period of 6 months
    default_data = default_data[default_data['months_balance'] < default_data['first_deafult_month'] - 5]
    # finally drop the columns that aren't needed
    default_data = default_data[['id', 'months_balance', 'status']]

    # create the not_default DF from the reports DF by dropping any id that had a default
    not_default = report[~report['id'].isin(default_ids)]
    # from the not_default, find the max month and min month an id existed.
    not_default_data = not_default.groupby('id')['months_balance'].agg(['max', 'count']).reset_index()
    # find the number of months total an id was present
    not_default_data = not_default_data[not_default_data['count']>=12]
    # Pull out the not_default_ids to drop from the report DF 
    not_default_ids = list(not_default_data['id'].unique())
    # drop the ids that don't have at least 12 months of data
    not_default = not_default[not_default['id'].isin(not_default_ids)]
    # merge the not_default DF with not_default_data to get everything onto one DF
    not_default = not_default.merge(not_default_data, on='id', how='left')
    # reassign not_default to only data only present for the last 12 months of an account's existence 
    not_default = (not_default[(not_default['months_balance']<=not_default['max']) 
                            & (not_default['months_balance']>=not_default['max']-11)])
    # then reduce the DF to only contain the first 6 months of that data to have a blind period of 6 months
    not_default = not_default[not_default['months_balance'] < not_default['max'] - 5]
    # drop the columns used for calculations
    not_default= not_default[['id', 'months_balance', 'status']]

    # concat the not_default  and default_data frames together to form a single DF
    full=pd.concat([not_default, default_data])
    # reset the index and drop the previous index
    full = full.reset_index(drop=True)
    # create target variable of defaulted
    
    # expand the full DF to make it so that each row is a single id
    expanded = full.groupby(['id', 'status']).size().unstack().reset_index()
    # fill all null values with 0 
    expanded.fillna(0, inplace=True)
    # rename the columns in a way that makes sense
    expanded.columns = ['id', '0-29', '30-59', '60-89', '90-119', '120-149', 'paid_off', 'no_debt']

    # find the max month of each id was present from full DF
    max_month = full.groupby('id')[['months_balance']].max().reset_index()
    max_month.columns=['id','max_month']
    max_month
    #merge the max month to the expanded DF. This will be used to get the full history for each id onto a single row
    expanded = expanded.merge(max_month, on='id', how='left')
    
    # create a range for the maxium number of months (12) in the DF
    # use a for loop to put get the entire account's history to the current month by shifting status by -n
    for n in range(1, 6):
        full[f'{str(n)}month_ago'] = full.groupby('id')['status'].shift(-n)
    # Then merge the full df into the expanded DF on id and max month to get the full history for each id onto a single row
    expanded = expanded.merge(full, left_on=['id', 'max_month'], right_on=['id', 'months_balance'], how='left')

    # Rename the columns so that status = 12th month and it counts up rather than down
    expanded.rename(columns={'status':'month_06',
       '1month_ago':'month_05', 
       '2month_ago': 'month_04', 
       '3month_ago': 'month_03', 
       '4month_ago': 'month_02',
       '5month_ago': 'month_01'}, inplace=True)

    # drop months_balance and max_month column and rearrage columns to make sense
    expanded = expanded[['id', '0-29', '30-59', '60-89', '90-119', '120-149', 'paid_off', 
                        'no_debt', 'month_01', 'month_02', 'month_03', 'month_04', 'month_05', 'month_06']]

    # create a months_exist DF to house the number of months an account was present (full history)
    months_exist = report.groupby('id')[['months_balance']].count().reset_index()
    months_exist.columns = ['id', 'months_exist']
    # left join the months_exist DF onto the expanded DF
    expanded = expanded.merge(months_exist, on='id', how='left')
 
    # create a DF that contains Id and month_01 - month_06 and replace the values in the months columns with scores
    replace_month = expanded[['id', 'month_01', 'month_02', 'month_03', 'month_04', 'month_05', 'month_06']].replace({'0':2, '1':3, '2':4, '3':5,
                                                                                        '4':6, 'X':0, 'C':1})
    # drop the months columns from the original DF
    expanded.drop(['month_01', 'month_02',
        'month_03', 'month_04', 'month_05', 'month_06'], axis=1, inplace=True)
    # Merge the original DF with the replace_month DF
    expanded = expanded.merge(replace_month, on='id', how='left')
    
    # Create score features
    expanded['total_score'] = expanded['month_01'] + expanded['month_02'] + expanded['month_03'] + expanded['month_04'] + expanded['month_05'] + expanded['month_06']
    expanded['odd_months_score'] = expanded['month_01'] + expanded['month_03'] + expanded['month_05']
    expanded['last_half_score'] = expanded['month_04'] + expanded['month_05'] + expanded['month_06']
    expanded['first_half_score'] = expanded['month_01'] + expanded['month_02'] + expanded['month_03']
    expanded['last_half_score'] = expanded['month_04'] + expanded['month_05'] + expanded['month_06']
    expanded['difference_score'] = expanded['last_half_score'] - expanded['first_half_score'] 
    expanded['odds_evens_score'] = expanded['month_01'] + expanded['month_03'] + expanded['month_04'] + expanded['month_06']
    expanded['begining_score'] = expanded['month_01'] + expanded['month_02']
    expanded['middle_score'] = expanded['month_03'] + expanded['month_04'] 
    expanded['ending_score'] = expanded['month_05'] + expanded['month_06'] 
    expanded['spread_score'] = expanded['month_02'] + expanded['month_03'] + expanded['month_04'] + expanded['month_05']
    expanded['alpha_omgea_score'] = expanded['month_01'] + expanded['month_06']
    expanded['begining_ending_score'] = expanded['begining_score'] + expanded['ending_score']
    
    # create the targbet varaible by only looking at ids that 
    expanded['defaulted'] = expanded['id'].isin(default_ids).astype(int)
    # return the expanded DF
    return expanded
    
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

    return apps

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
    This function does the following:
    * uses get_reports_data function to process credit_reports.csv data into the expanded DF 
    * uses get_application_data functionto process the application_record.csv into an apps DF
    * uses encode_dummies function to create dummy variables from the categorical variables of the apps DF
    * merges the apps and expanded DFs into a final_df on 'id'
    * uses split_stratify_data on the final_df to create the train, validate, test data sets
    * return train, validate, test data sets as DFs
    Note - The create_scaled_x_y function will be used after EDA to avoid confusion.
    Note 2 - Remember to drop columns not used as features such as age, gender, etc
    '''
    # get the credit report data into a DF
    expanded = get_reports_data('credit_record.csv')
    # get the apps data into a DF
    apps = get_application_data('application_record.csv')
    # create the dummy varaibles for the apps data
    apps = encode_dummies(apps)
    # add the score to the apps data
    final_df = apps.merge(expanded, on='id', how='inner')
    # split the apps_cred data (apps + credit report) into train, validate, and test sets and return the results
    train, validate, test = split_stratify_data(final_df, 'defaulted')
    return train, validate, test