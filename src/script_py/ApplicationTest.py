from .applet.visualized_analysis.VisualizedAnalysis import VisualizedAnalysis
from .deploy.service.BuildScriptService import BuildScriptService
from .applet.time_test.TimeTest import TimeTest
from .applet.demo.Demo import Demo


class ApplicationTest:

    @staticmethod
    def run():
        # VisualizedAnalysis.run()
        # TimeTest.run()
        # BuildScriptService.run()
        Demo.run()
