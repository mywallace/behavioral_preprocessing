#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:43:23 2020

@author: papitto
"""

import statsmodels.formula.api as smf
import statsmodels.api as sm
import pandas as pd 
import matplotlib.pyplot as plt
from pingouin import linear_regression

input_file = '/home/raid2/papitto/Desktop/PsychoPy/MRep_2020_backup/MRep_training_backup/data/results.csv'
dataset = pd.read_csv(input_file)

dataset = dataset[["Subj_tr", "OT3_spec_Tot", "OT3_sub_Tot", "OT3_rule_Tot", "OT3_gen_Tot", "RT3_spec_Tot", "RT3_sub_Tot", "RT3_rule_Tot", "RT3_gen_Tot" ]]

####################
#### ONSET TIME ####
####  REACTION  ####
####################

dataset_spec = dataset[["Subj_tr", "OT3_spec_Tot", "RT3_spec_Tot"]]
dataset_spec = dataset_spec.rename(columns={"OT3_spec_Tot": "OT","RT3_spec_Tot": "RT" })
dataset_sub = dataset[["Subj_tr", "OT3_sub_Tot", "RT3_sub_Tot"]]
dataset_sub = dataset_sub.rename(columns={"OT3_sub_Tot": "OT", "RT3_sub_Tot": "RT"})
dataset_rule = dataset[["Subj_tr", "OT3_rule_Tot", "RT3_rule_Tot"]]
dataset_rule = dataset_rule.rename(columns={"OT3_rule_Tot": "OT","RT3_rule_Tot": "RT"})
dataset_gen = dataset[["Subj_tr", "OT3_gen_Tot", "RT3_gen_Tot"]]
dataset_gen = dataset_gen.rename(columns={"OT3_gen_Tot": "OT","RT3_gen_Tot": "RT"})


for i, row in dataset_spec.iterrows():
    dataset_spec.at[i, 'condition'] = "spec"
for i, row in dataset_sub.iterrows():
    dataset_sub.at[i, 'condition'] = "sub"
for i, row in dataset_rule.iterrows():
    dataset_rule.at[i, 'condition'] = "rule"
for i, row in dataset_gen.iterrows():
    dataset_gen.at[i, 'condition'] = "gen"

frames = [dataset_spec, dataset_sub, dataset_rule, dataset_gen] 
result_df = pd.concat(frames)    
# so far it was identical to the previous script

# now create dummy variables. Linear regression
# methods usually work with numeric variables, so we convert 
# categorical variables to numeric one
result_df['Spec']=result_df.condition.map({'spec':1,'sub':0,'rule':0, "gen": 0})
result_df['Sub']=result_df.condition.map({'sub':1,'spec':0,'rule':0, "gen": 0})
result_df['Rule']=result_df.condition.map({'rule':1,'spec':0,'sub':0, "gen": 0})
result_df['Gen']=result_df.condition.map({'gen':1,'spec':0,'rule':0, "sub": 0})

result_df['condition_num']=result_df.condition.map({'gen':4,'spec':1,'rule':3, "sub": 2})

###################
####  FIT THE  ####
####  MODEL   ####
###################

# define the regression values to fit
y = result_df["OT"]
x = result_df["condition"]

# this formula might be actually able to create dummy variables by its own
model = smf.ols(formula="OT ~ C(condition)", data=result_df).fit()

# really not sure if it is working though
model.summary()

fig, ax = plt.subplots()
fig = sm.graphics.plot_fit(model, 0, ax=ax)


###################
####  PLOT THE  ###
####  MEANS   ####
###################

# create the means for the Onset Times (OT)
OT_gen_mean = dataset["OT3_gen_Tot"].mean()
OT_spec_mean = dataset["OT3_spec_Tot"].mean()
OT_sub_mean = dataset["OT3_sub_Tot"].mean()
OT_rule_mean = dataset["OT3_rule_Tot"].mean()

# plot the data in three different plots   
data = {'1_Spec': OT_spec_mean, '2_Sub': OT_sub_mean, '3_Rule': OT_rule_mean, '4_Gen': OT_gen_mean}
names = ['1_Spec', '2_Sub', '3_Rule','4_Gen']
values = [OT_spec_mean, OT_sub_mean, OT_rule_mean, OT_gen_mean]
fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
axs[0].bar(names, values)
axs[1].scatter(names, values)
axs[2].plot(names, values)
fig.suptitle('Categorical Plotting')

###################
####  pingouin  ###
###################

y = result_df["OT"]
x = result_df.drop(["OT", "condition", "condition_num", "Subj_tr", "Gen", "RT"], axis=1)
lm = linear_regression(x, y)
lm.round(2)

