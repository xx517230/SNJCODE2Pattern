import os
import re
import msvcrt

data_file_name = "ROM.bin"
output_file_name = "writerom.pat"
pat_pin_type = ("input", "output")

write_head_info = """SET_DEC_FILE "YSV58080.DEC"

HEADER CS,SCK,DI;

SPM_PATTERN (writerom_pat) {
   //C S D
   //  C
   //S K I
    *0 0 0*TS1, RPT 10;//TS1 50nS
    *0 0 0*;
    *0 0 0*;
"""
#写入数据协议格式开头
write_data_info_start = """// DI = 0x1A => 0001 1010
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 1*;
    *0 0 1*;
    *0 1 1*;
    *0 0 1*;
    *0 1 0*;
    *0 0 0*;
    *0 1 1*;
    *0 0 1*;
    *0 1 0*;
    *0 0 0*;
"""
#写入数据协议格式结尾
write_data_info_end = """// DI = 0x00 => 0000 0000
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
// DI = 0x00 => 0000 0000
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
// Delay 10uS
    *0 0 0*RPT 200; //50nS*200=10uS
// DI = 0x00 => 0000 0000
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;
    *0 1 0*;
    *0 0 0*;

    *1 0 0*RPT 16;

    *0 0 0*RPT 16;

"""

write_end_info = """
    *1 0 0*RPT 16;
    *1 0 0*;
}
"""


def errorInfo(str):
    # win32api.MessageBox(None, str, "错误", win32con.MB_ICONERROR | win32con.MB_OK | win32con.MB_SYSTEMMODAL);
    print(str)
    exit(0)


def int_to_pat(int, io_type, pin_type):
    bit_list = [0] * 8
    int_value = int(hex_str, 16)  # 十六进制字符串转int值
    if int_value > 255 or int_value < 0:
        error_info("int_to_pat方法中的数值不满足0~255范围,请确认!!!")
    if str.lower(io_type) not in pin_type:
        error_info("int_to_pat方法中io_type类型不是input或output,请确认!!!")
    for i in range(8 - 1, -1, -1):
        if int_value & (1 << i):
            if str.lower(io_type) == "input":
                bit_list[i] = "1"
            elif str.lower(io_type) == "output":
                bit_list[i] = "H"
        else:
            if str.lower(io_type) == "input":
                bit_list[i] = "0"
            elif str.lower(io_type) == "output":
                bit_list[i] = "L"
    return bit_list


def write_pat_to_file(data, bit_list, waveform_format):
    with open("rom.pat", "a", encoding="UTF-8") as fp:
        fp.write("// DI = %s => %s %s\n" % (hex(data), ''.join(bit_list[7:3:-1]), ''.join(bit_list[-5:-9:-1])))
        for i in range(8 - 1, -1, -1):
            if str.upper(waveform_format) == "NRZ":
                fp.write("    *0 1 %s*;\n" % (bit_list[i]))
                fp.write("    *0 0 %s*;\n" % (bit_list[i]))
            if str.upper(waveform_format) == "RZ":
                fp.write("    *0 1 %s*;\n" % (bit_list[i]))

def write_data_start():
    with open("rom.pat", "a", encoding="UTF-8") as fp:
        fp.write(write_data_info_start)

def write_data_end():
    with open("rom.pat", "a", encoding="UTF-8") as fp:
        fp.write(write_data_info_end)

def data_list_to_pat_list(data_list, bitSize):
    pin_type = ("input", "output")
    data_count = 0
    with open("rom.pat", "a", encoding="UTF-8") as fp:
        fp.write(write_head_info)
    for data in data_list:
        if data_count%16==0:
            write_data_start()
        bit_list = int_to_pat(data, "input", pin_type)
        write_pat_to_file(data, bit_list, "NRZ")
        data_count += 1
        
        if data_count%16==0:
            write_data_end()
        
        if data_count * 8 >= bitSize:
            with open("rom.pat", "a", encoding="UTF-8") as fp:
                fp.write(write_end_info)
            return

def int_to_pat(int, io_type, pin_type):
    list = [0] * 8
    int_value = int
    if int_value > 255 or int_value < 0:
        errorInfo("int_to_pat方法中的数值不满足0~255范围,请确认!!!")
    if str.lower(io_type) not in pat_pin_type:
        errorInfo("int_to_pat方法中io_type类型不是input或output,请确认!!!")
    for i in range(8 - 1, -1, -1):
        if (int_value & (1 << i)):
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


def write_spi_info(data_list, waveform_format):
    di_list = [0] * 8
    is_first = True
    with open(output_file_name, "w", encoding="UTF-8") as fp:
        fp.write(write_head_info)
        for data in data_list:
            if type(data) is str:
                if  str.upper(data)== "0X1A":
                    if is_first:
                        is_first = False
                    else:
                        fp.write("\n")
                        fp.write("    *1 0 0*RPT 10;\n")
                        fp.write("\n")
                        fp.write("    *0 0 0*RPT 10;\n")
                        fp.write("\n")
                di_list = hex_string_to_pat(data, "input")
                fp.write("// DI = %s => %s %s\n" % (data, ''.join(di_list[7:3:-1]), ''.join(di_list[-5:-9:-1])))
                for i in range(8 - 1, -1, -1):
                    if str.upper(waveform_format) == "NRZ":
                        fp.write("    *0 1 %s*;\n" % (di_list[i]))
                        fp.write("    *0 0 %s*;\n" % (di_list[i]))
                    if str.upper(waveform_format) == "RZ":
                        fp.write("    *0 1 %s*;\n" % (di_list[i]))
            elif type(data) is dict:
                fp.write("// Delay 10uS\n")
                fp.write("    *0 0 0*RPT 200; //50nS*200=10uS\n")
        fp.write("\n")
        fp.write(write_end_info)


def get_file_data(data_file):
    data_list = list()
    with open(data_file, "rb") as fp:
        file_size=os.path.getsize(data_file)
        if file_size!=262144:
            print("提供的ROM二进制文件大小不是256Kb,非2MBbit,请确认!!!")
        while True:
            data = fp.read(16)
            if not data:  # 文件末尾跳出
                break
            for metadata in data:
                data_list.append(metadata)
    return data_list


# 获取当前工作目录
source_file = "ROM.bin"
if os.path.exists("writerom.pat"):
    os.remove("writerom.pat")

# 将每行的数据以集合元素形式添加到data_list
data_list = get_file_data(source_file)
# 将data_list中的每个元素中十六个的十六进制的拆分成单个十六进制保存到hex_str_list
# 此时hex_str_list是客供文件所有十六进制的集合
print(len(data_list))
data_list_to_pat_list(data_list, 2*1024*1024)
print("\n按任意键退出...",end='')
msvcrt.getch()