import os
import re
import sys

import yaml

from .FileUtil import FileUtil


class GenUtil:

    @staticmethod
    def getValue(key):
        path = sys._getframe().f_back.f_code.co_filename
        index = path.rfind(os.path.sep) + 1
        config = path[index:].replace(".py", ".yaml")
        return GenUtil.getConfig(GenUtil.toLine(config))[key]

    @staticmethod
    def writeConfig(data):
        path = sys._getframe().f_back.f_code.co_filename
        index = path.rfind(os.path.sep) + 1
        name = path[index:].replace(".py", ".yaml")
        config = GenUtil.getConfigPath(GenUtil.toLine(name))
        func = lambda f: yaml.dump(data, f, allow_unicode=True)
        FileUtil.writeFile(config, func)

    @staticmethod
    def getConfig(config):
        path = GenUtil.getConfigPath(config)
        return yaml.load(FileUtil.read(path), Loader=yaml.FullLoader)

    @staticmethod
    def getConfigPath(config):
        path = FileUtil.getAbsPath(True, config)
        if not FileUtil.exist(path):
            path = FileUtil.getAbsPath(False, "src", "assets", config)
        return path

    @staticmethod
    def toLine(name):
        return name[0:1].lower() + re.sub("([A-Z])", "-\\1", name[1:]).lower()

    @staticmethod
    def toHump(name):
        return name[0:1].upper() + re.sub("-(\\w)", lambda m: m.group(1).upper(), name[1:])

    @staticmethod
    def has(list, e):
        for l in list:
            if e in l: return True
        return False

    @staticmethod
    def println(string=""):
        print(string)

    @staticmethod
    def print(string):
        print(string, end="")

    @staticmethod
    def strToList(line):
        return line.split(" ")

    @staticmethod
    def readParams(tips):
        return GenUtil.strToList(input(tips))
