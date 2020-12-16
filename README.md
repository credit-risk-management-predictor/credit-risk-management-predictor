## Project Title 
## Table of Contents
- [Goal](#goal)
- [Wrangle](#wrangle)
  - [Acquire](#acquire)
  - [Pre-processing](#pre-processing)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
  - [Hypothesis Testing](#hypothesis-testing)
- [Modeling](#modeling)
- [Results & Conclusion](#results--conclusion)
  - [Next Steps](#next-steps)
- [Appendix](#appendix)
  - [Team Members:](#team-members)
  - [Data Dictionary](#data-dictionary)

# Goal
Chinese banks are very risk-averse, yet younger generations are more willing to take on debt at similar rates to other developed countries. What are the contributing factors to a credit card holder defaulting on debt? How can we know if an account will default 6 months into the future? That is what we aim to find out! We will accomplish this by looking for patterns in user's credit history and application data, with a watchful eye to ethical consideration.

This project will contain
* A [Jupyter Notebook]() - needs link
* A 5 minute [presentation] needs link 
* A [data dictionary](#data-dictionary) (linked below) 

# Wrangle

## Acquire

## Pre-processing

# Exploratory Data Analysis (EDA)

## Hypothesis Testing

# Modeling

# Results & Conclusion

## Next Steps

# Appendix


## Team Members:
### Adam Gomez
<pre><a href="adam.daniel.gomez.787@gmail.com"><img src="https://www.flaticon.com/svg/static/icons/svg/3143/3143198.svg" alt="EMAIL" width="32" height="32"></a>    <a href="https://github.com/adam-gomez"><img src="https://www.flaticon.com/svg/static/icons/svg/25/25231.svg" alt="GitHub" width="32" height="32"></a>    <a href="https://www.linkedin.com/in/adam-gomez/"><img src="https://www.flaticon.com/svg/static/icons/svg/174/174857.svg" alt="LinkedIn" width="32" height="32"></pre>

### Matt Knight
<pre><a href="mattknight.sa@gmail.com"><img src="https://www.flaticon.com/svg/static/icons/svg/3143/3143198.svg" alt="EMAIL" width="32" height="32"></a>    <a href="https://github.com/matt-c-knight"><img src="https://www.flaticon.com/svg/static/icons/svg/25/25231.svg" alt="GitHub" width="32" height="32"></a>    <a href="https://www.linkedin.com/in/matt-knight-9ba764200/"><img src="https://www.flaticon.com/svg/static/icons/svg/174/174857.svg" alt="LinkedIn" width="32" height="32"></a></pre>

## Bibek Mainali
<pre><a href="mailto:bibek.mainali20@gmail.com"><img src="https://www.flaticon.com/svg/static/icons/svg/3143/3143198.svg" alt="LinkedIn" width="32" height="32"></a>    <a href="https://github.com/MainaliB"><img src="https://www.flaticon.com/svg/static/icons/svg/25/25231.svg" alt="GitHub" width="32" height="32"></a>    <a href="https://www.linkedin.com/in/bibek-mainali/"><img src="https://www.flaticon.com/svg/static/icons/svg/174/174857.svg" alt="LinkedIn" width="32" height="32"></a></pre>

## Anthony Rivera Straine
<pre><a href="mailto:anthony.straine@gmail.com"><img src="https://www.flaticon.com/svg/static/icons/svg/3143/3143198.svg" alt="LinkedIn" width="32" height="32"></a>    <a href="https://github.com/datastraine"><img src="https://www.flaticon.com/svg/static/icons/svg/25/25231.svg" alt="LinkedIn" width="32" height="32"></a>    <a href=" https://www.linkedin.com/in/anthony-straine/"><img src="https://www.flaticon.com/svg/static/icons/svg/174/174857.svg" alt="LinkedIn" width="32" height="32"></a></pre>

## Data Dictionary
| Name | Description |
|---|---|
| id  | Unique identifier for a credit account  |
| code_gender  | Whether the account holder is a man or woman  |
| flag_own_car  | Whether the account holder owns a car; 1 for yes 0 for no |
| flag_own_realty  | Whether the account holder owns real-estate; 1 for yes 0 for no  |
| cnt_children  | How many children does the account holder have  |
| amt_income_total  |  Annual Income of the account holder in yuan  |
| name_income_type | What type of job does the account holder have: 'Commercial associate', 'State servant', 'Pensioner', 'Working', 'Student' |
| name_education_type  | What level of education has the account holder obtained:  'Secondary / secondary special', 'Higher education', 'Incomplete higher', 'Lower secondary', 'Academic degree' |
| name_family_status  |  What is marital status of the account holder: 'Married', 'Widow', 'Single / not married', 'Separated', 'Civil marriage' |
| name_housing_type  |  What type of housing does the account holder reside in: 'Municipal apartment', 'House / apartment', 'With parents', 'Rented apartment', 'Office apartment', 'Co-op apartment' |
| age  | How old is the account holder |
| employed_years  |  How long has the account holder been employed at current position |
| flag_mobil |  Does the account holder have a mobile phone; 1 for yes 0 for no |
| flag_work_phone  | Does the account holder have a work phone; 1 for yes 0 for no  |
| flag_phone  | Does the account holder have a phone; 1 for yes 0 for no
| flag_email  | Does the account holder have an e-mail address |
| occupation_type  | What occupation does the account holder have: 'Cooking staff', 'Medicine staff', 'Other', 'Managers', 'High skill tech staff', 'Accountants', 'Laborers', 'Sales staff', 'Drivers', 'Core staff', 'Low-skill Laborers', 'Security staff', 'Secretaries', 'Waiters/barmen staff', 'IT staff','Cleaning staff', 'Private service staff', 'Realty agents','HR staff'  |
| cnt_fam_members  |  How many people are in the account holder's household (children + spouse if applicable) |
| 0-29  | Count of the number of times the account holder was 0-29 days late on making a payment during the 6 month period |
| 30-59  | Count of the number of times the account holder was 30-59 days late on making a payment during the 6 month period |
| 60-89  | Count of the number of times the account holder was 60-89  days late on making a payment during the 6 month period |
| 90-119  | Count of the number of times the account holder was 90-119 days late on making a payment during the 6 month period |
| 120-149  | Count of the number of times the account holder was 120-149  days late on making a payment during the 6 month period |
| paid_off  | Count of the number of times the account holder paid off the account during the 6 month period
| no_debt  | Count of the number of times the account holder was had no debt on the account during the 6 month period |
| months_exist  |  Total number of months the account was present in the data |
| month_01  | The score for month 1 of the period. The scoring system is 0:no debt; 1:paid off; 2:0-29 days late; 3:30-59 days late, 4:90-119 days late; 5:90-119 days late; 6:120-149 days late |
| month_02  | The score for month 2 of the period. The scoring system is 0:no debt; 1:paid off; 2:0-29 days late; 3:30-59 days late, 4:90-119 days late; 5:90-119 days late; 6:120-149 days late |
| month_03  | The score for month 3 of the period. The scoring system is 0:no debt; 1:paid off; 2:0-29 days late; 3:30-59 days late, 4:90-119 days late; 5:90-119 days late; 6:120-149 days late |
| month_04  | The score for month 4 of the period. The scoring system is 0:no debt; 1:paid off; 2:0-29 days late; 3:30-59 days late, 4:90-119 days late; 5:90-119 days late; 6:120-149 days late |
| month_05  | The score for month 5 of the period. The scoring system is 0:no debt; 1:paid off; 2:0-29 days late; 3:30-59 days late, 4:90-119 days late; 5:90-119 days late; 6:120-149 days late |
| month_06  | The score for month 6 of the period. The scoring system is 0:no debt; 1:paid off; 2:0-29 days late; 3:30-59 days late, 4:90-119 days late; 5:90-119 days late; 6:120-149 days late |
| total_score  | The total score for all the months in the period |
| odd_months_score  | The total score for all odd months (1,3,5) in the period |
| last_half_score | The total score for the last half of the period (4-6) |
| first_half_score  | The total score for the first half of the period (1-3) |
| difference_score  | The difference between the last_half and first_half of the period (last_half - first_half); can be a negative value |
| odds_evens_score  | The total score for months 1, 3, 4, and 6|
| beginning_score  |  The total score fpr months 1 and 2 |
| middle_score  | The total score for months 3 and 4 |
| ending_score | The total score for months 5 and 6 |
| spread_score  | The total score for months 2-5|
| alpha_omega_score  | The total score for months 1 and 6|
| beginning_ending_score  | The total score for months 1,2,5, and 6|
| defaulted | Whether or not the account defaulted; 1 for yes and 2 for no|

The following variables are dummy variables created for modeling. For each variable, 1 is yes/true and 0 is no/false

| List of Dummy Variables |
|---|
| name_income_type_commercial_associate  |
| name_income_type_pensioner  |
| name_income_type_state_servant  |
| name_income_type_student  |
| name_income_type_working  |
| name_education_type_academic_degree  |
| name_education_type_higher_education  |
| name_education_type_incomplete_higher  |
| name_education_type_lower_secondary  |
| name_education_type_secondary_/_secondary_special  |
| name_housing_type_co-op_apartment  |
| name_housing_type_house_/_apartment  |
| name_housing_type_municipal_apartment  |
| name_housing_type_office_apartment  |
| name_housing_type_rented_apartment  |
| name_housing_type_with_parents  |
| occupation_type_accountants |
| occupation_type_cleaning_staff  |
| occupation_type_cooking_staff  |
| occupation_type_core_staff  |
| occupation_type_drivers  |
| occupation_type_hr_staff  |
| occupation_type_high_skill_tech_staff  |
| occupation_type_it_staff  |
| occupation_type_laborers  |
| occupation_type_low-skill_laborers  |
| occupation_type_managers  |
| occupation_type_medicine_staff  |
| occupation_type_other  |
| occupation_type_private_service_staff  |
| occupation_type_realty_agents  |
| occupation_type_sales_staff  |
| occupation_type_secretaries  |
| occupation_type_security_staff |  
| occupation_type_waiters/barmen_staff  |
