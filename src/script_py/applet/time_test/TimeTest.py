import datetime

from ...pojo.dto.Log import Log
from ...util.GenUtil import GenUtil
from ...util.LogUtil import LogUtil


class TimeTest:

    def __init__(self):
        self.time = GenUtil.getValue("time")

    def apply(self):
        nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        LogUtil.loggerLine(Log.of("TimeTest", "apply", "time", self.time))
        LogUtil.loggerLine(Log.of("TimeTest", "apply", "nowTime", nowTime))

    @staticmethod
    def run():
        TimeTest().apply()
