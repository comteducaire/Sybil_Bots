from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import numpy as np



#TSNE Clustering
# Loading dataset
df = pd.read_csv("Normalized_Political_7Topics.csv", sep=";", usecols = ['Length_of_UserName', 'Followers_to_Friends_Ratio', 'Posting_Rate'
                        , 'Location', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                        , 'Likes', 'Likes_Rate', 'Has_Extended_Profile', 'Friends',
                     'Followers', 'Statuses', 'Topic 1', 'Topic 2', 'Topic 3','Topic 4', 'Topic 5', 'Topic 6', 'Topic 7'])


dbscan = DBSCAN()

# Fitting
dbscan.fit(df.values)

# Transoring Using PCA
pca = PCA(n_components=4).fit(df.values)
pca_2d = pca.transform(df.values)

# Plot based on Class
for i in range(0, pca_2d.shape[0]):
    if dbscan.labels_[i] == 0:
        c1 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='red', marker='+')
    elif dbscan.labels_[i] == 1:
        c2 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='g', marker='x')
    elif dbscan.labels_[i] == 2:
        c3 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='b', marker='*')
    elif dbscan.labels_[i] == 3:
        c4 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='black', marker='o')
    elif dbscan.labels_[i] == -1:
        c5 = plt.scatter(pca_2d[i, 0], pca_2d[i, 1], c='yellow', marker='*')


mydict = {i: np.where(dbscan.labels_ == i)[0] for i in range(4)}
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

plt.legend([c1, c2, c3, c4, c5], ['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Noise'])
plt.title('DBSCAN finds 4 clusters and Noise')
plt.show()