from .deploy.service.BuildScriptService import BuildScriptService

from .applet.demo.Demo import Demo


class ApplicationTest:

    @staticmethod
    def run():
        # Demo.run()
        BuildScriptService.run()
