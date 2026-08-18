from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from .FileUtil import FileUtil

# ==================== 常量（对应 Java 版 ExcelHeader 的常量） ====================

# 数据行高（磅）：Java 版 ROW_HEIGHT = 720 twip = 36 磅
_ROW_HEIGHT = 36.0

_CELL_MAX_WIDTH = 255 * 256
_LONG_FIELD_WIDTH = 50 * 256 * 3
_WIDTH_CACHE_MAX = 2048
_WIDTH_CACHE_KEY_MAX_LEN = 128

# 表头合并时四方向扩展的移动向量（右、下、左、上）
_MOVE = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# 列宽缓存（纯函数，只依赖字符串内容）
_width_cache = {}


# ==================== 列宽计算（对应 Java 版 getWidthCol / computeWidthCol） ====================

def _getWidthCol(value):
    if len(value) > _WIDTH_CACHE_KEY_MAX_LEN:
        return _computeWidthCol(value)
    if value in _width_cache:
        return _width_cache[value]
    width = _computeWidthCol(value)
    if len(_width_cache) < _WIDTH_CACHE_MAX:
        _width_cache[value] = width
    return width


def _computeWidthCol(value):
    chinese_sum, english_sum, char_sum = 0, 0, 0
    for c in value:
        if _isChinese(c):
            chinese_sum += 2
            char_sum += 2
        else:
            english_sum += 1
            char_sum += 1
    char_sum = 13 + char_sum - 1 if char_sum > 1 else 13
    if chinese_sum == 0 and english_sum > 0:
        char_sum += 4
    elif chinese_sum > 0 and english_sum > 0:
        percent = english_sum / chinese_sum
        if percent < 0.2:
            char_sum -= 2
        elif percent > 0.8:
            char_sum += 2
    # 对于较长字段封顶展示
    if len(value.encode("utf-8")) * 256 > _CELL_MAX_WIDTH:
        char_sum = _LONG_FIELD_WIDTH // 256
    return char_sum


def _isChinese(c):
    return "\u4e00" <= c <= "\u9fff" or "\u3400" <= c <= "\u4dbf" or "\uf900" <= c <= "\ufaff"


# ==================== 基础辅助 ====================

def _objToStr(value):
    """对应 Java 版 GenUtil.objToStr。"""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _cellValueToStr(value):
    """读侧单元格值转字符串（None -> 空串）。"""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip()


def _cellName(row, col):
    """0 基 (row, col) -> openpyxl 单元格名（1 基）。"""
    return get_column_letter(col + 1) + str(row + 1)


def _getSheet(wb, sheetName):
    return wb[sheetName] if sheetName else wb.active


def _resolvePath(fileName):
    if fileName.startswith("/") or fileName.startswith("\\"):
        return FileUtil.getAbsPath(False, "src", "assets", fileName)
    return fileName


# ==================== 上下文（对应 Java 版 ExcelContext） ====================

class _ExcelContext:
    def __init__(self):
        self.dataStartRow = 1
        self.styles = None
        self.colWidths = {}  # sheet_name -> {col: width}

    def updateDataStartRow(self, row):
        if row > self.dataStartRow:
            self.dataStartRow = row

    def getOrCreateColWidth(self, sheetName):
        m = self.colWidths.get(sheetName)
        if m is None:
            m = {}
            self.colWidths[sheetName] = m
        return m


_contexts = {}


def _getContext(wb):
    key = id(wb)
    ctx = _contexts.get(key)
    if ctx is None:
        ctx = _ExcelContext()
        _contexts[key] = ctx
    return ctx


# ==================== 样式（对应 Java 版 getCellStyles） ====================

def _buildCellStyles(wb):
    thin = Side(style="thin", color="FFD4D4D4")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    alignment = Alignment(horizontal="center", vertical="center")
    return [
        {"font": Font(name="Microsoft YaHei", size=11, bold=True),
         "fill": PatternFill(fill_type="solid", start_color="FFF2F2F2"),
         "border": border, "alignment": alignment},
        {"font": Font(name="Microsoft YaHei", size=10),
         "fill": PatternFill(fill_type="solid", start_color="FFFAFAFA"),
         "border": border, "alignment": alignment},
        {"font": Font(name="Microsoft YaHei", size=10),
         "border": border, "alignment": alignment},
    ]


def _applyStyle(cell, style):
    cell.font = style["font"]
    if "fill" in style:
        cell.fill = style["fill"]
    cell.border = style["border"]
    cell.alignment = style["alignment"]


# ==================== 写入辅助 ====================

def _setCellValue(ws, row, col, value):
    ws.cell(row=row + 1, column=col + 1, value=value)


def _setCellStyle(ws, styles, dataRow, row, col):
    """斑马纹样式（对应 Java 版 setCellStyle）。"""
    if dataRow % 2 == 0:
        style = styles[2] if row % 2 == 0 else styles[1]
    else:
        style = styles[2] if row % 2 != 0 else styles[1]
    _applyStyle(ws.cell(row=row + 1, column=col + 1), style)


def _setWidthColByAuto(wb, sheetName, col, value):
    ctx = _getContext(wb)
    m = ctx.getOrCreateColWidth(sheetName)
    w = float(_getWidthCol(value))
    if w > m.get(col, 0.0):
        m[col] = w


# ==================== 表头合并（对应 Java 版 checkMergeRange / merge） ====================

def _checkMergeRange(lstHeader, lstFlag, lstCoords, x, y, value):
    row_size = len(lstHeader[0])
    col_size = len(lstHeader)
    for move_x, move_y in _MOVE:
        mx, my = x + move_x, y + move_y
        if 0 <= mx < row_size and 0 <= my < col_size and not lstFlag[mx][my]:
            if lstHeader[my][mx] == value:
                lstFlag[mx][my] = True
                lstCoords.append((mx, my, lstHeader[my][mx]))
                _checkMergeRange(lstHeader, lstFlag, lstCoords, mx, my, value)


def _mergeHeader(wb, sheetName, lstCoords, styles, ctx):
    min_c = min(lstCoords, key=lambda c: (c[0], c[1]))
    max_c = max(lstCoords, key=lambda c: (c[0], c[1]))
    ws = _getSheet(wb, sheetName)
    # 表头数据写入到最小坐标的单元格中
    _setCellValue(ws, min_c[0], min_c[1], min_c[2])
    for x, y, value in lstCoords:
        # 记录列宽（写盘时统一应用）
        _setWidthColByAuto(wb, sheetName, y, value)
        ws.row_dimensions[x + 1].height = _ROW_HEIGHT
        # 记录数据起始行号（表头最大行号 + 1）
        ctx.updateDataStartRow(x + 1)
    # 表头样式应用到整个（合并）区域
    for x in range(min_c[0], max_c[0] + 1):
        for y in range(min_c[1], max_c[1] + 1):
            _applyStyle(ws.cell(row=x + 1, column=y + 1), styles[0])
    if len(lstCoords) > 1:
        ws.merge_cells(start_row=min_c[0] + 1, start_column=min_c[1] + 1,
                       end_row=max_c[0] + 1, end_column=max_c[1] + 1)


def _mergeHeaderByWidthCol(wb, sheetName, lstCoords, styles, widthCol):
    min_c = min(lstCoords, key=lambda c: (c[0], c[1]))
    max_c = max(lstCoords, key=lambda c: (c[0], c[1]))
    ws = _getSheet(wb, sheetName)
    _setCellValue(ws, min_c[0], min_c[1], min_c[2])
    ctx = _getContext(wb)
    for x, y, value in lstCoords:
        # 固定列宽作为下限，写盘时统一应用（与自动列宽取最大值）
        m = ctx.getOrCreateColWidth(sheetName)
        if float(widthCol) > m.get(y, 0.0):
            m[y] = float(widthCol)
        ws.row_dimensions[x + 1].height = _ROW_HEIGHT
    for x in range(min_c[0], max_c[0] + 1):
        for y in range(min_c[1], max_c[1] + 1):
            _applyStyle(ws.cell(row=x + 1, column=y + 1), styles[0])
    if len(lstCoords) > 1:
        ws.merge_cells(start_row=min_c[0] + 1, start_column=min_c[1] + 1,
                       end_row=max_c[0] + 1, end_column=max_c[1] + 1)


def _containsInt(lst, v):
    return v in lst


# ==================== 表头核心（对应 Java 版 writeHeader） ====================

def _writeHeaderCore(wb, sheetName, lstHeader, styles, dataCol, lstExcludeRow):
    col_size = len(lstHeader)
    row_size = len(lstHeader[0])
    lstFlag = [[False] * col_size for _ in range(row_size)]
    ctx = _getContext(wb)
    for row in range(row_size):
        for col in range(col_size):
            if not lstFlag[row][col]:
                lstFlag[row][col] = True
                lstCoords = [(row, col, lstHeader[col][row])]
                if not lstExcludeRow or row not in lstExcludeRow:
                    _checkMergeRange(lstHeader, lstFlag, lstCoords, row, col, lstHeader[col][row])
                _mergeHeader(wb, sheetName, lstCoords, styles, ctx)
    # 冻结：从左往右冻结 dataCol 列，从上往下冻结 dataStartRow 行
    ws = _getSheet(wb, sheetName)
    ws.freeze_panes = get_column_letter(dataCol + 1) + str(ctx.dataStartRow + 1)


def _writeHeaderByWidthColCore(wb, sheetName, lstHeader, styles, dataCol, dataRow, widthCol, lstExcludeRow):
    col_size = len(lstHeader)
    row_size = len(lstHeader[0])
    lstFlag = [[False] * col_size for _ in range(row_size)]
    for row in range(row_size):
        for col in range(col_size):
            if not lstFlag[row][col]:
                lstFlag[row][col] = True
                lstCoords = [(row, col, lstHeader[col][row])]
                if not lstExcludeRow or row not in lstExcludeRow:
                    _checkMergeRange(lstHeader, lstFlag, lstCoords, row, col, lstHeader[col][row])
                _mergeHeaderByWidthCol(wb, sheetName, lstCoords, styles, widthCol)
    ws = _getSheet(wb, sheetName)
    ws.freeze_panes = get_column_letter(dataCol + 1) + str(dataRow + 1)


# ==================== 门面（对应 Java 版 PoiExcelUtil） ====================

class PoiExcelUtil:

    # ---------- 读取 ----------

    @staticmethod
    def getWorkbook(fileName):
        """打开 Excel 文件（data_only 读取公式缓存值，对应 Java 版 getWorkbook(String)）。"""
        return load_workbook(fileName, data_only=True)

    @staticmethod
    def toMap(fileName):
        """读取默认 sheet（索引 0）、第 0 行为表头、数据从第 1 行开始。"""
        return PoiExcelUtil.toMapFull(fileName, None, 0, 0, -1, 1, -1, None)

    @staticmethod
    def toMapBySheet(fileName, sheetName, headerRow, dataRow):
        """指定 sheet 名、表头行、数据起始行。"""
        return PoiExcelUtil.toMapFull(fileName, sheetName, headerRow, 0, -1, dataRow, -1, None)

    @staticmethod
    def toMapFull(fileName, sheetName, headerRow, headerCol, headerLastCol, dataRow, dataLastRow, extraData):
        """完整参数读取（对应 Java 版 toMap(..., headerRow, headerCol, headerLastCol, dataRow, dataLastRow, extraData)）。"""
        wb = PoiExcelUtil.getWorkbook(fileName)
        try:
            ws = _getSheet(wb, sheetName)
            # 表头 -> 列索引
            if headerLastCol == -1 or headerLastCol > ws.max_column:
                headerLastCol = ws.max_column
            mapHeader = {}
            for col in range(headerCol + 1, headerLastCol + 1):
                value = _cellValueToStr(ws.cell(row=headerRow + 1, column=col).value)
                mapHeader[value] = col - 1  # 0 基列索引
            # 合并单元格一次性索引，O(1) 查询
            mergedIndex = PoiExcelUtil._buildMergedCellIndex(ws)
            # 数据行
            if dataLastRow == -1:
                dataLastRow = ws.max_row
            lst = []
            for row in range(dataRow + 1, dataLastRow + 1):
                m = {}
                for header, col in mapHeader.items():
                    value = _cellValueToStr(ws.cell(row=row, column=col + 1).value)
                    if value == "":
                        # mergedIndex 以 0 基 (row, col) 为键；此处 row 为 1 基、col 为 0 基
                        value = mergedIndex.get((row - 1, col), "")
                    if value != "":
                        m[header] = value
                if m:
                    if extraData:
                        m.update(extraData)
                    lst.append(m)
            return lst
        finally:
            wb.close()

    @staticmethod
    def _buildMergedCellIndex(ws):
        index = {}
        for rng in ws.merged_cells.ranges:
            value = _cellValueToStr(ws.cell(row=rng.min_row, column=rng.min_col).value)
            if not value:
                continue
            for row in range(rng.min_row, rng.max_row + 1):
                for col in range(rng.min_col, rng.max_col + 1):
                    index[(row - 1, col - 1)] = value
        return index

    # ---------- 样式 ----------

    @staticmethod
    def getCellStyles(wb):
        """创建三种样式（表头 / 斑马纹浅 / 斑马纹深），返回样式列表（对应 Java 版 getCellStyles）。"""
        return _buildCellStyles(wb)

    # ---------- 表头 ----------

    @staticmethod
    def writeHeader(wb, sheetName, lstHeader):
        """写表头（dataCol=0，自动样式）。"""
        PoiExcelUtil.writeHeaderByCol(wb, sheetName, lstHeader, 0)

    @staticmethod
    def writeHeaderByCol(wb, sheetName, lstHeader, dataCol):
        """写表头（自动样式）。"""
        PoiExcelUtil.writeHeaderByColExclude(wb, sheetName, lstHeader, dataCol, None)

    @staticmethod
    def writeHeaderByColExclude(wb, sheetName, lstHeader, dataCol, lstExcludeRow):
        """写表头（自动样式，跳过 lstExcludeRow 行的合并）。"""
        ctx = _getContext(wb)
        if ctx.styles is None:
            ctx.styles = _buildCellStyles(wb)
        _writeHeaderCore(wb, sheetName, lstHeader, ctx.styles, dataCol, lstExcludeRow)

    @staticmethod
    def writeHeaderByStyle(wb, sheetName, lstHeader, styles, dataCol):
        """写表头（显式样式）。"""
        PoiExcelUtil.writeHeaderByStyleExclude(wb, sheetName, lstHeader, styles, dataCol, None)

    @staticmethod
    def writeHeaderByStyleExclude(wb, sheetName, lstHeader, styles, dataCol, lstExcludeRow):
        """写表头（显式样式，跳过 lstExcludeRow 行的合并）。"""
        _writeHeaderCore(wb, sheetName, lstHeader, styles, dataCol, lstExcludeRow)

    @staticmethod
    def writeHeaderByWidthCol(wb, sheetName, lstHeader, styles, dataCol, widthCol):
        """写表头并设置固定列宽下限（显式样式，冻结 dataCol 列与上下文表头行数）。"""
        ctx = _getContext(wb)
        PoiExcelUtil.writeHeaderByWidthColRowExclude(wb, sheetName, lstHeader, styles, dataCol, ctx.dataStartRow,
                                                     widthCol, None)

    @staticmethod
    def writeHeaderByWidthColRow(wb, sheetName, lstHeader, styles, dataCol, dataRow, widthCol):
        """写表头并设置固定列宽下限（显式样式，显式冻结行数）。"""
        PoiExcelUtil.writeHeaderByWidthColRowExclude(wb, sheetName, lstHeader, styles, dataCol, dataRow, widthCol, None)

    @staticmethod
    def writeHeaderByWidthColRowExclude(wb, sheetName, lstHeader, styles, dataCol, dataRow, widthCol, lstExcludeRow):
        """写表头并设置固定列宽下限（完整参数）。"""
        _writeHeaderByWidthColCore(wb, sheetName, lstHeader, styles, dataCol, dataRow, widthCol, lstExcludeRow)

    # ---------- 数据 ----------

    @staticmethod
    def writeCellData(wb, sheetName, row, col, cellData):
        """写单元格（自动样式）。"""
        ctx = _getContext(wb)
        if ctx.styles is None:
            ctx.styles = _buildCellStyles(wb)
        PoiExcelUtil.writeCellDataByStyle(wb, sheetName, ctx.styles, row, col, cellData)

    @staticmethod
    def writeCellDataByStyle(wb, sheetName, styles, row, col, cellData):
        """写单元格（显式样式）。"""
        ctx = _getContext(wb)
        ws = _getSheet(wb, sheetName)
        value = _objToStr(cellData)
        _setCellValue(ws, row, col, value)
        # 记录列宽
        _setWidthColByAuto(wb, sheetName, col, value)
        # 设置斑马纹样式
        _setCellStyle(ws, styles, ctx.dataStartRow, row, col)
        if col == 0:
            ws.row_dimensions[row + 1].height = _ROW_HEIGHT

    @staticmethod
    def writeData(wb, sheetName, lstData):
        """批量写数据（自动样式，追加到末尾行）。"""
        if not lstData:
            return
        ctx = _getContext(wb)
        if ctx.styles is None:
            ctx.styles = _buildCellStyles(wb)
        ws = _getSheet(wb, sheetName)
        rowIndex = ws.max_row
        colSize = len(lstData[0])
        for mapData in lstData:
            for col in range(colSize):
                PoiExcelUtil.writeCellDataByStyle(wb, sheetName, ctx.styles, rowIndex, col, mapData.get(col))
            rowIndex += 1

    @staticmethod
    def writeRowData(wb, sheetName, mapData):
        """写一行（自动样式，追加到末尾行）。"""
        ctx = _getContext(wb)
        if ctx.styles is None:
            ctx.styles = _buildCellStyles(wb)
        ws = _getSheet(wb, sheetName)
        rowIndex = ws.max_row
        for col in range(len(mapData)):
            PoiExcelUtil.writeCellDataByStyle(wb, sheetName, ctx.styles, rowIndex, col, mapData.get(col))

    # ---------- 图片 ----------

    @staticmethod
    def writePicture(wb, sheetName, row, col, filePath):
        """在指定单元格写入图片（对应 Java 版 writePicture(sheet, row, col, filePath)）。"""
        from openpyxl.drawing.image import Image
        ws = _getSheet(wb, sheetName)
        img = Image(filePath)
        ws.add_image(img, _cellName(row, col))

    # ---------- 写盘 ----------

    @staticmethod
    def write(wb, fileName):
        """应用列宽并保存文件（对应 Java 版 write(workbook, fileName)）。"""
        ctx = _getContext(wb)
        for sheetName, cols in ctx.colWidths.items():
            ws = wb[sheetName]
            for col, width in cols.items():
                ws.column_dimensions[get_column_letter(col + 1)].width = width
        ctx.colWidths = {}
        wb.save(_resolvePath(fileName))
