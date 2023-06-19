import re
import os
import sys


class FileUtil:

    @staticmethod
    def appDir(is_prod):
        launch_path = os.path.realpath(sys.argv[0])
        app_dir = os.path.dirname(launch_path)
        if is_prod:
            return app_dir
        return os.path.dirname(app_dir)

    @staticmethod
    def getAbsPath(is_prod, *names):
        path = FileUtil.appDir(is_prod)
        for name in names:
            path += os.path.sep + name
        return path

    @staticmethod
    def list(fileName):
        return os.listdir(fileName)

    @staticmethod
    def isFolder(fileName):
        return os.path.isdir(fileName)

    @staticmethod
    def exist(fileName):
        return os.path.exists(fileName)

    @staticmethod
    def read(fileName):
        line_break = "\r\n" if sys.platform.startswith("win") else "\n"
        with open(fileName, mode="r", encoding="utf-8", newline=line_break) as f:
            return f.read()

    @staticmethod
    def write(fileName, content, conver=True):
        with open(fileName, mode="w" if conver else "a", encoding="utf-8", newline="\n") as f:
            return f.write(content)

    @staticmethod
    def writeFile(path, taskFunc):
        with open(path, mode="w", encoding="utf-8") as f:
            taskFunc(f)

    @staticmethod
    def modFile(path, regStr, value, isAll=False):
        FileUtil.modifyFile(path, regStr, lambda str: value, isAll)

    @staticmethod
    def modifyFile(path, regStr, valueFunc, isAll=False):
        content = re.sub(regStr, lambda m: valueFunc(m.group(1)), FileUtil.read(path), 0 if isAll else 1)
        FileUtil.write(path, content)

    @staticmethod
    def modContent(path, regStr, value, isAll=False):
        FileUtil.modify(path, regStr, lambda str: value, isAll)

    @staticmethod
    def modify(path, regStr, valueFunc, isAll=False):
        content = FileUtil.read(path)
        sep = "\r\n" if "\r\n" in path else "\n"
        contentArray = content.split(sep)
        pattern = re.compile(regStr)
        for line in contentArray:
            match = pattern.match(line)
            if not match: continue
            replaceStr = valueFunc(match.group(1))
            newLine = line.replace(match.group(1), replaceStr)
            content = content.replace(line, newLine)
            if not isAll: break
        FileUtil.write(path, content)
