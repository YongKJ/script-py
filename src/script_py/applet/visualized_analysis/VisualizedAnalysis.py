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

    @staticmethod
    def run():
        try:
            VisualizedAnalysis().apply()
            GenUtil.println("HTML 文件导出成功！")
        except Exception as e:
            GenUtil.println("HTML 文件导出失败！")
            GenUtil.print(e)
