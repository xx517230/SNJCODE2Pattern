import os
import re
import win32api
import win32con
import msvcrt

data_file_name = "DATA.TXT"
output_file_name = "OUT.TXT"

pat_pin_type = ("input", "output")

# regex 预编译
re_list_hex_dict = re.compile(r'\s*(0[xX][a-fA-F0-9][a-fA-F0-9])\s*:(0[xX][a-fA-F0-9xX][a-fA-F0-9xX])\s*')
re_hex_xx = re.compile(r'0[xX]{3}')
re_space_line = re.compile(r'\s+')  # 空行


def errorInfo(str):
    # win32api.MessageBox(None, str, "错误", win32con.MB_ICONERROR | win32con.MB_OK | win32con.MB_SYSTEMMODAL);
    print(str)
    exit(0)

def hex_string_to_pat(hex_string, io_type):
    list = [0] * 8
    int_value = int(hex_string, 16)#十六进制字符串转int值
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


def write_spi_info(di_do_list, waveform_format):
    di_list = [0] * 8
    do_list = [0] * 8
    with open(output_file_name, "w", encoding="UTF-8") as fp:
        for dict in di_do_list:
            x_flag = False
            for key in dict:
                di_list = hex_string_to_pat(key, "input")
                # 判断是否为值是否为0xXX,如果是则输出不关注
                if re_hex_xx.match(dict[key]):
                    do_list = ['X'] * 8
                    x_flag = True
                if not x_flag:
                    do_list = hex_string_to_pat(dict[key], "output")
                fp.write("// DI = %s => %s %s\n" % (key, ''.join(di_list[7:3:-1]), ''.join(di_list[-5:-9:-1])))
                fp.write("// DO = %s => %s %s\n" % (dict[key], ''.join(do_list[7:3:-1]), ''.join(do_list[-5:-9:-1])))
                for i in range(8 - 1, -1, -1):
                    if str.upper(waveform_format) == "NRZ":
                        fp.write("    *0 1 %s X*\n" % (di_list[i]))
                        fp.write("    *0 0 %s %s*\n" % (di_list[i], do_list[i]))
                    if str.upper(waveform_format) == "RZ":
                        fp.write("    *0 1 %s %s*\n" % (di_list[i], do_list[i]))


def get_file_data(data_file):
    list = []
    key = ''
    value = ''
    with open(data_file, "r", encoding="UTF-8") as fp:
        while True:
            fileLine = fp.readline()
            if not fileLine:  # 文件末尾跳出
                break
            if re_space_line.match(fileLine):
                continue
            if re_list_hex_dict.match(fileLine):
                key = re_list_hex_dict.match(fileLine).group(1)
                value = re_list_hex_dict.match(fileLine).group(2)
                dict = {key: value}
                list.append(dict)
            if key == '' or value == '':
                errorInfo("%s文件中存在数据格式异常问题,请确认!!!" % data_file)
    return list


# 获取当前工作目录
work_dir = os.getcwd()
data_file = os.path.join(work_dir, data_file_name)
di_do_list = get_file_data(data_file)
write_spi_info(di_do_list, "NRZ")
# write_spi_info(di_do_list,"RZ")

print("\n按任意键退出...",end='')
msvcrt.getch()