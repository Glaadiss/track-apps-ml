import pandas as pd
import pandas.io.sql as sqlio
from config import conn

sql_activities = """
select distinct r.rating, r."userId", (
  Case
    WHEN cast(r.date::timestamp as time) + INTERVAL '1' hour < INTERVAL '19' hour THEN cast((r.date - INTERVAL '23' hour)::timestamp as date)
    ELSE cast((r.date + INTERVAL '1' hour)::timestamp as date)
  END
  ) as date
from rating r
where r."userId" in (select u."userId" from rating u group by 1 having count(u."userId") >= 10)
order by date desc;
"""



df = sqlio.read_sql_query(sql_activities, conn)
df = pd.concat([df, pd.get_dummies(df["day_part"]), pd.get_dummies(df["app_type"])], axis=1)

df
