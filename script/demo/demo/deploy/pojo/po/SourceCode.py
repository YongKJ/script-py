from ....util.FileUtil import FileUtil
from ....util.GenUtil import GenUtil
from ....util.DataUtil import DataUtil
from ....pojo.po.Modules import Modules

import re


class SourceCode:

    def __init__(self, name="", path="", pycPath="", cachePycPath="", targetPath="", targetPycPath="", scriptPath="",
                 scriptPycPath="", content="", className="", internalImports=set(), externalModules=set()):
        self._name = name
        self._path = path
        self._pycPath = pycPath
        self._cachePycPath = cachePycPath
        self._targetPath = targetPath
        self._targetPycPath = targetPycPath
        self._scriptPath = scriptPath
        self._scriptPycPath = scriptPycPath
        self._content = content
        self._className = className
        self._internalImports = internalImports
        self._externalModules = externalModules

    @staticmethod
    def of(name, path, pycPath, cachePycPath, targetPath, targetPycPath, scriptPath, scriptPycPath, content, className,
           internalImports, externalModules):
        return SourceCode(name, path, pycPath, cachePycPath, targetPath, targetPycPath, scriptPath, scriptPycPath,
                          content, className, internalImports, externalModules)

    @staticmethod
    def get():
        srcFolder = FileUtil.getAbsPath(False, "src")
        return SourceCode.analyzeFolder(srcFolder)

    @staticmethod
    def analyzeFolder(folder):
        dictCodes = {}
        files = FileUtil.list(folder)
        sep = "\\" if "\\" in folder else "/"
        for file in files:
            if file == "assets": continue
            if file == "__pycache__": continue
            path = folder + sep + file
            if FileUtil.isFolder(path):
                dictCodes.update(SourceCode.analyzeFolder(path))
                continue
            dictCodes[path] = SourceCode.analyzeCode(path)
        return dictCodes

    @staticmethod
    def analyzeCode(path):
        targetPath = SourceCode.analyzePath(path, "target")
        scriptPath = SourceCode.analyzePath(path, "script")
        cachePycPath = SourceCode.analyzePath(path, "cache")
        pycPath = SourceCode.analyzePath(path, "pyc")
        className = SourceCode.getClassName(path)
        sep = "\\" if "\\" in path else "/"
        sep_index = path.rfind(sep) + 1
        content = FileUtil.read(path)
        name = path[sep_index:]
        return SourceCode.of(
            name, path, pycPath, cachePycPath, targetPath, SourceCode.analyzePath(targetPath, "pyc"),
            scriptPath, SourceCode.analyzePath(scriptPath, "pyc"), content, className,
            SourceCode.analyzeInternalImports(path, content),
            SourceCode.analyzeExternalModules(path, content)
        )

    @staticmethod
    def analyzeInternalImports(path, content):
        imports = set()
        pattern = re.compile("from\\s(\\S+)\\simport.*")
        for match in pattern.finditer(content):
            imports.add(SourceCode.analyzeImport(path, match.group(1)))
        return imports

    @staticmethod
    def analyzeImport(path, importStr):
        dirNumber = SourceCode.getDirNumber(importStr)
        sep = "\\" if "\\" in path else "/"
        for i in range(dirNumber):
            importStr = importStr[1:]
            path = FileUtil.dirname(path)
        return path + sep + importStr.replace(".", sep) + ".py"

    @staticmethod
    def getDirNumber(importStr):
        number = 0
        while importStr[0] == ".":
            importStr = importStr[1:]
            number += 1
        return number

    @staticmethod
    def analyzeExternalModules(path, content):
        modules = set()
        props = DataUtil.getProps(Modules)
        pattern = re.compile("\nimport\\s(\\S*)")
        for match in pattern.finditer(content):
            key = match.group(1)
            if not GenUtil.has(props, key): continue
            modules.add(DataUtil.getValue(Modules, key))
        return modules

    @staticmethod
    def analyzePath(path, type):
        oldPath = FileUtil.getAbsPath(False, "src")
        if type == "target":
            newPath = FileUtil.getAbsPath(False, "target", "script-py")
            return path.replace(oldPath, newPath)
        elif type == "script":
            newPath = FileUtil.getAbsPath(False, "script")
            return path.replace(oldPath, newPath)
        elif type == "cache":
            sep = "\\" if "\\" in path else "/"
            index = path.rfind(sep) + 1
            name = path[index:].replace(".py", ".cpython-36.pyc")
            return FileUtil.dirname(path) + sep + "__pycache__" + sep + name
        else:
            return path.replace(".py", ".pyc")

    @staticmethod
    def getClassName(path):
        sep = "\\" if "\\" in path else "/"
        sep_index = path.rfind(sep) + 1
        suf_index = path.rfind(".")
        return path[sep_index:suf_index]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def pycPath(self):
        return self._pycPath

    @pycPath.setter
    def pycPath(self, value):
        self._pycPath = value

    @property
    def cachePycPath(self):
        return self._cachePycPath

    @cachePycPath.setter
    def cachePycPath(self, value):
        self._cachePycPath = value

    @property
    def targetPath(self):
        return self._targetPath

    @targetPath.setter
    def targetPath(self, value):
        self._targetPath = value

    @property
    def targetPycPath(self):
        return self._targetPycPath

    @targetPycPath.setter
    def targetPycPath(self, value):
        self._targetPycPath = value

    @property
    def scriptPath(self):
        return self._scriptPath

    @scriptPath.setter
    def scriptPath(self, value):
        self._scriptPath = value

    @property
    def scriptPycPath(self):
        return self._scriptPycPath

    @scriptPycPath.setter
    def scriptPycPath(self, value):
        self._scriptPycPath = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def className(self):
        return self._className

    @className.setter
    def className(self, value):
        self._className = value

    @property
    def internalImports(self):
        return self._internalImports

    @internalImports.setter
    def internalImports(self, value):
        self._internalImports = value

    @property
    def externalModules(self):
        return self._externalModules

    @externalModules.setter
    def externalModules(self, value):
        self._externalModules = value
