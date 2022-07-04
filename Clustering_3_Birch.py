import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import Birch
import numpy as np

df = pd.read_csv("Normalized_Political_7Topics.csv", sep=";", usecols = ['Length_of_UserName', 'Followers_to_Friends_Ratio', 'Posting_Rate'
                        , 'Location', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                        , 'Likes', 'Likes_Rate', 'Has_Extended_Profile', 'Friends'
                        , 'Followers', 'Statuses', 'Topic 1', 'Topic 2', 'Topic 3','Topic 4', 'Topic 5', 'Topic 6', 'Topic 7'])

# define the model
birch_model = Birch(n_clusters=4, threshold=0.000000025, branching_factor=4)
arr = df.to_numpy()
# train the model
birch_model.fit(arr)
labels = birch_model.predict(arr)

mydict = {i: np.where(birch_model.labels_ == i)[0] for i in range(birch_model.n_clusters)}
# Transform this dictionary into list (if you need a list as result)
dictlist = []
dictlistcount = []
for key, value in mydict.items():
    temp = [key,value]
    tempnum = len(value)
    dictlist.append(temp)
    dictlistcount.append(tempnum)

print(dictlist) #print the sybil nodes in each cluster
print(dictlistcount) #print the count of nodes in each cluster

plt.scatter(arr[:, 13], arr[:, 14], c=labels)
plt.show()