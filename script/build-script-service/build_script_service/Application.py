from .deploy.service.BuildScriptService import BuildScriptService


class Application:

    @staticmethod
    def run():
        BuildScriptService.run()
