import re
import os
import sys

from ...pojo.dto.Log import Log
from ...pojo.po.Modules import Modules
from ...util.FileUtil import FileUtil
from ...util.GenUtil import GenUtil
from ...util.LogUtil import LogUtil
from ...util.DataUtil import DataUtil
from ...deploy.pojo.po.Script import Script
from ...deploy.pojo.po.SourceCode import SourceCode
from ...deploy.pojo.po.Dependency import Dependency
from ...deploy.pojo.dto.BuildConfig import BuildConfig


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
        # pattern = re.compile("from\\s(\\S+)\\simport.*")
        pattern = re.compile("\nimport\\s(\\S*)")
        content = FileUtil.read(path)
        for match in pattern.finditer(content):
            LogUtil.loggerLine(Log.of("GenUtil", "test8", "match.group(1)", match.group(1)))
        # match = pattern.findall(content)
        # match = pattern.match(content)
        # match = pattern.search(content)
        LogUtil.loggerLine(Log.of("GenUtil", "test8", "all", pattern.findall(content)))
        LogUtil.loggerLine(Log.of("GenUtil", "test8", "keys", Modules.__dict__))
        dicts = dir(Modules)
        LogUtil.loggerLine(Log.of("GenUtil", "test8", "dicts", dicts))
        dicts = DataUtil.getProps(Modules)
        LogUtil.loggerLine(Log.of("GenUtil", "test8", "dicts", dicts))
        LogUtil.loggerLine(Log.of("GenUtil", "test8", "attr", getattr(Modules, dicts[0])))

    def test9(self):
        dictCodes = SourceCode.get()
        for key in dictCodes:
            code = dictCodes[key]
            if code.className != "GenUtil": continue
            LogUtil.loggerLine(Log.of("GenUtil", "test9", "path", code.path))
            LogUtil.loggerLine(Log.of("GenUtil", "test9", "pycPath", code.pycPath))
            LogUtil.loggerLine(Log.of("GenUtil", "test9", "cachePycPath", code.cachePycPath))
            LogUtil.loggerLine(Log.of("GenUtil", "test9", "targetPath", code.targetPath))
            LogUtil.loggerLine(Log.of("GenUtil", "test9", "scriptPath", code.scriptPath))
            print("---------------------------------------------------------------")
        LogUtil.loggerLine(Log.of("GenUtil", "test9", "len", len(dictCodes)))

    def test10(self):
        appletDir = FileUtil.getAbsPath(False, "src", "script_py", "applet", "demo")
        scripts = filter(lambda file: file.endswith(".py"), FileUtil.list(appletDir))
        for script in scripts:
            LogUtil.loggerLine(Log.of("GenUtil", "test10", "script", script))

    def test11(self):
        scripts = Script.get()
        for script in scripts:
            LogUtil.loggerLine(Log.of("GenUtil", "test10", "codePaths.length", len(script.codePaths)))

    def test12(self):
        tomlpath = FileUtil.getAbsPath(False, "pyproject.toml")
        content = FileUtil.read(tomlpath)
        pattern = re.compile("\\[tool.poetry.dependencies\\]([\\s\\S]+?)\r\n\r\n")
        for match in pattern.finditer(content):
            LogUtil.loggerLine(Log.of("GenUtil", "test12", "match.group(1)", match.group(1)))
            tempPattern = re.compile("(\\S+)\\s=\\s\"(\\S+)\"")
            for tempMatch in tempPattern.finditer(match.group(1)):
                LogUtil.loggerLine(Log.of("GenUtil", "test12", "tempMatch.group(1)", tempMatch.group(1)))
                LogUtil.loggerLine(Log.of("GenUtil", "test12", "tempMatch.group(2)", tempMatch.group(2)))

    def test13(self):
        dependencies = Dependency.get()
        for dependency in dependencies:
            LogUtil.loggerLine(Log.of("GenUtil", "test13", "dependency.name", dependency.name))

    def test14(self):
        regStr = "name\\s=\\s\"(\\S+)\""
        tomlpath = FileUtil.getAbsPath(False, "pyproject.toml")
        FileUtil.modContent(tomlpath, regStr, "script-py-test")

    def test15(self):
        regStr = "(\\S+)\\s=\\s\"script_py\\S+\""
        tomlpath = FileUtil.getAbsPath(False, "pyproject.toml")
        FileUtil.modContent(tomlpath, regStr, "demo")

    def test16(self):
        regStr = "(from[\\s\\S]+Demo)"
        value = "from .deploy.service.BuildScriptService import BuildScriptService"
        appPath = FileUtil.getAbsPath(False, "src", "script_py", "Application.py")
        FileUtil.modContent(appPath, regStr, value)

    def test17(self):
        regStr = "\\s+(\\S+)\\.run\\(\\)"
        value = "BuildScriptService"
        appPath = FileUtil.getAbsPath(False, "src", "script_py", "Application.py")
        FileUtil.modContent(appPath, regStr, value)

    def test18(self):
        regStr = "(\\S+\\s=\\s\"script_py\\S+\")"
        tomlpath = FileUtil.getAbsPath(False, "pyproject.toml")
        FileUtil.modContent(tomlpath, regStr, "demo")

    def test19(self):
        config = BuildConfig.get()
        LogUtil.loggerLine(Log.of("Demo", "test19", "config", config))

    def test20(self):
        regStr = "(\r\n.*ApplicationTest.*)\r"
        path = FileUtil.getAbsPath(False, "src", "script-py.py")
        # FileUtil.modContent(path, ".*(#\\s).*", "")
        FileUtil.modFile(path, regStr, "", True)
        FileUtil.modFile(path, "(#\\s)", "", True)
        FileUtil.modFile(path, "(script_py)", "build-script-service", True)

    def test21(self):
        LogUtil.loggerLine(Log.of("Demo", "test20", "__name__", Demo.__name__))

    @staticmethod
    def run():
        demo = Demo()
        demo.test21()
        # demo.test20()
        # demo.test19()
        # demo.test18()
        # demo.test17()
        # demo.test16()
        # demo.test15()
        # demo.test14()
        # demo.test13()
        # demo.test12()
        # demo.test11()
        # demo.test10()
        # demo.test9()
        # demo.test8()
        # demo.test7()
        # demo.test6()
        # demo.test5()
        # demo.test4()
        # demo.test3()
        # demo.test2()
        # demo.test1()
        # demo.test()
