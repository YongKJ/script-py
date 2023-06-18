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
    def exist(fileName):
        return os.path.exists(fileName)
