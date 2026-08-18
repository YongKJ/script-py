from openpyxl import Workbook

from ...pojo.dto.Log import Log
from ...util.FileUtil import FileUtil
from ...util.GenUtil import GenUtil
from ...util.LogUtil import LogUtil
from ...util.PoiExcelUtil import PoiExcelUtil


class ExcelExportTest:
    """对应 Java 版 com.yongkj.applet.excelExportTest.ExcelExportTest。

    演示 PoiExcelUtil + ThreadUtil 的读写场景（多表头合并、多 sheet、固定列宽、样式）。

    与 Java 版的两处差异（有意为之）：
      1. 输出路径：Java 写死桌面路径，此处改为仓库 target/ 目录（可移植、可验证）。
      2. 线程：Java 外层并行写同一 workbook 的 5 个 sheet（共享字符串表非线程安全，属旧有风险）；
         此处 openpyxl 单 Workbook 非并发安全，故 sheet 写入串行。
    """

    def __init__(self):
        self.rowAccessWindowSize = 100
        self.excelReadPath = GenUtil.getValue("excel-read-path")
        self.excelWritePath = GenUtil.getValue("excel-write-path")

    @staticmethod
    def _output_path(name):
        # demo 产物定位到仓库 target/ 目录（可移植、可验证，忽略运行 cwd）
        return FileUtil.getAbsPath(False, "target", name)

    def _apply(self):
        FileUtil.mkdir(FileUtil.getAbsPath(False, "target"))
        self._writeTestSeven()
        # self._writeTestSix()
        # self._writeTestFive()
        # self._writeTestFour()
        # self._writeTestThree()
        # self._writeTestTwo()
        # self._writeTestOne()

    def _readTestTwo(self):
        """读取消息推送表格并转换为消息模板表格（对应 Java 版 readTestTwo，参考用）。"""
        lst_data = PoiExcelUtil.toMap(self.excelReadPath)
        lst_filtered = [po for po in lst_data
                        if "后端开发人员" in po and "宋明旭" in po["后端开发人员"]]

        LogUtil.loggerLine(Log.of("ExcelExportTest", "readTestTwo", "lstData.size()", len(lst_filtered)))
        LogUtil.loggerLine(Log.of("ExcelExportTest", "readTestTwo", "lstData", lst_filtered))

        id_value = 20001
        temp_lst_data = []
        for data in lst_filtered:
            sms_template_id = ""
            if "推送方式" in data and "短信" in data["推送方式"]:
                sms_template_id = "SMS_"
            if "新短信模板" in data:
                sms_template_id = data["新短信模板"]
            title = data.get("推送标题", "")
            if not title.strip() and sms_template_id.strip():
                title = "短信通知"
            content = data.get("推送内容", "")
            note = data.get("消息类型", "")
            if "/" in note:
                note = note.split("/")[0]
            if "商家" in note:
                note = "商家端"
            when_run = data.get("触发条件", "")
            link_mark = ""
            if "打开页面" in data and "跳转" in data["打开页面"]:
                link_mark = "after_sales_details"

            temp_data = {
                "id": str(id_value),
                "sms_template_id": sms_template_id,
                "title": title,
                "content": content,
                "note": note,
                "when_run": when_run,
                "link_mark": link_mark,
            }
            id_value += 1
            temp_lst_data.append(temp_data)

        lst_header = [["id"], ["sms_template_id"], ["title"], ["content"],
                      ["note"], ["when_run"], ["link_mark"]]

        wb = Workbook()
        sheet = wb.active.title
        styles = PoiExcelUtil.getCellStyles(wb)
        PoiExcelUtil.writeHeaderByStyle(wb, sheet, lst_header, styles, 1)

        row_index = len(lst_header[0])
        for data in temp_lst_data:
            col_index = 0
            for headers in lst_header:
                PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, data[headers[0]])
                col_index += 1
            row_index += 1

        PoiExcelUtil.write(wb, self._output_path("msg-template.xlsx"))

    def _readTestOne(self):
        """读取 excelReadPath 并打印（对应 Java 版 readTestOne）。"""
        lst_data = PoiExcelUtil.toMap(self.excelReadPath)

        LogUtil.loggerLine(Log.of("ExcelExportTest", "readTestOne", "lstData.size()", len(lst_data)))
        LogUtil.loggerLine(Log.of("ExcelExportTest", "readTestOne", "lstData", lst_data))
        print(
            "------------------------------------------------------------------------------------------------------------")

    def _writeTestSeven(self):
        """多 sheet + 分块窗口写数据（对应 Java 版 writeTestSeven）。"""
        lst_header = [["序号"], ["书名"], ["作者"], ["年代"], ["字数"]]
        map_data = {
            0: ["《水浒传》", "施耐庵", "宋朝", "96 万字"],
            1: ["《三国演义》", "罗贯中", "元朝", "73.4 万字"],
            2: ["《西游记》", "吴承恩", "明代", "82 万字"],
            3: ["《红楼梦》", "曹雪芹", "清代", "107.5 万字"],
            4: ["《聊斋志异》", "蒲松龄", "清代", "70.8 万字"],
        }

        data_row = len(lst_header[0])
        wb = Workbook()
        sheets = self._getSheets(wb)
        styles = PoiExcelUtil.getCellStyles(wb)
        # 单 workbook 库非并发安全（共享字符串表），sheet 写入串行。
        for sheet in sheets:
            PoiExcelUtil.writeHeaderByStyle(wb, sheet, lst_header, styles, 1)
            row_index = data_row
            i = 0
            while i < len(map_data):
                data_size = min(i + self.rowAccessWindowSize, len(map_data))
                for index in range(i, data_size):
                    col_index = 0
                    PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, row_index)
                    col_index += 1
                    for data in map_data[index]:
                        PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, data)
                        col_index += 1
                    row_index += 1
                i = data_size

        PoiExcelUtil.write(wb, self._output_path("demo-test-by-thread.xlsx"))

    def _writeTestSix(self):
        """多 sheet + 分块窗口 + 手动列宽（对应 Java 版 writeTestSix）。

        列宽已由 writeCellDataByStyle 自动记录并在写盘时统一应用，无需 Java 版的手动 mapColWidth。
        """
        lst_header = [["序号"], ["书名"], ["作者"], ["年代"], ["字数"]]
        map_data = {
            0: ["《水浒传》", "施耐庵", "宋朝", "96 万字"],
            1: ["《三国演义》", "罗贯中", "元朝", "73.4 万字"],
            2: ["《西游记》", "吴承恩", "明代", "82 万字"],
            3: ["《红楼梦》", "曹雪芹", "清代", "107.5 万字"],
            4: ["《聊斋志异》", "蒲松龄", "清代", "70.8 万字"],
        }

        data_row = len(lst_header[0])
        wb = Workbook()
        sheets = self._getSheets(wb)
        styles = PoiExcelUtil.getCellStyles(wb)
        for sheet in sheets:
            PoiExcelUtil.writeHeaderByStyle(wb, sheet, lst_header, styles, 1)
            row_index = data_row
            i = 0
            while i < len(map_data):
                data_size = min(i + self.rowAccessWindowSize, len(map_data))
                for index in range(i, data_size):
                    col_index = 0
                    PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, row_index)
                    col_index += 1
                    for data in map_data[index]:
                        PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, data)
                        col_index += 1
                    row_index += 1
                i = data_size

        PoiExcelUtil.write(wb, self._output_path("demo-test-by-thread-width.xlsx"))

    def _writeTestFive(self):
        """多 sheet + 固定列宽表头（对应 Java 版 writeTestFive）。"""
        lst_header = [["序号"], ["书名"], ["作者"], ["年代"], ["字数"]]
        map_data = {
            0: ["《水浒传》", "施耐庵", "宋朝", "96 万字"],
            1: ["《三国演义》", "罗贯中", "元朝", "73.4 万字"],
            2: ["《西游记》", "吴承恩", "明代", "82 万字"],
            3: ["《红楼梦》", "曹雪芹", "清代", "107.5 万字"],
            4: ["《聊斋志异》", "蒲松龄", "清代", "70.8 万字"],
        }

        data_row = len(lst_header[0])
        wb = Workbook()
        sheets = self._getSheets(wb)
        styles = PoiExcelUtil.getCellStyles(wb)
        for sheet in sheets:
            PoiExcelUtil.writeHeaderByWidthCol(wb, sheet, lst_header, styles, 1, 18)
            row_index = data_row
            i = 0
            while i < len(map_data):
                data_size = min(i + self.rowAccessWindowSize, len(map_data))
                for index in range(i, data_size):
                    col_index = 0
                    PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, row_index)
                    col_index += 1
                    for data in map_data[index]:
                        PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, data)
                        col_index += 1
                    row_index += 1
                i = data_size

        PoiExcelUtil.write(wb, self._output_path("demo-test-by-thread-style.xlsx"))

    def _writeTestFour(self):
        """多 sheet + 列表数据（对应 Java 版 writeTestFour）。"""
        lst_header = [["序号"], ["书名"], ["作者"], ["年代"], ["字数"]]
        lst_data = [
            ["《水浒传》", "施耐庵", "宋朝", "96 万字"],
            ["《三国演义》", "罗贯中", "元朝", "73.4 万字"],
            ["《西游记》", "吴承恩", "明代", "82 万字"],
            ["《红楼梦》", "曹雪芹", "清代", "107.5 万字"],
            ["《聊斋志异》", "蒲松龄", "清代", "70.8 万字"],
        ]

        data_row = len(lst_header[0])
        wb = Workbook()
        sheets = self._getSheets(wb)
        styles = PoiExcelUtil.getCellStyles(wb)
        for sheet in sheets:
            PoiExcelUtil.writeHeaderByStyle(wb, sheet, lst_header, styles, 1)
            row_index = data_row
            for temp_lst_data in lst_data:
                col_index = 0
                PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, row_index)
                col_index += 1
                for data in temp_lst_data:
                    PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, data)
                    col_index += 1
                row_index += 1

        PoiExcelUtil.write(wb, self._output_path("demo-test-by-thread-data.xlsx"))

    def _getSheets(self, wb):
        """创建一个 workbook 的 5 个 sheet（Sheet0..Sheet4）并返回 sheet 名列表。"""
        lst_sheet = []
        for i in range(5):
            sheet_name = "Sheet%d" % i
            if i == 0:
                wb.active.title = sheet_name
            else:
                wb.create_sheet(sheet_name)
            lst_sheet.append(sheet_name)
        return lst_sheet

    def _writeTestThree(self):
        """单 sheet 写两次（对应 Java 版 writeTestThree）。"""
        lst_header = [["序号"], ["书名"], ["作者"], ["年代"], ["字数"]]
        lst_data = [
            ["《水浒传》", "施耐庵", "宋朝", "96 万字"],
            ["《三国演义》", "罗贯中", "元朝", "73.4 万字"],
            ["《西游记》", "吴承恩", "明代", "82 万字"],
            ["《红楼梦》", "曹雪芹", "清代", "107.5 万字"],
            ["《聊斋志异》", "蒲松龄", "清代", "70.8 万字"],
        ]

        wb = Workbook()
        sheet = wb.active.title
        styles = PoiExcelUtil.getCellStyles(wb)
        PoiExcelUtil.writeHeaderByStyle(wb, sheet, lst_header, styles, 1)
        for i in range(len(lst_data)):
            row_index = len(lst_header[0]) + i
            col_index = 0
            PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, i + 1)
            col_index += 1
            for j in range(len(lst_data[i])):
                PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, lst_data[i][j])
                col_index += 1
        PoiExcelUtil.write(wb, self.excelReadPath)
        PoiExcelUtil.write(wb, self.excelWritePath)

    def _writeTestTwo(self):
        """5 个 sheet 自动列宽（对应 Java 版 writeTestTwo）。"""
        lst_header = [["序号"], ["书名"], ["作者"], ["年代"], ["字数"]]
        lst_data = [
            ["《水浒传》", "施耐庵", "宋朝", "96 万字"],
            ["《三国演义》", "罗贯中", "元朝", "73.4 万字"],
            ["《西游记》", "吴承恩", "明代", "82 万字"],
            ["《红楼梦》", "曹雪芹", "清代", "107.5 万字"],
            ["《聊斋志异》", "蒲松龄", "清代", "70.8 万字"],
        ]

        wb = Workbook()
        styles = PoiExcelUtil.getCellStyles(wb)
        for sheet in self._getSheets(wb):
            PoiExcelUtil.writeHeaderByStyle(wb, sheet, lst_header, styles, 1)
            for i in range(len(lst_data)):
                row_index = len(lst_header[0]) + i
                col_index = 0
                PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, i + 1)
                col_index += 1
                for j in range(len(lst_data[i])):
                    PoiExcelUtil.writeCellDataByStyle(wb, sheet, styles, row_index, col_index, lst_data[i][j])
                    col_index += 1
        PoiExcelUtil.write(wb, self._output_path("demo-width-auto.xlsx"))

    def _writeTestOne(self):
        """多行表头合并 + 批量写数据（对应 Java 版 writeTestOne）。"""
        lst_header = [
            ["a", "a", "e"],
            ["b", "b", "e"],
            ["b", "b", "f"],
            ["c", "a", "a"],
            ["c", "a", "a"],
            ["测", "测", "测"],
            ["测试", "测试", "测试"],
            ["t", "t", "t"],
            ["test", "test", "test"],
        ]

        wb = Workbook()
        sheet = wb.active.title
        PoiExcelUtil.writeHeaderByCol(wb, sheet, lst_header, 0)

        for _ in range(500):
            PoiExcelUtil.writeRowData(wb, sheet, self._getMapData("test"))
            PoiExcelUtil.writeRowData(wb, sheet, self._getMapData("demo"))
        PoiExcelUtil.write(wb, self._output_path("demo.xlsx"))

    @staticmethod
    def _getMapData(value):
        return {i: value for i in range(5)}

    @staticmethod
    def run():
        """对应 Java 版 ExcelExportTest.run(String[] args)。"""
        ExcelExportTest()._apply()
