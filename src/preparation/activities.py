import pandas as pd
import pandas.io.sql as sqlio
from config import conn


sql_activities = """
select distinct extract('epoch' from (activity."to" - activity."from")::interval) as time_in_sec,
                "from" + INTERVAL '1' hour as from,
                "to" + INTERVAL '1' hour as to,
                a.name,
                u.email,
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
order by time_in_sec desc
limit 100;
"""

df = sqlio.read_sql_query(sql_activities, conn)
df = pd.concat([df, pd.get_dummies(df["day_part"]), pd.get_dummies(df["app_type"])], axis=1)

df
