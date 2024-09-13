#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PySide2.QtWidgets import QMessageBox
import os
import re
import msvcrt


re_hex_data = re.compile(r"(?:[0-9a-fA-F]{2}\s??){16}")
re_space_line = re.compile(r"\s+")  # 空行
patternHeadInfo = """SET_DEC_FILE "SNJ401.DEC"
HEADER  PA3,VPP,PB3,PB2;

SPM_PATTERN(blanCheck)
{
           //PVPP
           //APBB
           //3P32
"""

write_end_info = """    *1 0 0 X*RPT 16;
    *1 0 0 X*;
}
"""


def error_info(info):
    win32api.MessageBox(
        None,
        info,
        "错误",
        win32con.MB_ICONERROR | win32con.MB_OK | win32con.MB_SYSTEMMODAL,
    )
    exit(0)


def esg_info(info):
    win32api.MessageBox(
        None, info, "转换完成", win32con.MB_OK | win32con.MB_SYSTEMMODAL
    )
    exit(0)


def int_to_pat(int_value, io_type, pin_type):
    list = [0] * 8
    if int_value > 255 or int_value < 0:
        errorInfo("int_to_pat方法中的数值不满足0~255范围,请确认!!!")
    if str.lower(io_type) not in pin_type:
        errorInfo("int_to_pat方法中io_type类型不是input或output,请确认!!!")
    for i in range(8 - 1, -1, -1):
        if int_value & (1 << i):
            if str.lower(io_type) == "input":
                list[i] = "1"
            elif str.lower(io_type) == "output":
                list[i] = "H"
        else:
            if str.lower(io_type) == "input":
                list[i] = "0"
            elif str.lower(io_type) == "output":
                list[i] = "L"
    return list


def write_pat_to_file(data, bit_list, waveform_format):
    with open("readrom.pat", "a", encoding="UTF-8") as fp:
        fp.write("// DI = 0xFF => 1111 1111\n")
        fp.write(
            "// DO = %s => %s %s\n"
            % (hex(data), "".join(bit_list[7:3:-1]), "".join(bit_list[-5:-9:-1]))
        )
        for i in range(8 - 1, -1, -1):
            if str.upper(waveform_format) == "NRZ":
                fp.write("    *0 1 1 X*;\n")
                fp.write("    *0 0 1 %s*;\n" % (bit_list[i]))
            if str.upper(waveform_format) == "RZ":
                fp.write("    *0 1 1 %s*;\n" % (bit_list[i]))


def write_pat_to_file_last_bit(data, bit_list, waveform_format):
    with open("readrom.pat", "a", encoding="UTF-8") as fp:
        fp.write("// DI = 0x00 => 0000 0000\n")
        fp.write(
            "// DO = %s => %s %s\n"
            % (hex(data), "".join(bit_list[7:3:-1]), "".join(bit_list[-5:-9:-1]))
        )
        for i in range(8 - 1, -1, -1):
            if str.upper(waveform_format) == "NRZ":
                fp.write("    *0 1 0 X*;\n")
                fp.write("    *0 0 0 %s*;\n" % (bit_list[i]))
            if str.upper(waveform_format) == "RZ":
                fp.write("    *0 1 0 %s*;\n" % (bit_list[i]))


def data2Pattern(patternFile, dataList):
    dataCnt = 1
    bitSize = len(dataList) * 8
    with open(patternFile, "a", encoding="UTF-8") as fp:
        fp.write(patternHeadInfo)

        for data in dataList:
            if data_count * 8 < bitSize:
                bit_list = int_to_pat(data, "output", pin_type)
                write_pat_to_file(data, bit_list, "NRZ")
            elif data_count * 8 == bitSize:
                print("==========")
                bit_list = int_to_pat(data, "output", pin_type)
                write_pat_to_file_last_bit(data, bit_list, "NRZ")
                with open("readrom.pat", "a", encoding="UTF-8") as fp:
                    fp.write("\n")
                    fp.write(write_end_info)
            if data_count * 8 > bitSize:
                print(">>>>>>")
                return
            data_count += 1


def getFileData(file, self):
    dataList = list()
    with open(file, "rb") as fp:
        fileSize = os.path.getsize(file)
        if fileSize != 128 * 1024:
            MessageBox = QMessageBox()
            MessageBox.critical(
                None, "警告", f"{file} 不是128K 文件大小,请确认bin文件是否正确!"
            )
        while True:
            data = fp.read(16)
            if not data:  # 文件末尾跳出
                break
            for metaData in data:
                dataList.append(metaData)
    return dataList


def readRom(filePath):
    parDir = os.path.dirname(filePath)
    fileName, _ = os.path.split(filePath)
    srcFile = parDir + "/" + fileName + ".pat"
    if os.path.exists(srcFile):
        os.remove(srcFile)
    dataList = getFileData(filePath)
    data2Pattern(dataList, srcFile)


if __name__ == "__main__":
    readRom()
