import pandas as pd
import pandas.io.sql as sqlio
from config import conn


def get_ratings(user_id):
    sql_ratings = """
    select distinct r.rating, r."userId" as user_id, (
      Case
        WHEN cast(r.date::timestamp as time) + INTERVAL '1' hour < INTERVAL '19' hour THEN cast((r.date - INTERVAL '23' hour)::timestamp as date)
        ELSE cast((r.date + INTERVAL '1' hour)::timestamp as date)
      END
      ) as date
    from rating r
    -- where r."userId" in (select u."userId" from rating u group by 1 having count(u."userId") >= 10)
    where r."userId" = {user_id}
    order by date desc;
    """.format(user_id=user_id)

    df = sqlio.read_sql_query(sql_ratings, conn)
    df = df.drop(labels=["user_id"], axis=1)

    return df
