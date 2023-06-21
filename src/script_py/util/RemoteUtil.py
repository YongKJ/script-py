import subprocess


class RemoteUtil:
    workFolder = ""

    @staticmethod
    def execLocalCmd(command):
        if len(RemoteUtil.workFolder) > 0:
            subprocess.call(command, cwd=RemoteUtil.workFolder)
        else:
            subprocess.call(command)

    @staticmethod
    def changeWorkFolder(home):
        RemoteUtil.workFolder = home
