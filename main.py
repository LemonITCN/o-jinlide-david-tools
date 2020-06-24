import os

import fitz
import openpyxl

import config_module
import exit_module
import global_data_module

SOURCE_EXCEL = 'sourceExcel'
SOURCE_EXCEL_FILE_NAME_COLUMN = 'sourceExcelFileNameColumn'
SOURCE_EXCEL_START_ROW = 'sourceExcelStartRow'
SOURCE_PDF = 'sourcePdf'
IMAGE_SCALE = 'scale'
OUTPUT_DIR = 'outputDir'


def read_asin_data(excel_path: str) -> []:
    workbook = openpyxl.load_workbook(excel_path)
    row_index = 0
    name_list = []
    for row in workbook.worksheets[0].rows:
        if row[0].value is not None and row_index >= config_module.get_config_obj()[SOURCE_EXCEL_START_ROW]:
            if row[0].value.strip() != '':
                name_list.append(row[config_module.get_config_obj()[SOURCE_EXCEL_FILE_NAME_COLUMN]].value)
        row_index = row_index + 1
    return name_list

print('正在初始化程序数据...')
global_data_module.init()
print('正在解析配置文件并读取Excel...')
# 读取Excel
file_names = read_asin_data(config_module.get_config_obj()[SOURCE_EXCEL])
print('正在解码PDF...')
# 读取PDF
pdf_doc = fitz.open(config_module.get_config_obj()[SOURCE_PDF])
print('PDF页数：' + str(pdf_doc.pageCount) + ', EXCEL 记录数：' + str(len(file_names)))
if pdf_doc.pageCount != len(file_names):
    exit_module.tip_and_wait_then_exit('Excel的记录数量与PDF页数不匹配，无法继续操作')
mat = fitz.Matrix(config_module.get_config_obj()[IMAGE_SCALE], config_module.get_config_obj()[IMAGE_SCALE])
if not os.path.exists(config_module.get_config_obj()[OUTPUT_DIR]):
    os.makedirs(config_module.get_config_obj()[OUTPUT_DIR])
for page_index in range(pdf_doc.pageCount):
    pdf_page = pdf_doc[page_index]
    print('开始转换写出第 ' + str(page_index + 1) + ' / ' + str(len(file_names)) + ' 页图片数据')
    pdf_page.getPixmap(matrix=mat).writePNG(
        config_module.get_config_obj()[OUTPUT_DIR] + os.sep + file_names[page_index] + '.png')

print('任务执行完毕')
