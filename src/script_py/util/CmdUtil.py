class CmdUtil:

    @staticmethod
    def updateScriptDependencies():
        return "poetry install"

    @staticmethod
    def buildScriptPackage():
        return "poetry build"
