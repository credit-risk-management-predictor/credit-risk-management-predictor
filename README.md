## Project Title 
## Table of Contents
- [Goal](#goal)
- [Wrangle](#wrangle)
- [Ethical Considerations](#ethical-considerations)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
  - [Hypothesis Testing](#hypothesis-testing)
- [Feature Selection](#feature-selection)
- [Modeling](#modeling)
- [Results & Conclusion](#results--conclusion)
  - [Next Steps](#next-steps)
- [Appendix](#appendix)
  - [Research](#research)
  - [Team Members:](#team-members)
    - [Adam Gomez](#adam-gomez)
    - [Matt Knight](#matt-knight)
    - [Bibek Mainali](#bibek-mainali)
    - [Anthony Rivera Straine](#anthony-rivera-straine)
  - [Data Dictionary](#data-dictionary)

# Goal
Chinese banks are very risk-averse, yet younger generations are more willing to take on debt at similar rates to other developed countries. What are the contributing factors to a credit card holder defaulting on debt? When will an account default 6 months into the future? That is what we aim to find out! We will accomplish this by looking for patterns in a user's credit history and application data, always with an eye to ethical consideration when dealing with demographic data, to predict if they will default 6 months in the future. 

**Bottom Line Up Front (BLUF)**

From all the work contained in this notebook we have determined that...

This project will contain
* A [Jupyter Notebook](https://github.com/credit-risk-management-predictor/credit-risk-management-predictor/blob/main/analysis_and_modeling.ipynb) 
* A [slide deck](https://www.canva.com/design/DAEQaR_b1MA/FKCuserTtnHMcS3sEfH7dg/view?utm_content=DAEQaR_b1MA&utm_campaign=designshare&utm_medium=link&utm_source=sharebutton)
* A 10 minute [presentation]() - needs link 
* A [data dictionary](#data-dictionary) (linked below) 

# Wrangle
All the prep/wrangle work is handled by the wrangle_credit function imported from the [wrangle](https://github.com/credit-risk-management-predictor/credit-risk-management-predictor/blob/main/wrangle.py) module. For an in-depth explanation of how the wrangle_credit function works please see the [How-To Notebook](https://github.com/credit-risk-management-predictor/credit-risk-management-predictor/blob/main/how_to.ipynb).

# Ethical Considerations
When dealing with something as consequential as credit card approvals, it is important to make sure you aren't training your model with data that has been biased against a demographic class due to historical discrimination as this can reinforce cultural biases. Besides, it's also bad for business. Knowing this, we will begin by determining if ***gender*** can be inferred from other information within the application data. If it can, then we should not use those features in our model.

# Exploratory Data Analysis (EDA)
In order to determine whether or not gender can be inferred from our data we have to conduct hypothesis tests. We will cross reference gender with the following features:

> flag_own_car, flag_own_realty, cnt_children, and amt_income_total

We accomplished this by running Two-Sample; Two-Tail T-tests and found that each had a significant statistically relationship with gender. However, while income and gender have a relationship, gender and income may suffer from a third variable problem.  Intuitively, this makes sense as income is also greatly dependent upon occupation. A T-test would show the macro relationship between gender and income, but would not be able to account for other confounding factors. For more details on the gender pay gap, see [The True Story of the Gender Pay Gap](https://freakonomics.com/podcast/the-true-story-of-the-gender-pay-gap-a-new-freakonomics-radio-podcast/) by [Feakonomics Podcast](www.freakonomics.com).


To gather insights into our data we will split our visualizations into two types: continuous variables and categorical variables. Based on our previous testing with gender, we decided not to include `flag_own_car`, `flag_own_realty`, or `cnt_children` in our visualization as these were tightly correlated with gender. 

**Continuous Variables Finding**
* There is a clear difference between the distributions of defaulted and not defaulted account holders for each of the scoring variables and how many months an account existed in the data
* Defaulted accounts skew toward the higher end of the of the scoring system, ergo they have more instances of late payments on the whole.
* With difference score, the accounts that defaulted have more positive values which means that their scores are higher in months 4, 5, and 6 combined than 1, 2, and 3 combined. 
* With difference score, accounts that did not default appear to have more consistent payments across the months as the majority accounts have a score of 0.


**Categorical Variables Findings**
- People with commercial associate type as income type make of 23% of the total pop however, they make 31% of the default pop
- Income type categorized as student do not default at all
- People with higher education make up 28% of the total applicant, however they make 31% of the total defaulting population
- People with incomplete higher education make up 4% of the total applicant population, however, they make up 6% of the defaulted population.
- People with Academic degree and lower secondary degree do not default at all and 
- Those who stay with parents do not default on their debt
- Those with house/apartment are more likely to default
- Those with office apartment do not default on their debt


## Hypothesis Testing
To test for statistical significance we need to run chi squared tests on our categorical variables and Two Sample; Two-Tail T-test on our continuous variables since our target variable, defaulted, is a categorical variable. From these test we failed to reject the null hypothesis on all our test involving categorical variables meaning that we could not prove statistical significance. On the other hand, we could did reject the null hypothesis on all our test involving our continuous variables and thus we can use them to build our models.

# Feature Selection
In order to select our features we used variance inflation factor method to eliminate features that had too much multicollinearity. In other words, we only wanted to model features that were truly independent of one another. This left us with the following features to use in our model
- amt_income_total
- paid_off
- no_debt
- total_score

# Modeling
After scaling our training data we need to handle how imbalanced our training data is before modeling. We will handle through various methods.

* Random Oversampling – Essentially randomly duplicates data from the minority class, in our case defaulted accounts
* Random Undersampling – Chooses random data from the majority class, account that did not default, and removes them from the training data
* Synthetic Minority Oversampling Technique (SMOTE) – Creates synthetic data from the minority class by by selecting examples that are close in the feature space, drawing a line between the examples in the feature space and drawing a new sample at a point along that line.
* Overunder sampling SMOTE : combines the above techniques to produce a training data set. 


Once we have our sampling objects created, we'll use them to fit our training data and then use the following modeling techniques to make predictions on the [training data](#Train-Modeling):

* Logistic Regression
* Stochastic Gradient Descent Classifier
* Ridge Classifier


We will then use the top 5 performing models on our validate data set to test for overfitting. Finally, we will use the top model from our validation against the test and report our results].

# Results & Conclusion
After running through all our models we found that logistic regression using the combination of over and under sampling worked the best as it had the highest accuracy and recall combination of all the model we ran on validate. We now need to run the this model on our test set.

On test, this model performed with a 78% recall rate on defaulted accounts, a 72% recall rate on non-defaulted accounts, and and over all accuracy rating of 72%. It should be noted that all of our models performed really badly in regards to precision for defaulted accounts. The reason for this is that the data is vastly overbalanced toward non-defaulted accounts. This makes sense as people in China are considered super savers and are debt adverse. It was also for this reason and the fact that we want to weigh accurate predictions of accounts who will default that we choose to use Recall.


## Next Steps
We would like to obtain more information in order to determine a customer’s profitability such as the amount of balance a customer carried and their interest rate. This would allow us to more accurately determined a user's risk score and improve the model's ability to hone in on which users would default. We will also use Recursive Feature Elimination to determine which features are useful for modeling and see how that model compares to our current model. 

# Appendix

## Research

* [China Bank Card: No of Issued Credit Card](https://www.ceicdata.com/en/china/bank-card-statistics/bank-card-no-of-issued-credit-card),  Ceic Data
* [COVID-19 and China’s Household Debt Dilemma](https://rhg.com/research/china-household-debt/#:~:text=China's%20credit%20card%20debt%20now,trillion%20yuan%20(%242.5%20trillion)) by Logan Wright and Allen Feng
May 12, 2020, Rhodium Group
* [Despite Rapid Digitisation of Payments in China, Credit Card Usage Will Reach New Heights by 2020](https://www.theasianbanker.com/updates-and-articles/despite-rapid-digitisation-of-payments-in-china,-credit-card-usage-will-reach-new-heights-by-2020) The Asian Banker, February 28, 2019
* [Will China's Credit Card Boom Follow The Well-Worn Path to Bust?](https://www.spglobal.com/en/research-insights/articles/will-china-s-credit-card-boom-follow-the-well-worn-path-to-bust) S&P GLOBAL RATINGS, 4 Jul, 2019

## Team Members:
### Adam Gomez
<img src="https://drive.google.com/file/d/1ci84cNRGOwql3rpIDEz59XBNIV6zBgap/view?usp=sharing" alt="EMAIL" width="32" height="32">
<pre><a href="adam.daniel.gomez.787@gmail.com"><img src="https://www.flaticon.com/svg/static/icons/svg/3143/3143198.svg" alt="EMAIL" width="32" height="32"></a>    <a href="https://github.com/adam-gomez"><img src="https://www.flaticon.com/svg/static/icons/svg/25/25231.svg" alt="GitHub" width="32" height="32"></a>    <a href="https://www.linkedin.com/in/adam-gomez/"><img src="https://www.flaticon.com/svg/static/icons/svg/174/174857.svg" alt="LinkedIn" width="32" height="32"></pre>

### Matt Knight
<pre><a href="mattknight.sa@gmail.com"><img src="https://www.flaticon.com/svg/static/icons/svg/3143/3143198.svg" alt="EMAIL" width="32" height="32"></a>    <a href="https://github.com/matt-c-knight"><img src="https://www.flaticon.com/svg/static/icons/svg/25/25231.svg" alt="GitHub" width="32" height="32"></a>    <a href="https://www.linkedin.com/in/matt-knight-9ba764200/"><img src="https://www.flaticon.com/svg/static/icons/svg/174/174857.svg" alt="LinkedIn" width="32" height="32"></a></pre>

### Bibek Mainali
<pre><a href="mailto:bibek.mainali20@gmail.com"><img src="https://www.flaticon.com/svg/static/icons/svg/3143/3143198.svg" alt="LinkedIn" width="32" height="32"></a>    <a href="https://github.com/MainaliB"><img src="https://www.flaticon.com/svg/static/icons/svg/25/25231.svg" alt="GitHub" width="32" height="32"></a>    <a href="https://www.linkedin.com/in/bibek-mainali/"><img src="https://www.flaticon.com/svg/static/icons/svg/174/174857.svg" alt="LinkedIn" width="32" height="32"></a></pre>

### Anthony Rivera Straine
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