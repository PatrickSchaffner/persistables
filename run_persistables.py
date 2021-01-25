from datetime import datetime, timedelta
import pickle

import numpy as np
import pandas as pd

from persistables import Persistable, Manager

pd.set_option('display.expand_frame_repr', False)

n_obs = 20
frequency = timedelta(minutes=5)
now = datetime.now()
to_date = now - timedelta(minutes=now.minute % 5, seconds=now.second, microseconds=now.microsecond)
from_date = to_date - n_obs * frequency
timeline = [from_date + i * frequency for i in range(n_obs)]
print(timeline)

manager = Manager(Persistable, database='sqlite:///test.db', echo=True)

with manager.open_session() as session:
    p_cached = session.query(Persistable) \
        .filter(Persistable.date.in_(timeline)) \
        .order_by(Persistable.date)\
        .all()
    print(f"Loaded {len(p_cached)} cached persistables.")
    if len(p_cached) > 0:
        p_cached[0].update_data()

missing_dates = sorted(list(set(timeline) - {p.date for p in p_cached}))
p_new = [Persistable(date=d, data=np.random.randint(0, d.day, size=(2, d.month)))
         for d in missing_dates]
print(f"Persist {len(p_new)} new persistables.")

with manager.open_session(auto_commit=True) as session:
    session.add_all(p_new)
    p_all = sorted([*p_cached, *p_new], key=lambda p: p.date)
    print(p_all)

with manager.open_connection() as conn:
    tbl = pd.read_sql_table(Persistable.__tablename__, conn)
    print(tbl)
    print(pickle.loads(tbl.data[tbl.shape[0]-1]))
