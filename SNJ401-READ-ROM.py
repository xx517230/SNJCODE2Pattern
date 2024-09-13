#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import msvcrt


re_hex_data = re.compile(r"(?:[0-9a-fA-F]{2}\s??){16}")
re_space_line = re.compile(r"\s+")  # 空行

write_head_info = """SET_DEC_FILE "YSV58080.DEC"

HEADER CS,SCK,DI,DO;

SPM_PATTERN (readrom_pat) {
   //C S D D
   //  C
   //S K I O
    *0 0 0 X*TS1, RPT 10;//TS1 50nS
    *0 0 0 X*;
    *0 0 0 X*;
// DI = 0x38 => 0011 1000
// DO = 0xXX => XXXX XXXX
    *0 1 0 X*;
    *0 0 0 X*;
    *0 1 0 X*;
    *0 0 0 X*;
    *0 1 1 X*;
    *0 0 1 X*;
    *0 1 1 X*;
    *0 0 1 X*;
    *0 1 1 X*;
    *0 0 1 X*;
    *0 1 0 X*;
    *0 0 0 X*;
    *0 1 0 X*;
    *0 0 0 X*;
    *0 1 0 X*;
    *0 0 0 X*;
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


def data_list_to_pat_list(data_list, bitSize):
    pin_type = ("input", "output")
    data_count = 1
    isFist = True
    for data in data_list:
        if isFist:
            isFist = False
            with open("readrom.pat", "a", encoding="UTF-8") as fp:
                fp.write(write_head_info)
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


def get_file_data(data_file):
    data_list = list()
    with open(data_file, "rb") as fp:
        file_size = os.path.getsize(data_file)
        if file_size != 262144:
            print("提供的ROM二进制文件大小不是256Kb,非2MBbit,请确认!!!")
        while True:
            data = fp.read(16)
            if not data:  # 文件末尾跳出
                break
            for metadata in data:
                data_list.append(metadata)
    return data_list


def readRom():
    sourceFile = "ROM.bin"
    if os.path.exists("readrom.pat"):
        os.remove("readrom.pat")

    data_list = get_file_data(source_file)
    print(len(data_list))
    data_list_to_pat_list(data_list, 2 * 1024 * 1024)
