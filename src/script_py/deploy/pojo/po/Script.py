from ....deploy.pojo.po.SourceCode import SourceCode
from ....util.FileUtil import FileUtil
from ....util.GenUtil import GenUtil


class Script:
    dictCodes = SourceCode.get()

    def __init__(self, pyName="", className="", packageName="", projectName="", lineProjectName="", scriptProjectName="",
                 targetProjectName="", targetLaunchPath="", targetTomlPath="", targetBuildPath="", targetConfigPath="",
                 targetDistPath="", pyPath="", yamlConfig="", scriptConfig="", scriptPath="", consoleScripts="",
                 codePaths=set(), modules=set()):
        self._pyName = pyName
        self._pyPath = pyPath
        self._className = className
        self._packageName = packageName
        self._projectName = projectName
        self._lineProjectName = lineProjectName
        self._scriptProjectName = scriptProjectName
        self._targetProjectName = targetProjectName
        self._targetConfigPath = targetConfigPath
        self._targetBuildPath = targetBuildPath
        self._targetLaunchPath = targetLaunchPath
        self._targetTomlPath = targetTomlPath
        self._targetDistPath = targetDistPath
        self._yamlConfig = yamlConfig
        self._scriptPath = scriptPath
        self._scriptConfig = scriptConfig
        self._consoleScripts = consoleScripts
        self._codePaths = codePaths
        self._modules = modules

    @staticmethod
    def of(pyName, className, packageName, projectName, lineProjectName, scriptProjectName, targetProjectName, targetLaunchPath,
           targetTomlPath, targetBuildPath, targetConfigPath, targetDistPath, pyPath, yamlConfig, scriptConfig,
           scriptPath, consoleScripts, codePaths, modules):
        return Script(pyName, className, packageName, projectName, lineProjectName, scriptProjectName, targetProjectName,
                      targetLaunchPath, targetTomlPath, targetBuildPath, targetConfigPath, targetDistPath, pyPath,
                      yamlConfig, scriptConfig, scriptPath, consoleScripts, codePaths, modules)

    @staticmethod
    def get():
        path = FileUtil.getAbsPath(False, "src", "script_py", "deploy", "service")
        scripts = Script.getByPath()
        scripts.extend(Script.getByPath(path))
        return scripts

    @staticmethod
    def getByPath(appletDir=""):
        appletDir = appletDir if len(appletDir) > 0 else FileUtil.getAbsPath(False, "src", "script_py", "applet")
        assetsDir = FileUtil.getAbsPath(False, "src", "assets")
        scriptDir = FileUtil.getAbsPath(False, "script")
        targetDir = FileUtil.getAbsPath(False, "target")
        sep = "\\" if "\\" in appletDir else "/"
        lstFile = FileUtil.list(appletDir)
        lstScript = []
        for file in lstFile:
            if file.startswith("__"): continue
            pyPath = appletDir + sep + file
            if FileUtil.isFolder(pyPath):
                pyPath = Script.getScript(pyPath)
            modules = set()
            index = pyPath.rfind(sep) + 1
            pyName = pyPath[index:]
            yamlName = GenUtil.toLine(pyName)
            scriptName = GenUtil.toLine(pyName)
            className = pyName.replace(".py", "")
            projectName = GenUtil.toLine(className)
            lineProjectName = projectName.replace("-", "_")
            yamlName = yamlName.replace(".py", ".yaml")
            yamlConfig = assetsDir + sep + yamlName
            scriptConfig = scriptDir + sep + yamlName
            scriptPath = scriptDir + sep + scriptName
            consoleScripts = Script.getConsoleScripts(className)
            packageName = Script.getPackageName(pyPath, className)
            targetBuildPath = targetDir + sep + projectName
            scriptProjectName = scriptDir + sep + lineProjectName
            targetProjectName = targetDir + sep + projectName + sep + "src" + sep + lineProjectName
            targetLaunchPath = FileUtil.dirname(targetProjectName) + sep + scriptName
            targetTomlPath = targetDir + sep + projectName + sep + "pyproject.toml"
            targetDistPath = targetProjectName + sep + projectName + sep + "dist"
            targetConfigPath = targetProjectName + sep + yamlName
            codePaths = {FileUtil.getAbsPath(False, "src", "script_py", "Application.py")}
            code = Script.dictCodes[pyPath]
            codePaths.add(code.path)
            modules.update(code.externalModules)
            Script.analyzeCode(Script.dictCodes[pyPath], set(), codePaths, modules)
            lstScript.append(
                Script.of(pyName, className, packageName, projectName, lineProjectName, scriptProjectName, targetProjectName,
                          targetLaunchPath, targetTomlPath, targetBuildPath, targetConfigPath, targetDistPath, pyPath,
                          yamlConfig, scriptConfig, scriptPath, consoleScripts, codePaths, modules))
        return lstScript

    @staticmethod
    def fillTargetInitFile(folder):
        files = FileUtil.list(folder)
        sep = "\\" if "\\" in folder else "/"
        initFile = folder + sep + "__init__.py"
        if not GenUtil.has(files, "__init__.py"):
            FileUtil.create(initFile)
        for file in files:
            path = folder + sep + file
            if FileUtil.isFolder(path):
                Script.fillTargetInitFile(path)

    @staticmethod
    def getConsoleScripts(className):
        scriptStr = GenUtil.toLine(className)
        tempScriptStr = scriptStr.replace("-", "_")
        return scriptStr + " = \"" + tempScriptStr + ".Application:Application.run\""

    @staticmethod
    def getPackageName(path, className):
        sep = "\\" if "\\" in path else "/"
        packageName = path.split("script_py")[1][1:]
        packageName = packageName.replace(sep, ".")
        packageName = packageName.replace(".py", "")
        return "from ." + packageName + " import " + className

    @staticmethod
    def analyzeCode(code, paths, codePaths, modules):
        for path in code.internalImports:
            if path not in Script.dictCodes.keys(): continue
            if path in paths: continue
            paths.add(path)
            code = Script.dictCodes[path]
            codePaths.add(code.path)
            modules.update(code.externalModules)
            Script.analyzeCode(code, paths, codePaths, modules)

    @staticmethod
    def getScript(folder):
        files = FileUtil.list(folder)
        sep = "\\" if "\\" in folder else "/"
        scripts = filter(lambda file: file.endswith(".py"), files)
        for script in scripts:
            if script.startswith("__"): continue
            return folder + sep + script
        return ""

    @property
    def pyName(self):
        return self._pyName

    @pyName.setter
    def pyName(self, value):
        self._pyName = value

    @property
    def scriptProjectName(self):
        return self._scriptProjectName

    @scriptProjectName.setter
    def scriptProjectName(self, value):
        self._scriptProjectName = value

    @property
    def targetDistPath(self):
        return self._targetDistPath

    @targetDistPath.setter
    def targetDistPath(self, value):
        self._targetDistPath = value

    @property
    def targetConfigPath(self):
        return self._targetConfigPath

    @targetConfigPath.setter
    def targetConfigPath(self, value):
        self._targetConfigPath = value

    @property
    def targetBuildPath(self):
        return self._targetBuildPath

    @targetBuildPath.setter
    def targetBuildPath(self, value):
        self._targetBuildPath = value

    @property
    def targetTomlPath(self):
        return self._targetTomlPath

    @targetTomlPath.setter
    def targetTomlPath(self, value):
        self._targetTomlPath = value

    @property
    def targetLaunchPath(self):
        return self._targetLaunchPath

    @targetLaunchPath.setter
    def targetLaunchPath(self, value):
        self._targetLaunchPath = value

    @property
    def targetProjectName(self):
        return self._targetProjectName

    @targetProjectName.setter
    def targetProjectName(self, value):
        self._targetProjectName = value

    @property
    def lineProjectName(self):
        return self._lineProjectName

    @lineProjectName.setter
    def lineProjectName(self, value):
        self._lineProjectName = value

    @property
    def projectName(self):
        return self._projectName

    @projectName.setter
    def projectName(self, value):
        self._projectName = value

    @property
    def packageName(self):
        return self._packageName

    @packageName.setter
    def packageName(self, value):
        self._packageName = value

    @property
    def className(self):
        return self._className

    @className.setter
    def className(self, value):
        self._className = value

    @property
    def modules(self):
        return self._modules

    @modules.setter
    def modules(self, value):
        self._modules = value

    @property
    def codePaths(self):
        return self._codePaths

    @codePaths.setter
    def codePaths(self, value):
        self._codePaths = value

    @property
    def consoleScripts(self):
        return self._consoleScripts

    @consoleScripts.setter
    def consoleScripts(self, value):
        self._consoleScripts = value

    @property
    def scriptPath(self):
        return self._scriptPath

    @scriptPath.setter
    def scriptPath(self, value):
        self._scriptPath = value

    @property
    def scriptConfig(self):
        return self._scriptConfig

    @scriptConfig.setter
    def scriptConfig(self, value):
        self._scriptConfig = value

    @property
    def yamlConfig(self):
        return self._yamlConfig

    @yamlConfig.setter
    def yamlConfig(self, value):
        self._yamlConfig = value

    @property
    def pyPath(self):
        return self._pyPath

    @pyPath.setter
    def pyPath(self, value):
        self._pyPath = value
