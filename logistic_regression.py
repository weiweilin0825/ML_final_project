# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
# %% Set Environment & Import Function
# ============================================================================
# Hide Warnings
import warnings
warnings.filterwarnings("ignore")

# Automatically Clear Var. & Console
from IPython import get_ipython
get_ipython().magic("clear")
get_ipython().magic("reset -f")

import numpy as np
import pandas as pd
from math import sqrt, exp, pi
from matplotlib import pyplot as plt

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

# %% Preprocessing
# ============================================================================
# Change Column "Name" to "Full Name"
train = train.rename(columns = {"Name" : "Full Name"})

# Add "Family = SibSp + Parch Column"
train.insert(8, "Family", train["SibSp"] + train["Parch"] + 1) # 在船上的家族人數(有包含自己)

# %%% Fare
# 在還沒填補Pclass值之前先算各Pclass的Fare平均，避免因Pclass填補誤差造成Fare平均的誤差
Fare_Pclass1_mean = train.dropna(axis = 0, how = "all", subset = ["Fare"]).dropna(axis = 0, how = "all", subset = ["Pclass"])[train["Pclass"] == 1]["Fare"].mean()
Fare_Pclass2_mean = train.dropna(axis = 0, how = "all", subset = ["Fare"]).dropna(axis = 0, how = "all", subset = ["Pclass"])[train["Pclass"] == 2]["Fare"].mean()
Fare_Pclass3_mean = train.dropna(axis = 0, how = "all", subset = ["Fare"]).dropna(axis = 0, how = "all", subset = ["Pclass"])[train["Pclass"] == 3]["Fare"].mean()

train["Fare"].fillna(-1, inplace = True)
for i in range(len(train)):
    if train["Fare"][i] == -1:
        if train["Pclass"][i] == 1:
            train["Fare"][i] = Fare_Pclass1_mean
        if train["Pclass"][i] == 2:
            train["Fare"][i] = Fare_Pclass2_mean
        if train["Pclass"][i] == 3:
            train["Fare"][i] = Fare_Pclass3_mean

# %%% Pclass
# Fill Pclass Method 1
"""
# replace Nan in Cabin row with 0
train["Cabin"].fillna(0, inplace=True)
test["Cabin"].fillna(0, inplace=True)
train["Pclass"].fillna(0, inplace=True)
test["Pclass"].fillna(0, inplace=True)
# change the data form of Cabin to 0 and 1
train.loc[train["Cabin"] == 0, "Cabin"] = 0
train.loc[train["Cabin"] != 0, "Cabin"] = 1
test.loc[test["Cabin"] == 0, "Cabin"] = 0
test.loc[test["Cabin"] != 0, "Cabin"] = 1
# find the mean Fare of different Pclass
fare_mean = train.groupby("Pclass")["Fare"].mean()
fare_mean = pd.DataFrame({"Pclass": fare_mean.index, "Fare": fare_mean.values})
class1_fare_mean = fare_mean["Fare"][1]
class2_fare_mean = fare_mean["Fare"][2]
class3_fare_mean = fare_mean["Fare"][3]
# fill the Nan of Pclass based on Fare difference with mean of fare of different class
for i in range(len(train)):
    if train["Pclass"][i] == 0:
        fare_difference1 = abs(train["Fare"][i]-class1_fare_mean)
        fare_difference2 = abs(train["Fare"][i]-class2_fare_mean)
        fare_difference3 = abs(train["Fare"][i]-class3_fare_mean)
        if min(fare_difference1, fare_difference2, fare_difference3) == fare_difference1:
            train["Pclass"][i] = 1
        if min(fare_difference1, fare_difference2, fare_difference3) == fare_difference2:
            train["Pclass"][i] = 2
        if min(fare_difference1, fare_difference2, fare_difference3) == fare_difference3:
            train["Pclass"][i] = 3
for i in range(len(test)):
    if test["Pclass"][i] == 0:
        fare_difference1 = abs(test["Fare"][i]-class1_fare_mean)
        fare_difference2 = abs(test["Fare"][i]-class2_fare_mean)
        fare_difference3 = abs(test["Fare"][i]-class3_fare_mean)
        if min(fare_difference1, fare_difference2, fare_difference3) == fare_difference1:
            test["Pclass"][i] = 1
        if min(fare_difference1, fare_difference2, fare_difference3) == fare_difference2:
            test["Pclass"][i] = 2
        if min(fare_difference1, fare_difference2, fare_difference3) == fare_difference3:
            test["Pclass"][i] = 3
"""

# Fill Pclass Method 2
# Age Distribution of Pclass
plt.bar(train[train["Pclass"] == 1]["Age"].value_counts().index, train[train["Pclass"] == 1]["Age"].value_counts())
plt.title("Age Distribution of Pclass 1")
plt.xlabel("Age")
plt.ylabel("Number of people")
plt.xlim([0, 100])
plt.ylim([0, 25])
plt.show()
plt.bar(train[train["Pclass"] == 2]["Age"].value_counts().index, train[train["Pclass"] == 2]["Age"].value_counts())
plt.title("Age Distribution of Pclass 2")
plt.xlabel("Age")
plt.ylabel("Number of people")
plt.xlim([0, 100])
plt.ylim([0, 25])
plt.show()
plt.bar(train[train["Pclass"] == 3]["Age"].value_counts().index, train[train["Pclass"] == 3]["Age"].value_counts())
plt.title("Age Distribution of Pclass 3")
plt.xlabel("Age")
plt.ylabel("Number of people")
plt.xlim([0, 100])
plt.ylim([0, 25])
plt.show()

# Max Fare of Pclass 2 & 3
max_fare_pclass_2and3 = train[train["Pclass"] > 1].max(skipna = True)["Fare"]

# Replace Nan in Cabin Row With -1
train["Pclass"].fillna(-1, inplace = True)

# Fill Pclass
for i in range(len(train)):
    if train["Pclass"][i] == -1: # Refer to Cabin
        if "T" in str(train["Cabin"][i]):
            train["Pclass"][i] = 1
        if "A" in str(train["Cabin"][i]):
            train["Pclass"][i] = 1
        if "B" in str(train["Cabin"][i]):
            train["Pclass"][i] = 1
        if "C" in str(train["Cabin"][i]):
            train["Pclass"][i] = 1
        if "D" in str(train["Cabin"][i]):
            train["Pclass"][i] = 1
        if "E" in str(train["Cabin"][i]):
            train["Pclass"][i] = 1
    if train["Pclass"][i] == -1: # Refer to Fare
        if train["Pclass"][i] > max_fare_pclass_2and3:
            train["Pclass"][i] = 1
    if train["Pclass"][i] == -1: # Refer to Embarked
        if train["Embarked"][i] == "Q":
            train["Pclass"][i] = 3

# %%% Name
# Split Last Name, Title and First Name
train.insert(4, "Last Name", train["Full Name"].str.split(", ", expand = True).iloc[:, 0])
train.insert(5, "Title", train["Full Name"].str.split(", ", expand = True).iloc[:, 1].str.split(".", expand = True).iloc[:, 0])
train.insert(6, "First Name", train["Full Name"].str.split(", ", expand = True).iloc[:, 1].str.split(".", expand = True).iloc[:, 1].map(lambda x: str(x)[1:]))
"""
print(train["Title"].value_counts()) # number of people of each title
"""

# %%% Age
"""
# Age Distribution of "Mr" title
plt.bar(train[train["Title"] == "Mr"]["Age"].value_counts().index, train[train["Title"] == "Mr"]["Age"].value_counts())
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of people")
plt.show()
"""

Age_total_mean = train.dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Mr_mean = train[train["Title"] == "Mr"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Miss_mean = train[train["Title"] == "Miss"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Mrs_mean = train[train["Title"] == "Mrs"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Master_mean = train[train["Title"] == "Master"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Dr_mean = train[train["Title"] == "Dr"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Rev_mean = train[train["Title"] == "Rev"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Col_mean = train[train["Title"] == "Col"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Major_mean = train[train["Title"] == "Major"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Jonkheer_mean = train[train["Title"] == "Jonkheer"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Mlle_mean = train[train["Title"] == "Mlle"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Mme_mean = train[train["Title"] == "Mme"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Capt_mean = train[train["Title"] == "Capt"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()
Age_Sir_mean = train[train["Title"] == "Sir"].dropna(axis = 0, how = "all", subset = ["Age"])["Age"].mean()

# Fill Nan Data With Mean of Certain Catag.
train["Age"].fillna(-1, inplace = True)
for i in range(len(train)):
    if train["Age"][i] == -1:
        if train["Title"][i] == "Mr":
            train["Age"][i] = Age_Mr_mean
        if train["Title"][i] == "Miss":
            train["Age"][i] = Age_Miss_mean
        if train["Title"][i] == "Mrs":
            train["Age"][i] = Age_Mrs_mean
        if train["Title"][i] == "Master":
            train["Age"][i] = Age_Master_mean
        if train["Title"][i] == "Dr":
            train["Age"][i] = Age_Dr_mean
        if train["Title"][i] == "Rev":
            train["Age"][i] = Age_Rev_mean
        if train["Title"][i] == "Col":
            train["Age"][i] = Age_Col_mean
        if train["Title"][i] == "Major":
            train["Age"][i] = Age_Major_mean
        if train["Title"][i] == "Jonkheer":
            train["Age"][i] = Age_Jonkheer_mean
        if train["Title"][i] == "Mlle":
            train["Age"][i] = Age_Mlle_mean
        if train["Title"][i] == "Mme":
            train["Age"][i] = Age_Mme_mean
        if train["Title"][i] == "Ms":
            train["Age"][i] = Age_Miss_mean
        if train["Title"][i] == "Capt":
            train["Age"][i] = Age_Capt_mean
        if train["Title"][i] == "Sir":
            train["Age"][i] = Age_Sir_mean
        else:
            train["Age"][i] = Age_total_mean

# %%% Embarked
"""
test["Embarked"].fillna(-1, inplace=True)
for i in range(len(train)):
    if test["Embarked"][i] == -1:
        test["Embarked"][i] = "S"
"""

# %% To Do List
# ============================================================================
# Test也要填值
# 把所有填值都合併在一個for迴圈內
def set_Cabin_type(df):
    df.loc[ (df.Cabin.notnull()), 'Cabin' ] = "Yes"
    df.loc[ (df.Cabin.isnull()), 'Cabin' ] = "No"
    return df

train=set_Cabin_type(train)

d_Sex=pd.get_dummies(train['Sex'],prefix='Sex')
d_Pclass=pd.get_dummies(train['Pclass'],prefix='Pclass')
d_Embarked=pd.get_dummies(train['Embarked'],prefix='Embarked')
d_Cabin=pd.get_dummies(train['Cabin'],prefix='Cabin')
train=pd.concat([train,d_Sex,d_Pclass],axis=1)
train.drop(['Full Name','Last Name','Title','First Name','Sex','Pclass','Embarked','Cabin','Ticket','Family','Embarked','Cabin'],axis=1,inplace=True)
print(train)

#Normalize Age and Fare
train_normalize_max_age=((train['Age']-train['Age'].mean())/train['Age'].std()).max()
train_normalize_max_fare=((train['Fare']-train['Fare'].mean())/train['Fare'].std()).max()

test['Age'] = ((test['Age']-train['Age'].mean())/train['Age'].std())/train_normalize_max_age
test['Fare'] = ((test['Fare']-train['Fare'].mean())/train['Fare'].std())/train_normalize_max_fare

train['Age'] = ((train['Age']-train['Age'].mean())/train['Age'].std())/train_normalize_max_age
train['Fare'] = ((train['Fare']-train['Fare'].mean())/train['Fare'].std())/train_normalize_max_fare


#Split Training set value to train_of_train and train_of_test
train_of_train=train.sample(frac=0.7)
test_of_train=train.drop(train_of_train.index)
#print (train_of_train,'\n',test_of_train)

y_train_of_train=train_of_train.loc[:,['Survived']]
y_test_of_train=test_of_train.loc[:,['Survived']]       #get the survived array
y_train=train.loc[:,['Survived']]

test_of_train.drop(['PassengerId','Survived'], axis=1,inplace=True)
train_of_train.drop(['PassengerId','Survived'], axis=1,inplace=True)
train.drop(['PassengerId','Survived'], axis=1,inplace=True)             #drop the unused data of training
passenger=test.loc[:,['PassengerId']]
test.drop(['PassengerId'], axis=1,inplace=True)

print(train)
#change to array to compute
y_train_of_train=y_train_of_train.to_numpy()
y_test_of_train=y_test_of_train.to_numpy()
y_train=y_train.to_numpy()

train_of_train=train_of_train.to_numpy()
test_of_train=test_of_train.to_numpy()

test=test.to_numpy()
train=train.to_numpy()

passenger=passenger.to_numpy()

#reshape y
y_train_of_train=np.squeeze(y_train_of_train)
y_test_of_train=np.squeeze(y_test_of_train)
y_train=np.squeeze(y_train)

# ============================================================================
# %% Logistic Regression
# ============================================================================
def sigmoid(input):    
    output = 1 / (1 + np.exp(-input))
    return output


def optimize(x, y,learning_rate,iterations,parameters): 
    size = x.shape[0]
    weight = parameters["weight"] 
    bias = parameters["bias"]
    for i in range(iterations): 
        sigma = sigmoid(np.dot(x, weight) + bias)
        loss = (-1/size )*np.sum(y * np.log(sigma) + (1 - y) * np.log(1-sigma))
        dW = 1/size * np.dot(x.T, (sigma - y))
        db = 1/size * np.sum(sigma - y)
        weight -= learning_rate * dW
        bias -= learning_rate * db 
        if (i+1)%100==0:
            print('=== Iteration: %d ===' %(i+1))
            print('Training loss: %.4f' %loss)
    
    parameters["weight"] = weight
    parameters["bias"] = bias
    return parameters

init_parameters = {} 
init_parameters["weight"] = np.zeros(train.shape[1])
init_parameters["bias"] = 0

def train_process(x, y, learning_rate,iterations):
    parameters_out = optimize(x, y, learning_rate, iterations ,init_parameters)
    return parameters_out

# ============================================================================
# %% Training and Testing
# ============================================================================
parameters_out = train_process(train, y_train, learning_rate = 0.1, iterations = 100000)
output_values=np.dot(train,parameters_out["weight"])+parameters_out["bias"]
prediction=np.zeros(len(output_values))

for i in range(len(output_values)):
    if sigmoid(output_values[i])>=1/2:
        prediction[i]=1
    else:
        prediction[i]=0
count=0
for i in range(len(output_values)):
    if y_train[i]==prediction[i]:
        count+=1
accuracy=count/len(output_values)
print("The Accuracy is", accuracy*100,"%")