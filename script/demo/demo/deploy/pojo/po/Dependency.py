import re

from ....util.FileUtil import FileUtil


class Dependency:

    def __init__(self, text, name, version):
        self._text = text
        self._name = name
        self._version = version

    @staticmethod
    def of(text, name, version):
        return Dependency(text, name, version)

    @staticmethod
    def get():
        pattern = re.compile("\\[tool.poetry.dependencies\\]([\\s\\S]+?)\r\n\r\n")
        tomlPath = FileUtil.getAbsPath(False, "pyproject.toml")
        content = FileUtil.read(tomlPath)
        dependencies = []
        for match in pattern.finditer(content):
            tempPattern = re.compile("\\s\\s(\\S+)\\s=\\s\"(\\S+)\"")
            for tempMatch in tempPattern.finditer(match.group(1)):
                text = tempMatch.group()
                name = tempMatch.group(1)
                version = tempMatch.group(2)
                dependencies.append(Dependency.of(text, name, version))
        return dependencies

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
