from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import sklearn.cluster as cluster

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




input_data = pd.read_csv("Normalized_Political_2.csv", sep=";", usecols = ['Length_of_UserName', 'Followers_to_Friends_Ratio', 'Posting_Rate'
                        , 'Location', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                        , 'Likes', 'Likes_Rate', 'Has_Extended_Profile', 'Friends',
                     'Followers', 'Statuses', 'Topic 1 (American Presidents)', 'Topic 2 (Covid economics)', 'Topic 3 (Women in Politics)'])

# initialize KMeans object specifying the number of desired clusters
kmeans = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
    n_clusters=4 , n_init=10,
    random_state=None, tol=0.0001, verbose=0)

# learning the clustering from the input data
label = kmeans.fit(input_data.values)

print("***************Cluster_Centers***************")
print(kmeans.cluster_centers_)
print("END***************Cluster_Centers***************")

# output the labels for the input data
print(kmeans.labels_)

# predict the classification for given data sample
predicted_class = kmeans.fit_predict(input_data.values)

print(predicted_class)
#predicted_class = kmeans.predict([[1, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 500]])


# plt.scatter(input_data.values[:, 0], input_data.values[:, 1], c=predicted_class, s=50, cmap='viridis')
#
# centers = kmeans.cluster_centers_
# plt.scatter(centers[:, 0], centers[:, 1], s=200,);

# plotting the results
centers = kmeans.cluster_centers_
#plt.scatter(centers[:, 0], centers[:, 1], s = 40)
#plt.show()

plot_clusters(input_data, cluster.KMeans, (), {'n_clusters':4})


plot_clusters(input_data, cluster.DBSCAN, (), {'eps':0.025})