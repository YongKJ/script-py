import re
import os
import sys
import shutil


class FileUtil:

    @staticmethod
    def appDir(is_prod=False):
        launch_path = FileUtil.dirname(__file__)
        app_dir = FileUtil.dirname(launch_path)
        if is_prod:
            if "site-packages" in app_dir:
                return app_dir
            else:
                return FileUtil.dirname(app_dir)
        app_dir = FileUtil.dirname(app_dir)
        sep = "\\" if "\\" in app_dir else "/"
        tempPath = "script-py" + sep + "script"
        if tempPath in app_dir:
            app_dir = FileUtil.dirname(app_dir)
        return FileUtil.dirname(app_dir)

    @staticmethod
    def hasYaml(appDir):
        files = FileUtil.list(appDir)
        for file in files:
            if ".yaml" in file:
                return True
        return False

    @staticmethod
    def getAbsPath(is_prod, *names):
        path = FileUtil.appDir(is_prod)
        for name in names:
            path += os.path.sep + name
        return path

    @staticmethod
    def create(fileName):
        file = open(fileName, "w")
        file.close()

    @staticmethod
    def mkdir(fileName):
        if FileUtil.exist(fileName): return
        os.makedirs(fileName, exist_ok=True)

    @staticmethod
    def copy(srcFileName, desFileName):
        if FileUtil.isFolder(srcFileName):
            shutil.copytree(srcFileName, desFileName)
        else:
            shutil.copyfile(srcFileName, desFileName)

    @staticmethod
    def move(srcFileName, desFileName):
        shutil.move(srcFileName, desFileName)

    @staticmethod
    def rename(srcFileName, desFileName):
        os.rename(srcFileName, desFileName)

    @staticmethod
    def delete(fileName):
        if not FileUtil.exist(fileName): return
        if FileUtil.isFolder(fileName):
            shutil.rmtree(fileName)
        else:
            os.remove(fileName)

    @staticmethod
    def dirname(path):
        return os.path.dirname(path)

    @staticmethod
    def list(fileName):
        return os.listdir(fileName)

    @staticmethod
    def isFile(fileName):
        return os.path.isfile(fileName)

    @staticmethod
    def isFolder(fileName):
        return os.path.isdir(fileName)

    @staticmethod
    def exist(fileName):
        return os.path.exists(fileName)

    @staticmethod
    def read(fileName):
        try:
            line_break = "\r\n" if sys.platform.startswith("win") else "\n"
            with open(fileName, mode="r", encoding="utf-8", newline=line_break) as f:
                return f.read()
        except Exception as e:
            print(fileName)
            print(e)

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
        sep = "\r\n" if "\r\n" in content else "\n"
        contentArray = content.split(sep)
        pattern = re.compile(regStr)
        for i in range(0, len(contentArray)):
            line = contentArray[i]
            match = pattern.match(line)
            if not match: continue
            replaceStr = valueFunc(match.group(1))
            contentArray[i] = line.replace(match.group(1), replaceStr)
            if not isAll: break
        FileUtil.write(path, sep.join(contentArray))
