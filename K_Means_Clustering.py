from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
import numpy as np
import time
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}

def plot_clusters(data, algorithm, args, kwds):
    start_time = time.time()
    labels = algorithm(*args, **kwds).fit_predict(data)
    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    plt.scatter(data.T[0], data.T[1], c='black', **plot_kwds)
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(True)
    frame.axes.get_yaxis().set_visible(False)
    end_time = time.time()
    plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=24)
    plt.text(-0.5, 0.7, 'Clustering took {:.2f} s'.format(end_time - start_time), fontsize=14)


input_data = pd.read_csv("Normalized_Political_7Topics.csv", sep=";", usecols = ['Length_of_UserName', 'Followers_to_Friends_Ratio', 'Posting_Rate'
                        , 'Location', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                        , 'Likes', 'Likes_Rate', 'Has_Extended_Profile', 'Friends',
                     'Followers', 'Statuses', 'Topic 1', 'Topic 2', 'Topic 3','Topic 4', 'Topic 5', 'Topic 6', 'Topic 7'])

#dataframe = pd.DataFrame()
# initialize KMeans object specifying the number of desired clusters
kmeans = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
    n_clusters=4 , n_init=10,
    random_state=None, tol=0.0001, verbose=0)

#kmeans = KMeans(n_clusters = 3, random_state = 1).fit(dataframe)


#learning the clustering from the input data
label = kmeans.fit(input_data.values)
#dataframe['kmean'] = label

mydict = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}

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


print("***************Cluster_Centers***************")
print(kmeans.cluster_centers_)
print("END***************Cluster_Centers***************")

# output the labels for the input data
print(kmeans.labels_)

# predict the classification for given data sample
predicted_class = kmeans.fit_predict(input_data.values)

print(predicted_class)

# plotting the results
#clusters = kmeans.n_clusters
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], s = 100)
plt.show()
# plt.scatter(clusters[:,0], clusters[0,:], s = 100)
# plt.show()

# plot_clusters(input_data, cluster.KMeans, (), {'n_clusters':4})
# plt.show()