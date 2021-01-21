from datetime import datetime, timedelta

import numpy as np

from persistables import Persistable, create_base


Base = create_base()


class SomeReport(Base, Persistable):
    pass


with Base.open(filename='test.db', echo=True) as session:
    r_all = session.query(SomeReport).all()
    if len(r_all) == 0:
        d = {'x': np.random.randint(0, 100, size=(20,7)),
             'y': None,
             'z': 'a text!',
             'w': timedelta(hours=3)
        }
        r_new = SomeReport(id=0, datetime=datetime.now(), data=d)
        session.add(r_new)
        session.commit()
    else:
        for r in r_all:
            print("Report #{id:d} ({date:s}): \n{data:s}\n".format(
                    id=r.id,
                    date=r.datetime.strftime('%Y-%m-%d'),
                    data=str(r.data)
            ))
