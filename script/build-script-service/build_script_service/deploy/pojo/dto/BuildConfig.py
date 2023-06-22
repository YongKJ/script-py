from ....util.FileUtil import FileUtil
from ....util.GenUtil import GenUtil

import re


class BuildConfig:

    def __init__(self, tomlPath="", projectPath="", scriptPath="", targetPath="", launchPath="", launchContent="",
                 applicationPath="", tomlDependenciesPattern="", tomlDependenciesOriginal="", tomlNamePattern="",
                 tomlNameOriginal="", tomlScriptsPattern="", tomlScriptsOriginal="", scriptRunPattern="",
                 scriptRunOriginal="", packageImportPattern="", packageImportOriginal=""):
        self._tomlPath = tomlPath
        self._projectPath = projectPath
        self._scriptPath = scriptPath
        self._targetPath = targetPath
        self._launchPath = launchPath
        self._launchContent = launchContent
        self._applicationPath = applicationPath
        self._tomlDependenciesPattern = tomlDependenciesPattern
        self._tomlDependenciesOriginal = tomlDependenciesOriginal
        self._tomlNamePattern = tomlNamePattern
        self._tomlNameOriginal = tomlNameOriginal
        self._tomlScriptsPattern = tomlScriptsPattern
        self._tomlScriptsOriginal = tomlScriptsOriginal
        self._scriptRunPattern = scriptRunPattern
        self._scriptRunOriginal = scriptRunOriginal
        self._packageImportPattern = packageImportPattern
        self._packageImportOriginal = packageImportOriginal

    @staticmethod
    def of(tomlPath, projectPath, scriptPath, targetPath, launchPath, launchContent, applicationPath,
           tomlDependenciesPattern, tomlDependenciesOriginal, tomlNamePattern, tomlNameOriginal, tomlScriptsPattern,
           tomlScriptsOriginal, scriptRunPattern, scriptRunOriginal, packageImportPattern, packageImportOriginal):
        return BuildConfig(tomlPath, projectPath, scriptPath, targetPath, launchPath, launchContent, applicationPath,
                           tomlDependenciesPattern, tomlDependenciesOriginal, tomlNamePattern, tomlNameOriginal,
                           tomlScriptsPattern, tomlScriptsOriginal, scriptRunPattern, scriptRunOriginal,
                           packageImportPattern, packageImportOriginal)

    @staticmethod
    def get():
        projectPath = FileUtil.getAbsPath(False, "src", "script_py")
        tomlPath = FileUtil.getAbsPath(False, "pyproject.toml")
        scriptPath = FileUtil.getAbsPath(False, "script")
        sep = "\\" if "\\" in scriptPath else "/"
        targetPath = FileUtil.dirname(FileUtil.appDir(False)) + sep + "target"
        applicationPath = FileUtil.getAbsPath(False, "src", "script_py", "Application.py")
        launchPath = FileUtil.getAbsPath(False, "src", "script-py.py")
        launchContent = FileUtil.read(launchPath)
        config = BuildConfig.of(
            tomlPath, projectPath, scriptPath,
            targetPath, launchPath, launchContent, applicationPath,
            "(\\[tool.poetry.dependencies\\][\\s\\S]+?\r\n\r\n)", "",
            "name\\s=\\s\"(\\S+)\"", "script-py", "(\\S+\\s=\\s\"\\S+run\")",
            "script-py = \"script_py.Application:Application.run\"", "\\s+(\\S+)\\.run\\(\\)",
            "Demo", "(from[\\s\\S]+import[\\s\\S]+)", "from .applet.demo.Demo import Demo"
        )
        BuildConfig.analyzeTomlDependencies(config)
        return config

    @staticmethod
    def analyzeTomlDependencies(config):
        content = FileUtil.read(config.tomlPath)
        pattern = re.compile(config.tomlDependenciesPattern)
        for match in pattern.finditer(content):
            config.tomlDependenciesOriginal = match.group(1)

    @staticmethod
    def getTomlDependenciesLatest(dependencies, script):
        dependenciesStr = "[tool.poetry.dependencies]"
        for dependency in dependencies:
            if "python" in dependency.name:
                dependenciesStr += dependency.text
                continue
            if GenUtil.has(script.modules, dependency.name):
                dependenciesStr += dependency.text
        return dependenciesStr + "\r\n\r\n"

    @staticmethod
    def updateScript(folder, script):
        sep = "\\" if "\\" in folder else "/"
        files = FileUtil.list(folder)
        for file in files:
            if ".yaml" in file: continue
            srcPath = folder + sep + file
            desPath = srcPath.replace(
                script.targetLineProjectName,
                script.scriptLineProjectName
            )
            FileUtil.mkdir(FileUtil.dirname(desPath))
            FileUtil.copy(srcPath, desPath)

    @property
    def tomlPath(self):
        return self._tomlPath

    @tomlPath.setter
    def tomlPath(self, value):
        self._tomlPath = value

    @property
    def projectPath(self):
        return self._projectPath

    @projectPath.setter
    def projectPath(self, value):
        self._projectPath = value

    @property
    def scriptPath(self):
        return self._scriptPath

    @scriptPath.setter
    def scriptPath(self, value):
        self._scriptPath = value

    @property
    def targetPath(self):
        return self._targetPath

    @targetPath.setter
    def targetPath(self, value):
        self._targetPath = value

    @property
    def launchContent(self):
        return self._launchContent

    @launchContent.setter
    def launchContent(self, value):
        self._launchContent = value

    @property
    def launchPath(self):
        return self._launchPath

    @launchPath.setter
    def launchPath(self, value):
        self._launchPath = value

    @property
    def applicationPath(self):
        return self._applicationPath

    @applicationPath.setter
    def applicationPath(self, value):
        self._applicationPath = value

    @property
    def tomlDependenciesPattern(self):
        return self._tomlDependenciesPattern

    @tomlDependenciesPattern.setter
    def tomlDependenciesPattern(self, value):
        self._tomlDependenciesPattern = value

    @property
    def tomlDependenciesOriginal(self):
        return self._tomlDependenciesOriginal

    @tomlDependenciesOriginal.setter
    def tomlDependenciesOriginal(self, value):
        self._tomlDependenciesOriginal = value

    @property
    def tomlNamePattern(self):
        return self._tomlNamePattern

    @tomlNamePattern.setter
    def tomlNamePattern(self, value):
        self._tomlNamePattern = value

    @property
    def tomlNameOriginal(self):
        return self._tomlNameOriginal

    @tomlNameOriginal.setter
    def tomlNameOriginal(self, value):
        self._tomlNameOriginal = value

    @property
    def tomlScriptsPattern(self):
        return self._tomlScriptsPattern

    @tomlScriptsPattern.setter
    def tomlScriptsPattern(self, value):
        self._tomlScriptsPattern = value

    @property
    def tomlScriptsOriginal(self):
        return self._tomlScriptsOriginal

    @tomlScriptsOriginal.setter
    def tomlScriptsOriginal(self, value):
        self._tomlScriptsOriginal = value

    @property
    def scriptRunPattern(self):
        return self._scriptRunPattern

    @scriptRunPattern.setter
    def scriptRunPattern(self, value):
        self._scriptRunPattern = value

    @property
    def scriptRunOriginal(self):
        return self._scriptRunOriginal

    @scriptRunOriginal.setter
    def scriptRunOriginal(self, value):
        self._scriptRunOriginal = value

    @property
    def packageImportPattern(self):
        return self._packageImportPattern

    @packageImportPattern.setter
    def packageImportPattern(self, value):
        self._packageImportPattern = value

    @property
    def packageImportOriginal(self):
        return self._packageImportOriginal

    @packageImportOriginal.setter
    def packageImportOriginal(self, value):
        self._packageImportOriginal = value
