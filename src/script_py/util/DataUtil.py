class DataUtil:

    @staticmethod
    def getProps(clazz):
        return [p for p in dir(clazz) if not p.startswith("__")]

    @staticmethod
    def getValue(clazz, key):
        try:
            return getattr(clazz, key)
        except Exception as e:
            print(key)
            print(e)
