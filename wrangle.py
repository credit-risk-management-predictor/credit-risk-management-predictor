import pandas as pd
import numpy as np
import math

def get_reports_data(creditrecordcsv):
    '''
    The function takes in the credit_record.csv and creates a data frame for:
    * expanded - for each account id find out the number of times each status occured throughout the history of the account
    * score - creates a scoring system and returns the Expanded with the aggergated score and the number of times each status occured by serverity
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
    # multiple each lateness by n where n is cronological order of the lateness i.e. being 30-59days is 2 and '120-149' is 5
    # for paid off multiple by -2
    score['30-59'] = score['30-59'] * 2
    score['60-89'] = score['60-89'] * 3
    score['90-119'] =  score['90-119'] * 4
    score['120-149'] = score['120-149'] * 5
    score['bad_debt'] = score['bad_debt'] * 6
    score['paid_off'] = score['paid_off'] * -2
    # convert the id to string
    score['id'] = score['id'].astype(str)
    # sum the values on the row level
    score['score'] = score.sum(axis=1)
 
    # create a range for the maxium number of months (61) in the data frame
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