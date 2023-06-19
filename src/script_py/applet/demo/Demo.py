import re
import os
import sys

from ...pojo.dto.Log import Log
from ...util.FileUtil import FileUtil
from ...util.GenUtil import GenUtil
from ...util.LogUtil import LogUtil


class Demo:

    def __init__(self):
        self.msg = GenUtil.getValue("msg")

    def test(self):
        GenUtil.writeConfig({"msg": "世界， 你好！"})
        LogUtil.loggerLine(Log.of("Demo", "test", "msg", self.msg))

    def test1(self):
        path = sys.executable
        LogUtil.loggerLine(Log.of("Demo", "test1", "path", path))
        path = __file__
        LogUtil.loggerLine(Log.of("Demo", "test1", "path", path))
        path = os.path.dirname(__file__)
        LogUtil.loggerLine(Log.of("Demo", "test1", "path", path))
        path = sys.argv[0]
        LogUtil.loggerLine(Log.of("Demo", "test1", "path", path))
        path = os.path.realpath(sys.argv[0])
        LogUtil.loggerLine(Log.of("Demo", "test1", "path", path))

    def test2(self):
        path = FileUtil.appDir(True)
        LogUtil.loggerLine(Log.of("Demo", "test2", "path", path))
        path = FileUtil.appDir(False)
        LogUtil.loggerLine(Log.of("Demo", "test2", "path", path))
        path = FileUtil.getAbsPath(False, "src", "test")
        LogUtil.loggerLine(Log.of("Demo", "test2", "path", path))

    def test3(self):
        data1 = GenUtil.toLine("FileUtil.py")
        LogUtil.loggerLine(Log.of("Demo", "test3", "data1", data1))
        data2 = GenUtil.toHump("file-util.py")
        LogUtil.loggerLine(Log.of("Demo", "test3", "data2", data2))
        GenUtil.getValue("msg")

    def test4(self):
        LogUtil.loggerLine(Log.of("GenUtil", "getValue", "co_name", sys._getframe().f_back.f_code.co_name))
        LogUtil.loggerLine(Log.of("GenUtil", "getValue", "f_code", sys._getframe().f_back.f_code))
        LogUtil.loggerLine(Log.of("GenUtil", "getValue", "co_varnames", sys._getframe().f_back.f_code.co_varnames))
        LogUtil.loggerLine(Log.of("GenUtil", "getValue", "co_filename", sys._getframe().f_back.f_code.co_filename))
        LogUtil.loggerLine(Log.of("GenUtil", "getValue", "co_code", sys._getframe().f_back.f_code.co_code))
        LogUtil.loggerLine(Log.of("GenUtil", "getValue", "__name__", sys._getframe().f_back.f_code.__class__.__name__))
        LogUtil.loggerLine(Log.of("GenUtil", "getValue", "dir", dir(sys._getframe().f_back.f_code)))

    def test5(self):
        # path = "D:\\Document\\MyCodes\\Github\\script-py\\src\\script_py"
        path = FileUtil.getAbsPath(False, "src", "script_py")
        lstFile = FileUtil.list(path)
        for file in lstFile:
            print(file)
        LogUtil.loggerLine(Log.of("GenUtil", "getValue", "lstFile", lstFile))
        LogUtil.loggerLine(Log.of("GenUtil", "getValue", "type", type(lstFile)))

    def test6(self):
        path = FileUtil.getAbsPath(False, "pyproject.toml")
        FileUtil.modContent(path, "authors = (.*)", "YongKJ")

    def test7(self):
        regStr = "(\r\n\\s+<dependency>[\\s\\S]*?</dependency>)"
        path = "D:\Document\MyCodes\Github\script-java\pom.xml"
        value = "\r\n        <dependency>\r\n            <groupId>org.apache.httpcomponents</groupId>\r\n            <artifactId>httpclient</artifactId>\r\n            <version>4.5.49</version>\r\n        </dependency>"
        FileUtil.modFile(path, regStr, value)
        # FileUtil.modFile(path, regStr, value, True)

    def test8(self):
        path = "D:\\Document\\MyCodes\\Github\\script-py\\src\\script_py\\applet\\demo\\Demo.py"
        pattern = re.compile("from.*import\\s(\\S+)")
        content = FileUtil.read(path)
        for match in pattern.finditer(content):
            LogUtil.loggerLine(Log.of("GenUtil", "test8", "match.group(1)", match.group(1)))
        # match = pattern.findall(content)
        # match = pattern.match(content)
        # match = pattern.search(content)
        # LogUtil.loggerLine(Log.of("GenUtil", "test8", "match", match))

    @staticmethod
    def run():
        demo = Demo()
        demo.test8()
        # demo.test7()
        # demo.test6()
        # demo.test5()
        # demo.test4()
        # demo.test3()
        # demo.test2()
        # demo.test1()
        # demo.test()
