import pandas as pd
import pandas.io.sql as sqlio
from config import conn
from enum import Enum


class ColumnType(Enum):
    app_type = 1
    day_part = 2
    app_name = 3

def get_activities(user_id):
    sql_activities = """
    select distinct extract('epoch' from (activity."to" - activity."from")::interval) as time_in_sec,
                    cast("from"::timestamp as date) as date, 
                    "from" + INTERVAL '1' hour as from,
                    "to" + INTERVAL '1' hour as to,
                    a.name,
                    u."id" as user_id,
                    (
                      CASE
                        WHEN cast("from"::timestamp as time) + INTERVAL '1' hour < INTERVAL '5' hour THEN 'early_morning'
                        WHEN cast("from"::timestamp as time) + INTERVAL '1' hour < INTERVAL '9' hour THEN 'morning'
                        WHEN cast("from"::timestamp as time) + INTERVAL '1' hour < INTERVAL '12' hour THEN 'noon'
                        WHEN cast("from"::timestamp as time) + INTERVAL '1' hour < INTERVAL '17' hour THEN 'afternoon'
                        WHEN cast("from"::timestamp as time) + INTERVAL '1' hour < INTERVAL '21' hour THEN 'evening'
                        ELSE 'night'
                      END
                    ) as day_part,
                    (
                      CASE
                        WHEN a.name in ('com.facebook.katana', 'com.instagram.android', 'com.snapchat.android', 'com.linkedin.android')   THEN 'social'
                        WHEN a.name in ('com.skype.raider', 'com.facebook.orca', 'com.android.mms', 'com.whatsapp', 'com.samsung.android.messaging', 'com.samsung.android.contacts', 'com.android.contacts', 'com.google.android.apps.messaging', 'com.Slack', 'com.microsoft.teams')   THEN 'communication'
                        WHEN a.name in ('com.sec.android.app.launcher', 'com.huawei.android.launcher', 'com.android.systemui') THEN 'launcher'
                        WHEN a.name in ('com.google.android.youtube', 'com.netflix.mediaclient', 'tv.twitch.android.app') THEN 'video'
                        WHEN a.name in ('com.android.chrome', 'org.mozilla.firefox', 'com.sec.android.app.sbrowser') THEN 'browser'
                        WHEN a.name in ('com.google.android.gm', 'com.microsoft.office.outlook') THEN 'mail'
                        WHEN a.name in ('com.samsung.android.incallui', 'com.android.dialer') THEN 'call'
                        WHEN a.name in ('net.wordbit.enpl', 'org.coursera.android', 'com.linkedin.android', 'com.ichi2.anki', 'com.google.android.apps.docs', 'com.udemy.android', 'com.google.android.apps.translate') THEN 'learning'
                        WHEN a.name in ('com.supercell.brawlstars', 'com.roblox.client', 'com.mojang.minecraftpe', 'com.mmarcel.cnb2', 'com.jetstartgames.chess', 'com.nianticlabs.pokemongo') THEN 'game'
                        WHEN a.name in ('com.spotify.music', 'com.apple.android.music') THEN 'music'
                        ELSE 'other'
                      END
                    ) as app_type
    from activity
           join application a on activity."applicationId" = a.id
           join "user" u on activity."userId" = u.id
    where (activity."to" - activity."from") < INTERVAL '3' hour
      and a.name not like '%clock%'
      and u."id" = {user_id}
    """.format(user_id=user_id)

    df = sqlio.read_sql_query(sql_activities, conn)

    day_part_data = pd.get_dummies(df["day_part"], prefix=ColumnType.day_part.name)

    app_type_data = pd.get_dummies(df["app_type"], prefix=ColumnType.app_type.name)

    name_data = pd.get_dummies(df["name"], prefix=ColumnType.app_name.name)

    df = df.drop(labels=["day_part", "app_type", "name", "from", "to", "user_id"], axis=1)

    df = pd.concat([df, day_part_data, app_type_data, name_data], axis=1)

    df_data = df.drop(labels=['time_in_sec', 'date'], axis=1)

    df_time = df['time_in_sec']

    df_date = df['date']

    df = pd.concat([df_date, df_time, df_data.mul(df_time, axis=0)], axis=1)

    df = df.groupby(['date']).sum().reset_index()

    return df

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
