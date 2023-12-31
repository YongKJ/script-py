from ..pojo.po.Script import Script
from ...deploy.pojo.dto.BuildConfig import BuildConfig
from ...deploy.pojo.po.Dependency import Dependency
from ...util.CmdUtil import CmdUtil
from ...util.FileUtil import FileUtil
from ...util.GenUtil import GenUtil
from ...util.RemoteUtil import RemoteUtil


class BuildScriptService:

    def __init__(self):
        self.configType = 1
        self.scripts = Script.get()
        self.dependencies = Dependency.get()
        self.buildConfig = BuildConfig.get()

    def apply(self):
        GenUtil.println()
        for i in range(len(self.scripts)):
            GenUtil.println(str(i + 1) + ". " + self.scripts[i].pyName)
        GenUtil.println(str(len(self.scripts) + 1) + ". update script dependencies")
        GenUtil.print("Please enter one or more numbers corresponding to the script: ")
        nums = GenUtil.readParams()
        if len(nums) == 0: return
        GenUtil.println()

        for num in nums:
            index = int(num) - 1
            if 0 <= index < len(self.scripts):
                self.build(self.scripts[index])
            if index == len(self.scripts):
                buildCmd = CmdUtil.updateScriptDependencies()
                RemoteUtil.changeWorkFolder(FileUtil.appDir())
                RemoteUtil.execLocalCmd(buildCmd)

    def build(self, script):
        self.changeBuildConfig(script, True)
        self.changeTargetProject(script)

        RemoteUtil.changeWorkFolder(script.targetBuildPath)
        buildCmd = CmdUtil.buildScriptPackage()
        RemoteUtil.execLocalCmd(buildCmd)

        self.updateScript(script)
        self.changeBuildConfig(script, False)

    def updateScript(self, script):
        FileUtil.delete(script.scriptProjectName)
        BuildConfig.updateScript(script.targetLineProjectName, script)
        FileUtil.copy(self.buildConfig.launchPath, script.scriptPath)
        if FileUtil.exist(script.yamlConfig):
            FileUtil.copy(script.yamlConfig, script.scriptConfig)
        if script.className != BuildScriptService.__name__:
            BuildScriptService.updateScriptPackage(script)

    @staticmethod
    def updateScriptPackage(script):
        sep = "\\" if "\\" in script.targetDistPath else "/"
        files = FileUtil.list(script.targetDistPath)
        for file in files:
            srcPath = script.targetDistPath + sep + file
            desPath = script.scriptProjectName + sep + file
            FileUtil.copy(srcPath, desPath)

    def changeBuildConfig(self, script, isBefore):
        self.changeLaunchScript(script, isBefore)
        FileUtil.modContent(
            self.buildConfig.applicationPath, self.buildConfig.packageImportPattern,
            self.buildConfig.packageImportOriginal if not isBefore else script.packageName
        )
        FileUtil.modContent(
            self.buildConfig.applicationPath, self.buildConfig.scriptRunPattern,
            self.buildConfig.scriptRunOriginal if not isBefore else script.className
        )
        FileUtil.modContent(
            self.buildConfig.tomlPath, self.buildConfig.tomlNamePattern,
            self.buildConfig.tomlNameOriginal if not isBefore else script.projectName
        )
        FileUtil.modContent(
            self.buildConfig.tomlPath, self.buildConfig.tomlScriptsPattern,
            self.buildConfig.tomlScriptsOriginal if not isBefore else script.consoleScripts
        )
        FileUtil.modFile(
            self.buildConfig.tomlPath, self.buildConfig.tomlDependenciesPattern,
            self.buildConfig.tomlDependenciesOriginal if not isBefore else
            BuildConfig.getTomlDependenciesLatest(self.dependencies, script)
        )

    def changeLaunchScript(self, script, isBefore):
        if not isBefore:
            FileUtil.write(self.buildConfig.launchPath, self.buildConfig.launchContent)
            return
        FileUtil.modFile(self.buildConfig.launchPath, "(\r\n.*ApplicationTest.*)\r", "", True)
        FileUtil.modFile(self.buildConfig.launchPath, "(script_py)", script.lineProjectName)
        FileUtil.modFile(self.buildConfig.launchPath, "(#\\s)", "")

    def changeTargetProject(self, script):
        FileUtil.delete(script.targetProjectName)
        for codePath in script.codePaths:
            desCodePath = codePath.replace(
                self.buildConfig.projectPath,
                script.targetLineProjectName
            )
            FileUtil.mkdir(FileUtil.dirname(desCodePath))
            FileUtil.copy(codePath, desCodePath)
        Script.fillTargetInitFile(script.targetLineProjectName)
        if FileUtil.exist(script.yamlConfig):
            FileUtil.copy(script.yamlConfig, script.targetConfigPath)
        FileUtil.copy(self.buildConfig.tomlPath, script.targetTomlPath)

    @staticmethod
    def run():
        BuildScriptService().apply()
