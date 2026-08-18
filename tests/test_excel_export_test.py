from script_py.applet.excel_export_test.ExcelExportTest import ExcelExportTest
from script_py.util.FileUtil import FileUtil
from script_py.util.PoiExcelUtil import PoiExcelUtil


def _target_dir():
    return FileUtil.getAbsPath(False, "target")


def test_write_test_one():
    FileUtil.mkdir(_target_dir())
    ExcelExportTest()._writeTestOne()

    lst_data = PoiExcelUtil.toMap(FileUtil.getAbsPath(False, "target", "demo.xlsx"))
    # 3 行表头 + 1000 行数据 = 1003 行；toMap 以第 0 行为表头，数据从第 1 行起 => 1002 行
    assert len(lst_data) == 1002
    # 前 2 行为表头第 1、2 行，第 3 行（lst_data[2]）起为数据行，test / demo 交替
    assert lst_data[2]["a"] == "test"
    assert lst_data[3]["a"] == "demo"
    assert lst_data[1001]["a"] == "demo"


def test_write_test_seven():
    FileUtil.mkdir(_target_dir())
    ExcelExportTest()._writeTestSeven()

    lst_data = PoiExcelUtil.toMap(FileUtil.getAbsPath(False, "target", "demo-test-by-thread.xlsx"))
    assert len(lst_data) == 5
    assert lst_data[0]["序号"] == "1"
    assert lst_data[0]["书名"] == "《水浒传》"
    assert lst_data[4]["书名"] == "《聊斋志异》"
