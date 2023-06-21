from ..config.Global import Global


class LogUtil:

    @staticmethod
    def loggerLine(log):
        if not Global.LOG_ENABLE:
            return
        print("[" + log.className + "] " + log.methodName + " -> " + log.paramName + ": ", end="")
        print(log.value)

    @staticmethod
    def logger(log):
        if not Global.LOG_ENABLE:
            return
        print("[" + log.className + "] " + log.methodName + " -> " + log.paramName + ": ", end="")
        print(log.value, end="")
