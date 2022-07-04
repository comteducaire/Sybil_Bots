import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean

# Function to plot initial data points.
def plot_data_before(data):
    x, y = data.iloc[:, 0], data.iloc[:, 1]
    plt.scatter(x, y, color="m", marker="o", s=30)

    plt.xlabel('X axis', size=20)
    plt.ylabel('Y axis', size=20)

    plt.show()

# Function to find points that are closest to centriods
def closestCentriods(data, ini_cent):
    K = np.shape(ini_cent)[0]

    m = np.shape(data)[0]
    idx = np.zeros((m, 1), dtype=np.float32)

    cent_vals = np.zeros((m, K))
    # Subtract each data row with each centroid value and get the different
    # Find sqaured sum of different of eache each row
    for i in range(K):
        Diff = data - ini_cent[i, :]
        cent_vals[:, i] = np.sum(Diff ** 2, axis=1)

    # Return index of minimum value column wise.
    idx = cent_vals.argmin(axis=1)
    return idx


# Function to find/update centriod, mean of a cluster
# def avg(data, x_indx, axis):
#   for i in range(x_indx)
#     data[i,:] = mean()
#   pass


def calcCentriods(data, idx, K):
    n = np.shape(data)[1]
    centriods = np.zeros((K, n))
    for i in range(K):
        with warnings.catch_warnings():
          x_indx = [wx for wx, val in enumerate(idx) if val == i]
          centriods[i, :] = np.mean(data[x_indx, :], axis = 0)
        #print('mean:', np.mean(data[x_indx, :], axis= 0))
    return centriods


# Function to find euclidean distance between two points
def findDistance(point1, point2):
    eucDis = 0
    for i in range(len(point1)):
        eucDis = eucDis + (point1[i] - point2[i]) ** 2

    return eucDis ** 0.5


# Function to calcualte Dunn Index
def calcDunnIndex(points, cluster):
    # points -- all data points
    # cluster -- cluster centroids

    numer = float('inf')
    for c in cluster:  # for each cluster
        for t in cluster:  # for each cluster
            # print(t, c)
            if (t == c).all(): continue  # if same cluster, ignore
            ndis = findDistance(t, c)
            # print('Numerator', numerator, ndis)
            numer = min(numer, ndis)  # find distance between centroids

    denom = 0
    for c in cluster:  # for each cluster
        for p in points:  # for each point
            for t in points:  # for each point
                if (t == p).all(): continue  # if same point, ignore
                ddis = findDistance(t, p)
                #    print('Denominator', denominator, ddis)
                denom = max(denom, ddis)

    return numer / denom


# Function to iterate centriod search,
# until we have found optimum result
def applyKmeans(data, initial_centroids, max_iters):
    dataArr = np.array(data)

    m1, n1 = dataArr.shape
    m2, n2 = initial_centroids.shape

    K = np.shape(initial_centroids)[0]
    centriods = initial_centroids
    previous_centriods = centriods

    for i in range(max_iters):
        print('\n\n K-Means iteration number {}'.format(i + 1))

        # Find the closest centriods
        idx = closestCentriods(dataArr, centriods)
        centriods = calcCentriods(dataArr, idx, K)

        print('\n\n The centriods are')
        print('\n The value of first centriod : {} \n The value of second centriod {}\n\n'.format(centriods[0, :],
                                                                                                  centriods[1, :]))

        plot_data_after(data, centriods)

        points = dataArr.reshape(m1 * n1, 1)
        centers = centriods.reshape(m2 * n2, 1)

        print("\n\nCalculate Dunn's Index")
        print("-----------------------\n\n")
        print('The value of Dunns Index is ', calcDunnIndex(dataArr, centriods))
        print("-----------------------\n\n")
        # Break when centriod doesn't change
        if np.equal(previous_centriods, centriods).all():
            break
        else:
            previous_centriods = centriods


# Scatter centiods along with initial data set.
def plot_data_after(data, centriods):
    x, y = data.iloc[:, 0], data.iloc[:, 1]
    cx, cy = centriods[:, 0], centriods[:, 1]
    plt.scatter(x, y, color="m", marker="o", s=30)

    plt.xlabel('X axis', size=20)
    plt.ylabel('Y axis', size=20)

    plt.scatter(cx, cy, color="b", marker="*", s=300)

    plt.show()


# Main function to fetch data set,
# Apply K-means and find Dunns Index
def main():
    input_data = pd.read_csv("Normalized_Political_2.csv", sep=";", usecols = ['Length_of_UserName', 'Followers_to_Friends_Ratio', 'Posting_Rate'
                        , 'Location', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                        , 'Likes', 'Likes_Rate', 'Has_Extended_Profile', 'Friends',
                     'Followers', 'Statuses', 'Topic 1 (American Presidents)', 'Topic 2 (Covid economics)', 'Topic 3 (Women in Politics)'])

    data = input_data[['Statuses', 'Topic 1 (American Presidents)']]
                       # , 'Location', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                        #, 'Likes', 'Likes_Rate', 'Has_Extended_Profile', 'Friends',
                     #'Followers', 'Statuses', 'Topic 1 (American Presidents)', 'Topic 2 (Covid economics)', 'Topic 3 (Women in Politics)']]

    print("\n\n Initial draw points")
    plot_data_before(data)
    initial_centroids = np.array([[1, 3], [0, 4]])

    #     dataArr = np.array(data)
    #     idx = closestCentriods(dataArr, initial_centroids)

    #     K = np.shape(initial_centroids)[0]
    #     centriods = calcCentriods(dataArr, idx, K)

    #     plot_data_after (data, centriods)

    applyKmeans(data, initial_centroids, 1)


if __name__ == '__main__':
    main()