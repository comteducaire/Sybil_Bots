from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import TSNE
import numpy as np


#TSNE Clustering
# Loading dataset
df = pd.read_csv("Normalized_Political_2.csv", sep=";", usecols = ['Length_of_UserName', 'Followers_to_Friends_Ratio', 'Posting_Rate'
                        , 'Location', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                        , 'Likes', 'Likes_Rate', 'Has_Extended_Profile', 'Friends',
                     'Followers', 'Statuses', 'Topic 1 (American Presidents)', 'Topic 2 (Covid economics)', 'Topic 3 (Women in Politics)'])


# Available methods on dataset
print(dir(df))

model = TSNE(learning_rate=100)

# Fitting Model
transformed = model.fit_transform(df.values)
# label = {0: 'red', 1: 'blue', 2: 'green'}

# Plotting 2d t-Sne
x_axis = transformed[:, 0]
y_axis = transformed[:, 1]

# color1=(0.69411766529083252, 0.3490196168422699, 0.15686275064945221, 1.0)
# color2=(0.65098041296005249, 0.80784314870834351, 0.89019608497619629, 1.0)
#
# colormap = np.array([color1,color2])

plt.scatter(x_axis, y_axis, s=20)
plt.show()