import pandas as pd

from src.preparation.activities import get_activities
from src.preparation.ratings import get_ratings


def group_data(user_id):
    df_activities = get_activities(user_id)
    df_ratings = get_ratings(user_id)

    df_joint = df_activities.set_index('date').join(df_ratings.set_index('date'), how='inner')

    # df_joint  = df_joint /df_joint.max().astype(np.float64)
    #
    # df_joint = df_joint.fillna(0)

    X = pd.DataFrame(df_joint.drop(labels=['rating'], axis=1))
    rating_mean = df_joint['rating'].mean()

    y = pd.DataFrame(df_joint['rating'])
    y['rating'] = (y['rating'] > rating_mean).astype(int)

    return X, y

#
# df_day_part_app_type_rating = df_joint[[c for c in df_joint.columns if c.lower()[:8] != 'app_name']]
#
# df_day_part_app_name_rating = df_joint[[c for c in df_joint.columns if c.lower()[:8] != 'app_type']]

# sns.pairplot(df_joint)


# def get_redundant_pairs(df):
#     pairs_to_drop = set()
#     cols = df.columns
#     for i in range(0, df.shape[1]):
#         for j in range(0, i+1):
#             pairs_to_drop.add((cols[i], cols[j]))
#     return pairs_to_drop
#
# def get_top_abs_correlations(df, n=5):
#     au_corr = df.corr().abs().unstack()
#     labels_to_drop = get_redundant_pairs(df)
#     au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
#     return au_corr[0:n]
#
# print("Top Absolute Correlations")
# print(get_top_abs_correlations(df_day_part_app_type_rating, 10))
# print(get_top_abs_correlations(df_day_part_app_name_rating , 10))
#
# pp = sns.pairplot(data=df_joint,
#                   x_vars=df_joint.columns,
#                   y_vars=['rating'])

# pp = sns.pairplot(data=df_joint,
#                   x_vars=[c for c in df_joint.columns if c.startswith('day_part')],
#                   y_vars=[c for c in df_joint.columns if c.startswith('app_type')])
#
#
#
#
# plt.show()
# print(scores)
# print(model.intercept_)
