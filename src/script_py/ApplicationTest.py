from .deploy.service.BuildScriptService import BuildScriptService
from .applet.time_test.TimeTest import TimeTest
from .applet.demo.Demo import Demo


class ApplicationTest:

    @staticmethod
    def run():
        # TimeTest.run()
        BuildScriptService.run()
        # Demo.run()
