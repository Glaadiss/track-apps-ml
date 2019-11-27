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
                ) as day_part
from activity
       join application a on activity."applicationId" = a.id
       join "user" u on activity."userId" = u.id
where (activity."to" - activity."from") < INTERVAL '3' hour
  and a.name not like '%clock%'
order by time_in_sec desc
limit 100;
"""

df = sqlio.read_sql_query(sql_activities, conn)
df = pd.concat([df, pd.get_dummies(df["day_part"])], axis=1)

