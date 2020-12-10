import pandas as pd
import numpy as np

def get_reports_data(creditreportcsv):
    '''
    The fuction takes in the credit report csv and creates a data frame for:
    * expanded - for each account id find out the number of times each status occured throughout the history of the account
    * score - creates a scoring system and returns the Expanded with the aggergated score and the number of times each status occured by serverity
    * full_history - for each account gives the full account's history starting at the most recent month of account going backwards 
    i.e. if an account has been active for 3 months the status of the account will the most recent month's status while 2 months ago will be the first month of the account's existence
    '''
    report = pd.read_csv(creditreportcsv)
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
    