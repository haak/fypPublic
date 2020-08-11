from lenskit import batch, topn, util
from lenskit import crossfold as xf
from lenskit.algorithms import Recommender, als, user_knn as knn
from lenskit import topn
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances


def find_n_neighbours(user_id):
    df = pd.read_csv("/home/alex/Documents/fyp/datasets/df/df.csv")

    sim_user_30_u = df
    neighbours = sim_user_30_u.iloc[user_id]
    # print(neighbours)
    # print(type(neighbours))
    return neighbours


def write_neighbours(n):
    Ratings = pd.read_csv("/home/alex/Documents/fyp/datasets/ml-latest-small/ratings.csv")
    Mean = Ratings.groupby(by="userId", as_index=False)['rating'].mean()
    Rating_avg = pd.merge(Ratings, Mean, on='userId')

    Rating_avg['adg_rating'] = Rating_avg['rating_x'] - Rating_avg['rating_y']
    final = pd.pivot_table(Rating_avg, values='adg_rating', index='userId', columns='movieId')
    final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)

    b = cosine_similarity(final_user)
    np.fill_diagonal(b, 0)
    similarity_with_user = pd.DataFrame(b, index=final_user.index)
    similarity_with_user.columns = final_user.index
    df = similarity_with_user

    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False).iloc[:n].index,
                                      index=['top{}'.format(i) for i in range(1, n + 1)]), axis=1)

    df.to_csv('/home/alex/Documents/fyp/datasets/df/df.csv',encoding='utf-8', index=False)
    return


if __name__ == '__main__':
    # write_neighbours(30)
    neighbours = find_n_neighbours(1,1)
    # print(neighbours)