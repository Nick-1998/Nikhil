#!/usr/bin/env python
# coding: utf-8

# # PROJECT
# 
# 
# 
# 
# 
# 
# ##                 Predicting wheather employee of an organization should get Promotion or Not ?
# 
# 
# 
# 
# 
# 
# 
# 
# 
# Your client is very large MNC Company they have 9 broad verticals organization. One of the problem your client is facing is around identifying the right people for promotion (only for managers position and below) and prepare them in time.
# 
# 
# Currently process , they are following
# 
# 
# 1) They first identify set of employees based on recommendation/past peformance 
# 
# 2) Selected employees go through the training and evaluation program for each vertical. These program are based on he required skill of each vertical.
# 
# 3) At the end of program based on various factors sucha as training peoformance , and employee gets an promotion.

# In[1]:


# Importing libarieries 


# In[2]:


get_ipython().system(' pip install sklearn')


# In[3]:


get_ipython().system(' pip install ipywidgets')


# In[4]:


get_ipython().system('pip install sweetviz')


# In[5]:


get_ipython().system(' pip install imblearn  ')


# # Libary Usages
# 
# 
# ### Matplotlib vs seaborn
# Seborn provides advance staistical operations and graphs 
# 
# ### sweetviz libary 
# It is used for EDA purpose.
# 
# ### Sklearn 
# This is used for Machine Learning Projects
# 
# ### ipywidgets 
# This libary 
# widgets used for making a program interactive
# 
# 
# ### imblearn
#  used for imblanced datasets

# In[6]:


# Lets import libaries 


# In[7]:


import numpy as np 
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

# setting size of figures
plt.rcParams['figure.figsize']=(16,5)
# setting style of plot
plt.style.use('fivethirtyeight')

# For interactivity
import ipywidgets as widgets 
from ipywidgets import interact
from ipywidgets import interact_manual

# for EDA(explorary Data Analysis)
import sweetviz

# for machine learning
import sklearn 
import imblearn 


# In[8]:


# used for selecting style of plot 
# fivethirtyeight is best 
plt.style.available


# In[9]:


# Reading DataSets


# In[10]:


train = pd.read_csv('Workshop Datasets/train.csv')
test = pd.read_csv( 'Workshop Datasets/test.csv')


# In[11]:


# if datsset is not csv
# train = pd.read_excel('Workshop Datasets/train.excel')


# In[12]:


# Show first 5 columns
train.head()


# In[13]:


# show last 5 columns
train.tail()


# In[14]:


test.head()


# In[15]:


# Check the datatype 
train.info()


# In[16]:


train['is_promoted'].value_counts()


# In[17]:


train['is_promoted'].value_counts().plot(kind = 'bar')


# In[18]:


# Let's check the target class Balance
plt.rcParams['figure.figsize']=(15,5)
plt.style.use('fivethirtyeight')

plt.subplot(1,2,1)
sns.countplot(train['is_promoted'],)

# Labelling 
plt.xlabel('Promoted or Not?', fontsize= 10)

# for piechart
plt.subplot(1,2,2)
train['is_promoted'].value_counts().plot(kind = 'pie',explode = [0,0.1], autopct= '%.2f%%',
                                         startangle = 90,
                                         labels= [ 'Non Promoted Employees',
                                                  'Promoted Employees'],shadow = True,pctdistance = 0.5)

plt.axis('off')

plt.suptitle('Target Class Balance', fontsize = 15)
plt.show()


# In[19]:


# Let make a report using sweetviz for complete EDA
my_report = sweetviz.compare([train, 'Train'],[test,'Test'], 'is_promoted')
my_report.show_html('Report.html')


# # Descrtiptive Statistics

# Descriptive Statistics is important step to understand the  Data and take out insights.
# 
# for Categorical columns we check for for stats ,count , frequency and unique elements.

# In[20]:


# let's check  descritptive statistics for numerical columns
train.describe()


# In[21]:


# let's check descriptive statistics for categorical columns
train.describe(include='object')


# In[22]:


# let's make interactive function to check the statistics of these numerical columns at a time 

@interact
def check(column=list(train.select_dtypes('number').columns[1:])):
    print('Maximum Value :', train[column].max())
    print('Minimum Value:',train[column].min())
    print('Mean:{0:2f}'.format(train[column].mean()))
    print('Median:',train[column].median())    
    print('Standard Deviation:{0:2f}'.format(train[column].std()))   


# ###  Treatment of Missing values 

# #### Treatment of missing values is very imp step in ML Model Creation
# 
# ### Types of Missing values
# 1) Missing values Random
# 2)Missing values are not random
# 3) Missing values at completely random
# 
# ### What we can do to impute or treate missing values to make good ML Model?
# 
# Use Business logic to impute the missing values
# 
# use Statistical methods - Mean , Median and Mode
# 
# use ML techniques to impute the misssing values.
# 
# can delete missing values when the missing values is very high.
# 
# ### When to  use Mean , Median and Mode ?
# 
# Use Mean - when we don't have outliers in the datasets for Numerical Variables.
# 
# Use Median - when we  have outliers in the datasets for Numerical Variables.
# 
# Use Mode - when we have cateorgical  variables

# In[23]:


# missing vlues in training datasets 
train.isnull().sum()


# In[24]:


# missing values in training data set

# lets calculate the total missing values in the dataset
train_total = train.isnull().sum()

# lets calculate the percentage of missing values in the dataset
train_percent = ((train.isnull().sum()/train.shape[0])*100).round(2)

# lets calculate the percentage of missing values in the dataset
test_percent = ((test.isnull().sum()/test.shape[0])*100).round(2)

# lets calculate the total missing values in the dataset
test_total = test.isnull().sum()

# Let's check the percentage of missing vlues in training datasets 
train.percent=((train.isnull().sum()/train.shape[0])*100).round(2)

# lets make a dataset consisting of total no. of missing values and percentage of missing values in the dataset
train_missing_data = pd.concat([train_total, train_percent, test_total, test_percent],
                                axis=1, 
                                keys=['Train_Total', 'Train_Percent %','Test_Total', 'Test_Percent %'],
                                sort = True)

# lets check the head
train_missing_data.style.bar(color = ['gold'])


# We can see from the above table, that Only two columns have missing values in Train and Test Dataset both. Also, the Percentage of Missing values is around 4 and 7% in education, and previous_year_rating respectively. So, do not have delete any missing values, we can simply impute the values using Mean, Median, and Mode Values. 
# 
# Lets check the Data Types of these Columns, so that we can impute the missing values in these columns.

# In[25]:


# lets impute the missing values in the Training Data
train['education']= train['education'].fillna(train[ 'education'].mode()[0])
train['previous_year_rating'] = train['previous_year_rating'].fillna(train['previous_year_rating'].mode()[0])

# lets check whether the Null values are still present or not?
print("Number of Missing Values Left in the Training Data :", train.isnull().sum())


# # Outliers Detection using Box Plots
# 
# The presence of outliers in a classification or regression dataset can result in a poor fit and lower predictive modeling performance. Instead, automatic outlier detection methods can be used in the modeling pipeline and compared, just like other data preparation transforms that may be applied to the dataset

# In[26]:


# lets check the columns where we can have outliers 
train.select_dtypes('number').head()


# In[27]:


train['awards_won?'].value_counts()


# In[28]:


# lets check the boxplots for the columns where we suspect for outliers
plt.rcParams['figure.figsize']= (15,5)
plt.style.use('fivethirtyeight')


# Box plot for average training score
plt.subplot(1,2,1)
sns.boxplot(train['avg_training_score'],color = 'red')
plt.xlabel('Average Training Score',fontsize = 12)
plt.ylabel('Range',fontsize = 12)

# Box plot for length of  service 
plt.subplot(1,2,2)
sns.boxplot(train['length_of_service'],color = 'red')
plt.xlabel('Length of Service',fontsize = 12)
plt.ylabel('Range',fontsize=12)

plt.suptitle('Box Plot', fontsize=12)
plt.show()


# # Univariate Analysis
# 
# Univariate analysis is perhaps the simplest form of statistical analysis. Like other forms of statistics, it can be inferential or descriptive. The key fact is that only one variable is involved. Univariate analysis can yield misleading results in cases in which multivariate analysis is more appropriate.
# 
# This is an Essential step, to understand the variables present in the dataset one by one.
# 
# First, we will check the Univariate Analysis for Numerical Columns to check for Outliers by using Box plots.
# 
# Then, we will use Distribution plots to check the distribution of the Numerical Columns in the Dataset.
# 
# After that we will check the Univariate Analysis for Categorical Columns using Pie charts, and Count plots.
# 
# We Use Pie charts, when we have very few categories in the categorical column, and we use count plots we have more categorises in the dataset.

# In[29]:


# let's plot pie charts for the columns where we have few categories
plt.rcParams['figure.figsize']=(12,5)
plt.style.use('fivethirtyeight')

# plotting a pie chart to represent share of Previous year Rating of the Employees
plt.subplot(1,3,1)
labels = ['0','1']
sizes = train['KPIs_met >80%'].value_counts()
colors = plt.cm.Wistia(np.linspace(0, 1, 5))
explode = [0, 0]


plt.pie(sizes, labels = labels, colors = colors, explode = explode, shadow = True, startangle = 90)
plt.title('KPIs Met > 80%', fontsize = 15)

# plotting a pie chart to represent share of Previous year Rating of the Employees
plt.subplot(1,3,2)
labels = ['1','2','3','4', '5']
sizes = train['previous_year_rating'].value_counts()
colors = plt.cm.Wistia(np.linspace(0,1,5))
explode = [0,0,0,0,0.1]

plt.pie(sizes,labels = labels , colors = colors , explode = explode , shadow = True , startangle = 90)
plt.title('Previous year Rating ', fontsize = 20)


# plotting a pie chart to represent share of Previous year Rating of the Employees
plt.subplot(1,3,3)
labels = ['0', '1']
sizes = train['awards_won?'].value_counts()
colors = plt.cm.Wistia(np.linspace(0,1,5))
explode = [0,0.1]

plt.pie(sizes, labels = labels , colors = colors , explode = explode , shadow = True , startangle = 90)
plt.title('Awards Won',fontsize = 20)

plt.legend()
plt.show()


# We, can see that there are some pie charts, we have for representing KPIs, Previous year Ratings, and Awards Won?
# 
# Also, The one Big Pattern is that only some of the employees could reach above 80% of KPIs set.
# Most of the Employees have a very low rating for the previous year, and
# very few employees, probably 2% of them could get awards for their work, which is normal.

# In[30]:


# legend() Demonstration 
# A legend is an area describing the elements of the graph. In the matplotlib library, there’s a function called legend() which is used to Place a legend on the axes.
x = [1,2,4,5,9]
y = [1,4,5,5,6]
plt.plot(x,y)
plt.legend(['single element']) 
plt.show()


# In[31]:


# lets check the distribution of trainings undertaken by employees
plt.rcParams['figure.figsize']=(15,5)
sns.countplot(train['no_of_trainings'], palette = 'viridis')
plt.xlabel( ' ', fontsize = 14)
plt.title('Distribution of trainings taken by Employees')
plt.show()


# The abov Countplot, where are checking the distribution of trainings undertaken by the Employee, It is clearly visible that 80 % of the employees have taken the training only once, and there are negligible no. of employees, who took trainings more than thrice.

# In[32]:


# let's Check the Age of Employees
plt.rcParams['figure.figsize']= (8,4)
plt.hist(train['age'],color = 'black')
plt.title('Distribution of Age among the Employees',fontsize = 15)
plt.xlabel('Age of the Employees')
plt.grid()
plt.show()


# In[33]:


# lets check different Departments
plt.rcParams['figure.figsize']= (12,6)
sns.countplot(y = train['department'], palette = 'cividis', orient = 'v')
plt.xlabel('')
plt.ylabel('Department Name')
plt.title('Distribution of Employees in Different Departments', fontsize = 15)
plt.grid()
plt.show()


# In[34]:


# Let's check the distribution of different regions 
plt.rcParams['figure.figsize'] = (12,15)
sns.countplot(y= train['region'], palette = 'inferno',orient= 'v')
plt.xlabel('')
plt.ylabel('Region')
plt.xticks(rotation = 90)
plt.title('Different regions', fontsize = 15)
plt.grid()
plt.show()


# In[35]:


# let's plot the pie charts of the columns where we have few categories 
plt.rcParams['figure.figsize'] = (15,5)

# plotting a pie chart to represent share of Previous year Rating of the Employees
plt.subplot(1,3,1)
labels = train['education'].value_counts().index
sizes = train[ 'education'].value_counts()
colors = plt.cm.copper(np.linspace(0,1,5))
explode = [0,0,0.1]

plt.pie(sizes , labels = labels , colors = colors , explode = explode , shadow = True , startangle = 90)
plt.title('Education', fontsize = 15)

# plotting a pie chart to represent share of Previous year Rating of the Employees
plt.subplot(1,3,2)
labels = train['gender'].value_counts().index
sizes = train['gender'].value_counts()
colors = plt.cm.copper(np.linspace(0,1,5))
explode = [0,0]

plt.pie(sizes , labels = labels , colors = colors , explode = explode , shadow = True , startangle = 90)
plt.title('Gender', fontsize =  15)

# plotting a pie chart to represent share of Previous year Rating of the Employees
plt.subplot(1,3,3)
labels = train['recruitment_channel'].value_counts().index
sizes = train['recruitment_channel'].value_counts()
colors = plt.cm.copper(np.linspace(0,1,5))
explode = [0,0,0.1]

plt.pie(sizes,labels = labels , colors = colors , explode = explode , shadow = True , startangle = 90)
plt.title('Recruitment Channel')
#Explode 
# The explode argument in pyplot pie decides which part should explode (separate and move a distance from the center). This argument accepts a tuple of numeric values, and each non-zero value represents the distance of that slice from the center of a pie chart. In this Python pie chart example, we exploded medium priority from the center.


# In[36]:


# interactive function for plotting univariate charts for categorical data

plt.rcParams['figure.figsize'] = (15, 4)
@interact_manual
def check(column = list(train.select_dtypes('object').columns),
          palette = ['cividis','copper','spring','Reds','Blues']):
    sns.countplot(train[column], palette = palette)
   
    plt.show()


# ## Bivariate Anlaysis

# Bivariate analysis is one of the simplest forms of quantitative analysis. It involves the analysis of two variables, for the purpose of determining the empirical relationship between them. Bivariate analysis can be helpful in testing simple hypotheses of association.
# 
# #### Types of Bivariate Analysis
# 
# ##### 1)Categorical vs Categorical
# ###### 2)Categorical vs Numerical
# ###### 3)Numerical vs Numerical

# In[37]:


# Compare gender gap in promotion 

plt.rcParams['figure.figsize']= (15,5)
x = pd.crosstab(train['gender'], train['is_promoted'])
colors = plt.cm.Wistia(np.linspace(0,1,5))
x.div(x.sum(1).astype(float),axis=0).plot(kind = 'bar' , stacked = False, color = colors)
plt.title('Effect of Gender Promotion', fontsize = 15)
plt.xlabel('')
plt.show()


# In[38]:


# Compare different departments and Promotion
plt.rcParams['figure.figsize'] = (15,5)
x = pd.crosstab(train['department'],train['is_promoted'])
colors = plt.cm.copper(np.linspace(0,1,3))
x.div(x.sum(1).astype(float),axis=0).plot(kind = 'area', stacked = False , color = colors)
plt.title('Effect of Department on Promotion', fontsize = 15)
plt.xticks(rotation = 20)
plt.xlabel('')
plt.show()


# From above graphical representation it shows there is alomost similar effect on promotion.Wecan sayt hat all departments have similar effect on promotion.It doesn't contribute a lot in making a Machine Learning Model.(Not able to prdeict wheather Employee should get promotion or not) 

# In[39]:


# Checking effect of number of trainings for promotion
plt.rcParams['figure.figsize'] = (15,3)
sns.barplot(train['no_of_trainings'], train['is_promoted'])
plt.title('Effect of Trainings' ,fontsize = 15)
plt.xlabel('No of Trainings', fontsize = 10)
plt.ylabel('Employee promoted or not',fontsize = 10)
plt.show()


# It is clear hat from above graph who takes more  than 5 trainings will not get promoted.

# In[40]:


# Effect of Age on Promotion
plt.rcParams['figure.figsize'] = (15,4)
sns.boxenplot(train['is_promoted'], train['age'], palette = 'PuRd')
plt.title('Effect of Age on Promotion' , fontsize = 15)
plt.xlabel('Employee get promoted or not ?', fontsize = 10)
plt.xlabel('Age of Employee', fontsize = 10)
plt.show()


# In[41]:


# Department vs Average training score
plt.rcParams['figure.figsize'] = (17,6)
sns.boxplot(train['department'], train['avg_training_score'], palette = 'autumn')
plt.title('Average Training score from each department', fontsize = 15)
plt.xlabel('Department', fontsize = 10)
plt.ylabel('Avg training score', fontsize = 10)
plt.show()


# In[42]:


# Let's Make interactive function for Bivariate Analysis
plt.rcParams['figure.figsize'] = (15,5)
@interact_manual
def  bivariate_plot(column1 = list(train.select_dtypes('object').columns),
                    column2 = list(train.select_dtypes('number').columns[1:])):
    sns.boxplot(train[column1],train[column2])


# In[43]:


# lets make an Interactive Function for Bivariate Analysis
plt.rcParams['figure.figsize'] = (15,5)
@interact_manual
def bivariate_plot(column1 = list(train.select_dtypes('object').columns),
                  column2 = list(train.select_dtypes('number').columns[1:])):
    sns.boxenplot(train[column1],train[column2])                  


# # Multivariate Analysis
# 
# ### Multivariate analysis is based on the principles of multivariate statistics, which involves observation and analysis of more than one statistical outcome variable at a time.
# 
# ####  First, we will use the Correlation Heatmap to check the correlation between the Numerical Columns
# #### Check the ppscore or the Predictive Score to check the correlation between all the columns present in the data.
# #### Use Bubble Charts, split Violin plots, Hue with Bivariate Plots.

# In[44]:


# lets check the Heat Map for the Data with respect to correlation.
plt.rcParams['figure.figsize'] = (15,5)
sns.heatmap(train.corr(),annot = True ,linewidth = 0.5,cmap = 'Wistia')
plt.title('Correaltion Heat Map',fontsize = 15)
plt.show()


# From above graph we can say that length of service and age are highly coorelated.
# And also previous year rating and KPI are correlated to each othe

# In[45]:


# Check the relation of recruitment Channel, length of service and Promotions when they won awards ?
plt.rcParams['figure.figsize'] =(16,7)
sns.boxplot(train['recruitment_channel'],
           train['length_of_service'],
            hue = train['is_promoted'],
            palette = 'cividis')
plt.title('Recruitment Channel vs Length of Service')
plt.ylabel('Recruitment Channel')
plt.xlabel('Length of Service')
plt.show()


# In[46]:


train


# In[47]:


# lets check the relation of Departments and Promotions when they won awards ?
plt.rcParams['figure.figsize'] = (16,7)
sns.barplot(train['department'],train[ 'length_of_service'],hue = train[ 'awards_won?'],palette = 'autumn')
plt.title('Chance of Promotion in each department', fontsize = 15)
plt.ylabel('Length of service',fontsize=10)
plt.xlabel('Departments',fontsize = 10)


# # FEATURE ENGINEERING
# 
# Feature engineering is the process of using domain knowledge to extract features from raw data via data mining techniques. These features can be used to improve the performance of machine learning algorithms. Feature engineering can be considered as applied machine learning itself.
# 
# #### There are mutliple ways of performing feature engineering.
# 
# So many people in the Industry consider it the most important step to improve the Model Performance.
# 
# We should always understand the columns well to make some new features using the old existing features.
# 
# ## Let's discuss the ways how we can perform feature engineering
# 
# We can perform Feature Engineering by removing Unnecassary Columns
# 
# Extracting Features from the Date and Time Features.
# 
# Extracting Features from the Categorcial Features.
# 
# Binnning the Numerical and Categorical Features.
# 
# Aggregating Multiple Features together by using simple Arithmetic operations.

# In[48]:


# lets create some extra features from existing features to improve our Model
# creating a metric of sum
train['sum_metric'] = train['awards_won?']+ train['KPIs_met >80%'] + train['previous_year_rating']
test['sum_metric'] = test['awards_won?']+test['KPIs_met >80%'] + test['previous_year_rating']

# Creating total score column
train['total_score'] = train['avg_training_score'] * train['no_of_trainings']
test['total_score'] = test['avg_training_score'] * test['no_of_trainings']


# In[49]:


# lets remove some of the columns which are not very useful for predicting the promotion.

train = train.drop(['recruitment_channel', 'region', 'employee_id'], axis = 1)
test = test.drop(['recruitment_channel', 'region', 'employee_id'], axis = 1)

# lets check the columns in train and test data set after feature engineering
train.columns


# ### Grouping & Filtering Operations
# ###### The grouping operations are the fundamental components of the entity clustering technique. They define what collections of entities and relationships comprise higher-level objects, the entity clusters.

# In[50]:


# let's check the realtionship between KPIs and promotion 
x = pd.crosstab(train['KPIs_met >80%'],train['is_promoted'])
x.style.background_gradient(cmap = 'bone')


# In[51]:


#lets check the relation between the Awards and Promotion
x = pd.crosstab(train['awards_won?'],train['is_promoted'])
x.style.background_gradient(cmap='bone')


# In[52]:


# lets check the no. eployees who won awards from each Department
train[['department', 'awards_won?']].groupby(['department']).agg('sum').sort_values(by = 'awards_won?',
                                                            ascending = False).style.background_gradient('magma')


# In[53]:


# lets group the employees based on their Education
@interact
def group(column = list(train.select_dtypes('object').columns)):
    return train[[column,'is_promoted']].groupby([column]).agg(['count',
                                                              'sum','mean','max']).style.background_gradient(cmap='viridis')


# In[54]:


# lets use the interactive function to make it more reusable
@interact
def group_operations(column = list(train.select_dtypes('object').columns),
                     column2 = list(train.select_dtypes('number').columns)[1:]):
    return train[[column,column2]].groupby([column]).agg('count').style.background_gradient(cmap = 'Wistia')


# In[55]:


# lets get the names of all the employees who have taken trainings more than 7 Times

@interact
def check(column = 'no_of_trainings', x = 5):
    y = train[train['no_of_trainings'] > x]
    return y['is_promoted'].value_counts()


# In[56]:


# lets also check the value counts of the number of trainings employee took.
train['no_of_trainings'].value_counts()


# In[57]:


# lets cap the values of number of trainings after 5, as the chances of promotion is negligible after 5th training 

train['no_of_trainings'] = train['no_of_trainings'].replace((6, 7, 8, 9, 10),(5, 5, 5, 5, 5))

# lets check the values of no. of trainings after capping the values
train['no_of_trainings'].value_counts()


# In[58]:


'''
lets check the no. of employee who did not get an award, did not acheive 80+ KPI, previous_year_rating as 1
and avg_training score is less than 40
but, still got promotion.
''' 

train[(train['KPIs_met >80%'] == 0) & (train['previous_year_rating'] == 1.0) & 
      (train['awards_won?'] == 0) & (train['avg_training_score'] < 60) & (train['is_promoted'] == 1)]


# In[59]:


# lets remove the above two columns as they have a huge negative effect on our training data

# lets check shape of the train data before deleting two rows
print("Before Deleting the above two rows :", train.shape)

train = train.drop(train[(train['KPIs_met >80%'] == 0) & (train['previous_year_rating'] == 1.0) & 
      (train['awards_won?'] == 0) & (train['avg_training_score'] < 60) & (train['is_promoted'] == 1)].index)

# lets check the shape of the train data after deleting the two rows
print("After Deletion of the above two rows :", train.shape)


# In[60]:


# lets check how many of the employees have greater than 30 years of service and still do not get promotion

@interact
def check_promotion(x = 20):
    x = train[(train['length_of_service'] > x)]
    return x['is_promoted'].value_counts()


# In[ ]:





# # Dealing with Cateogrical model
# 
# 
# Dealing with categorical columns how?
# ###### Converting categorical column (objects) to numerical columns interms of  1 0r 0 becuase machine learning model only works with numerical columns.
# ## Various ways to encode cateogrical columns into Numerical Columns:
# I am gonna use label encoder to Department and Gender columns

# In[61]:


# We gonna check first what are the categorical column is present in data
train.select_dtypes('object').head()


# In[62]:


# Counts of Education 
train['education'].value_counts()


# In[63]:


# lets start encoding these categorical columns to convert them into numerical columns

# lets encode the education in their degree of importance 
train['education'] = train['education'].replace(("Master's & above", "Bachelor's", "Below Secondary"),
                                                (3, 2, 1))
test['education'] = test['education'].replace(("Master's & above", "Bachelor's", "Below Secondary"),
                                                (3, 2, 1))

# lets use Label Encoding for Gender and Department to convert them into Numerical
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
train['department'] = le.fit_transform(train['department'])
test['department'] = le.fit_transform(test['department'])
train['gender'] = le.fit_transform(train['gender'])
test['gender'] = le.fit_transform(test['gender'])

# lets check whether we still have any categorical columns left after encoding
print(train.select_dtypes('object').columns)
print(test.select_dtypes('object').columns)


# In[64]:


# Lets check whether we still have any categorical columns left after encoding
print(train.select_dtypes('object').columns)
print(test.select_dtypes('object').columns)
train.head(3)


# # Splitting Data
# 
# ###### This is one of the most Important step to perform Machine Learning Prediction on a Dataset, you have to separate the target and independent Columns.

# In[65]:


# Let's split the target data  from train data

y = train['is_promoted']  # target variable 
x = train.drop(['is_promoted'],axis = 1)
x_test = test

# let's print the shapes of newly formed datasets 
print('Shape of x :', x.shape)
print('Shape of y :', y.shape)
print('Shape of x test:', x_test.shape)


# # Resampling 
# 
# Resampling is the method that consists of drawing repeated samples from the original data samples. The method of Resampling is a nonparametric method of statistical inference.
# 
# #### In this Problem we have noticed that the target column is highly imbalanced, we need to balance the data by using some Statistical Methods.
# 
# ### There are many Statistical Methods we can use for Resampling the Data such as:
# Over Samping
# 
# Cluster based Sampling
# 
# Under Sampling

# In[66]:


# It is very important to resample the data, as the target class is highly imbalanced.
# Here We are going to use Over Sampling Technique to resample the data.
# lets import the SMOTE algorithm to do the same.

from imblearn.over_sampling import SMOTE

x_resample , y_resample = SMOTE().fit_sample(x , y.values.ravel())

print(x_resample.shape)
print(y_resample.shape)


# In[67]:


# Let's check the value counts of target variable 4
print('Before Sampling :')
print(y.value_counts())
print('After sampling :')
y_resample = pd.DataFrame(y_resample)
print(y_resample[0].value_counts())


# In[68]:


# lets create a validation set from the training data so that we can check whether the model that we have created is good enough
# lets import the train_test_split library from sklearn to do that

from sklearn.model_selection import train_test_split

x_train,x_valid , y_train , y_valid = train_test_split(x_resample , y_resample, test_size = 0.2,random_state = 0)

# Let's print shape
print('Shape of x train :',x_train.shape)
print('Shape of y train :',y_train.shape)
print('Shape of x valid tain:', x_valid.shape)
print('Shape of y valid train:',y_valid.shape)
print('Shape of x Test :',x_test.shape)


# # Feature Scaling
# 
# Feature scaling is a method used to normalize the range of independent variables or features of data. In data processing, it is also known as data normalization and is generally performed during the data preprocessing 
# 
# ![image.png](attachttp://localhost:8888/files/Workshop%20Datasets/image.pnghment:image.png)

# In[69]:


# Feature Scaling is important for scaling the datasets - we will use standardization method (commnly used)
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_valid = sc.transform(x_valid)
x_test = sc.transform(x_test)


# # Decisions Tree
# 
# A decision tree is a decision support tool that uses a tree-like model of decisions and their possible consequences, including chance event outcomes, resource costs, and utility. It is one way to display an algorithm that only contains conditional control statements.

# In[70]:


train.head()


# In[71]:


# Lets use Decision Trees to classify the data
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report

model = DecisionTreeClassifier()
model.fit(x_train, y_train)

y_pred = model.predict(x_valid)

print("Training Accuracy :", model.score(x_train, y_train))
print("Testing Accuracy :", model.score(x_valid, y_valid))

cm = confusion_matrix(y_valid, y_pred)
plt.rcParams['figure.figsize'] = (3, 3)
sns.heatmap(cm, annot = True, cmap = 'Wistia', fmt = '.8g')
plt.show()


# In[72]:


import warnings
warnings.filterwarnings('ignore')

from sklearn.feature_selection import RFECV

# The "accuracy" scoring is proportional to the number of correct classifications
model = DecisionTreeClassifier() 
rfecv = RFECV(estimator = model, step = 1, cv = 5, scoring = 'accuracy')
rfecv = rfecv.fit(x_train, y_train)

print('Optimal number of features :', rfecv.n_features_)
x_train = pd.DataFrame(x_train)
print('Best features :', x_train.columns[rfecv.support_])


# In[73]:


# lets take a look at the Classification Report
cr = classification_report(y_valid, y_pred)
print(cr)


# In[74]:


train.describe()


# In[75]:


# lets perform some Real time predictions on top of the Model that we just created using Decision Tree Classifier

# lets check the parameters we have in our Model
'''
department -> The values are from 0 to 8, (Department does not matter a lot for promotion)
education -> The values are from 0 to 3 where Masters-> 3, Btech -> 2, and secondary ed -> 1
gender -> the values are 0 for female, and 1 for male
no_of_trainings -> the values are from 0 to 5
age -> the values are from 20 to 60
previou_year_rating -> The values are from 1 to 5
length_of service -> The values are from 1 to 37
KPIs_met >80% -> 0 for Not Met and 1 for Met
awards_won> -> 0-no, and 1-yes
avg_training_score -> ranges from 40 to 99
sum_metric -> ranges from 1 to 7
total_score -> 40 to 710
'''


# In[76]:


prediction = rfecv.predict(np.array([[2, #department code
                                      3, #masters degree
                                      1, #male
                                      1, #1 training
                                      30, #30 years old
                                      5, #previous year rating
                                      10, #length of service
                                      1, #KPIs met >80%
                                      1, #awards won
                                      95, #avg training score
                                      7, #sum of metric 
                                      700 #total score
                                     ]]))

print("Whether the Employee should get a Promotion : 1-> Promotion, and 0-> No Promotion :", prediction)


# In[ ]:




