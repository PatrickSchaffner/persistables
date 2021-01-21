
class Manager(object):
    
    def __init__(self, database, classes, echo=False):
        self._engine = create_engine(database, echo=echo)
        self._metadata = self._merge_metadata(classes)
        self._session = sessionmaker(bind=engine)
        
    
    @staticmethod
    def _merge_metadata(classes):
        meta = {cls.metadata for cls in classes}
        tables = {*list(cls.tables.items()) for cls in classes}
        merged = MetaData()
        for (name, tbl) in tables:
            tbl.to_metadata(merged)
        return merged
