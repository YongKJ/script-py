from ...util.LogUtil import LogUtil
from ...pojo.dto.Log import Log


class Demo:

    def __init__(self):
        self.msg = ""

    def test(self):
        self.msg = "Hello world!"
        LogUtil.logger(Log.of("Demo", "test", "msg", self.msg))

    @staticmethod
    def run():
        Demo().test()
