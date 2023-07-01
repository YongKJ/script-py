class DataUtil:

    @staticmethod
    def getProps(clazz):
        return [p for p in dir(clazz) if not p.startswith("__")]

    @staticmethod
    def getValue(clazz, key):
        try:
            props = DataUtil.getProps(clazz)
            for prop in props:
                if prop in key:
                    return getattr(clazz, prop)
            return None
        except Exception as e:
            print(key)
            print(e)
