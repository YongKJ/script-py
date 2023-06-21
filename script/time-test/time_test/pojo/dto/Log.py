class Log:

    def __init__(self, class_name, method_name, param_name, value):
        self._className = class_name or ""
        self._methodName = method_name or ""
        self._paramName = param_name or ""
        self._value = value or ""

    @staticmethod
    def of(class_name, method_name, param_name, value):
        return Log(class_name, method_name, param_name, value)

    @property
    def className(self):
        return self._className

    @className.setter
    def className(self, value):
        self._className = value

    @property
    def methodName(self):
        return self._methodName

    @methodName.setter
    def methodName(self, value):
        self._methodName = value

    @property
    def paramName(self):
        return self._paramName

    @paramName.setter
    def paramName(self, value):
        self._paramName = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
