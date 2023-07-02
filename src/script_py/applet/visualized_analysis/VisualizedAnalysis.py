import pandas as Pandas
import plotly.offline as Plot
import plotly.express as BrushPlot

from ...util.GenUtil import GenUtil
from ...util.FileUtil import FileUtil


class VisualizedAnalysis:

    def __init__(self):
        self.outPath = GenUtil.getValue("output-path")
        self.excelPath = GenUtil.getValue("excel-path")

    def apply(self):
        cols = ["train_loss", "test_loss", "train_acc", "test_acc"]
        sheetData = Pandas.read_excel(self.excelPath)
        FileUtil.mkdir(self.outPath)
        for col in cols:
            title = "epoch / " + col
            fileName = self.outPath + "epoch-" + col + ".html"
            linePlot = BrushPlot.line(sheetData, "epoch", col, title=title)

            linePlot.update_traces(line_color="rgb(31,119,180)")
            linePlot.update_xaxes(gridcolor="rgb(238,238,238)")
            linePlot.update_yaxes(gridcolor="rgb(238,238,238)")
            linePlot.update_layout(
                hoverlabel_bgcolor="rgb(31,119,180)",
                hoverlabel_font_color="white",
                plot_bgcolor="rgba(0,0,0,0)",
                width=800, height=600,
            )

            Plot.plot(linePlot, filename=fileName, auto_open=False)

    def multipleLineCharts(self):
        title = "visual analysis of training data"
        sheetData = Pandas.read_excel(self.excelPath)
        cols = ["train_loss", "test_loss", "train_acc", "test_acc"]
        linePlot = BrushPlot.line(sheetData, "epoch", cols, title=title)

        # linePlot.update_xaxes(gridcolor="rgb(238,238,238)", showspikes=True, spikesnap="cursor")
        # linePlot.update_yaxes(gridcolor="rgb(238,238,238)", showspikes=True, spikesnap="cursor")
        linePlot.update_xaxes(gridcolor="rgb(238,238,238)")
        linePlot.update_yaxes(gridcolor="rgb(238,238,238)")
        linePlot.update_traces(hovertemplate="%{y}")
        linePlot.update_layout(
            hoverlabel_font_color="white",
            plot_bgcolor="rgba(0,0,0,0)",
            width=800, height=600,
            yaxis_title="data",
            legend_title="",
            # hoverdistance=0,
            hovermode="x",
        )

        FileUtil.mkdir(self.outPath)
        fileName = self.outPath + "epoch-data.html"
        Plot.plot(
            linePlot, filename=fileName, auto_open=False,
            config={"modeBarButtonsToAdd": ["toggleSpikelines"]}
        )

    @staticmethod
    def run():
        try:
            # VisualizedAnalysis().apply()
            VisualizedAnalysis().multipleLineCharts()
            GenUtil.println("HTML 文件导出成功！")
        except Exception as e:
            GenUtil.println("HTML 文件导出失败！")
            GenUtil.print(e)
