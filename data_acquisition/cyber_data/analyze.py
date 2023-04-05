'''
Author: Qi7
Date: 2023-04-04 19:53:35
LastEditors: aaronli-uga ql61608@uga.edu
LastEditTime: 2023-04-05 00:22:28
Description: 
'''
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('cyber_final.csv')


#%%
# Drop the unrelated protocols
drop_protocol = ['BJNP', 'BROWSER', 'DB-LSP-DISC']
df = df[df.Protocol.isin(drop_protocol) == False]

class_encoder = LabelEncoder()
scaler = MinMaxScaler()
df['class_1'] = class_encoder.fit_transform(df['class_1'])
df['class_2'] = class_encoder.fit_transform(df['class_2'])
df_protocol = pd.get_dummies(df['Protocol'])
df_clean = df[['Count', 'Traffic', 'class_1', 'class_2']]
df_clean = pd.concat([df_protocol, df_clean], axis=1)

binary_class1 = df['class_1'].astype('category')
label_color = ['green' if i==1 else 'Red' for i in binary_class1]

# dataframe for PCA : PCA can not have 'categorical' features
df_tmp = df_clean.drop(['class_1', 'class_2'], axis=1)
# Mean normalization
normalized_df = (df_tmp - df_tmp.mean()) / df_tmp.std()

# PCA
# pca = PCA(n_components=2)
# pca.fit(normalized_df)
# df_pca = pca.transform(normalized_df)
# df_pca = pd.DataFrame(df_pca)
# df_pca.columns = ['PCA component 1', 'PCA component 2']
# df_pca.plot.scatter(x='PCA component 1', y='PCA component 2', marker='o',
#         alpha=0.6, # opacity
#         color=label_color,
#         title="red: attack, green: normal" )
# plt.show()
# %%
features = normalized_df.to_numpy()
targets =  df_clean['class_2'].to_numpy()

# split the training and test data
train_features, test_features, train_targets, test_targets = train_test_split(
        features, targets,
        train_size=0.8,
        test_size=0.2,
        # random but same for all run, also accuracy depends on the
        # selection of data e.g. if we put 10 then accuracy will be 1.0
        # in this example
        random_state=23,
        # keep same proportion of 'target' in test and target data
        stratify=targets
    )

# use LogisticRegression
classifier = RandomForestClassifier()
# training using 'training data'
classifier.fit(train_features, train_targets) # fit the model for training data

# predict the 'target' for 'training data'
prediction_training_targets = classifier.predict(train_features)
self_accuracy = accuracy_score(train_targets, prediction_training_targets)
print("Accuracy for training data (self accuracy):", self_accuracy)

# predict the 'target' for 'test data'
prediction_test_targets = classifier.predict(test_features)
test_accuracy = accuracy_score(test_targets, prediction_test_targets)
print("Accuracy for test data:", test_accuracy)
# %%
