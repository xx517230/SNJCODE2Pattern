#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from MyWindow import *

patternHeadInfo = """SET_DEC_FILE "SNJ401.DEC"

HEADER  PA3,PB3,PB2,VPP_CTRL,PA1;//VPP_CTRL控制VPP_CH(PMU 7.5V)与VPP_PAD的通断，PA1通过二极管与VPP_PAD连接（二极管防止VPP 7.5V灌入通道）

SPM_PATTERN(writeRom)
{
   //PPP V
   //ABB P
   //332 P
    *0XX10*TS4,RPT 5;//TS4 50uS
    *0XX10*;// 0    To enter I2C mode: VPP= 0101 0011 1010 11 01
    *1XX10*;
    *0XX11*;// 1
    *1XX11*;
    *0XX10*;// 0
    *1XX10*;
    *0XX11*;// 1
    *1XX11*;
    *0XX10*;// 0
    *1XX10*;
    *0XX10*;// 0
    *1XX10*;
    *0XX11*;// 1
    *1XX11*;
    *0XX11*;// 1
    *1XX11*;
    *0XX11*;// 1
    *1XX11*;
    *0XX10*;// 0
    *1XX10*;
    *0XX11*;// 1
    *1XX11*;
    *0XX10*;// 0
    *1XX10*;
    *0XX11*;// 1
    *1XX11*;
    *0XX11*;// 1
    *1XX11*;
    *0XX10*;// 0
    *1XX10*;
    *0XX11*;// 1
    *1XX11*;
    *01111*RPT 8; //delay
    *01111*;//I2C MODE
    *01111*;//I2C start
    *01011*;
    *00011*;//CCIN CC=0
    *01011*;
    *01011*;
    *00011*;
    *00011*;//0  COMMAND ADDR
    *01011*;
    *01011*;
    *00011*;
    *00011*;//0
    *01011*;
    *01011*;
    *00011*;
    *00111*;//1
    *01111*;
    *01111*;
    *00111*;
    *00011*;//0
    *01011*;
    *01011*;
    *00011*;
    *00X11*;
    *00X11*;
    *00X11*;//ACK
    *01L11*;
    *01L11*;
    *00X11*;
    *00X11*;
    *00X11*;
    *00X11*;//H  READ ID0=11 0000 0001
    *01H11*;
    *00X11*;//H
    *01H11*;
    *00X11*;//L
    *01L11*;
    *00X11*;//L
    *01L11*;
    *00X11*;//L
    *01L11*;
    *00X11*;//L
    *01L11*;
    *00X11*;//L
    *01L11*;
    *00X11*;//L
    *01L11*;
    *00X11*;//L
    *01L11*;
    *00X11*;//H
    *01H11*;
    *00011*;//STOP
    *01011*;
    *01111*;
    *01111*;//I2C start     set rwt 64H
    *01111*;
    *01011*;
    *00011*;//CCIN CC=0
    *01011*;
    *01011*;
    *00011*;
    *00111*;//1  COMMAND ADDR
    *01111*;
    *01111*;
    *00111*;
    *00011*;//0
    *01011*;
    *01011*;
    *00011*;
    *00011*;//0
    *01011*;
    *01011*;
    *00011*;
    *00011*;//0
    *01011*;
    *01011*;
    *00011*;
    *00X11*;
    *00X11*;
    *00X11*;//ACK
    *01L11*;
    *01L11*;
    *00X11*;
    *00X11*;
    *00X11*;
    *00011*;//0 write 64H 00 0110 0100
    *01011*;
    *00011*;//0
    *01011*;
    *00011*;//0
    *01011*;
    *00111*;//1
    *01111*;
    *00111*;//1
    *01111*;
    *00011*;//0
    *01011*;
    *00011*;//0
    *01011*;
    *00111*;//1
    *01111*;
    *00011*;//0
    *01011*;
    *00011*;//0
    *01011*;
    *00X11*;
    *00X11*;//ACK
    *01L11*;
    *01L11*;
    *00X11*;
    *00X11*;
    *00011*;//STOP
    *01011*;
    *01111*;
    *01111*;//I2C start 
    *01011*;
    *01011*;
    *00111*;//进入write mode
    *00111*;
    *01111*;//CC=1
    *01111*;
    *00011*;
    *00011*;
    *01011*;//RWB=0
    *01011*;
    *00011*;
    *00001*RPT 10;      //PMU7.5V接上,同时保持PA1 3V
    *00001*RPT 10;
    *00001*;            //VPP set to 7.5V for OTP program   
    *00001*TS8,RPT 10;//write data start
"""

patternForNotEnd = """    *00001*;
    *01001*;//NOT END 0
    *00L01*;
    *01L01*;//ACK AK06
    *00X01*RPT 8;
"""
patternForEnd = """    *00101*TS1;//5uS
    *01101*;//END 1
    *00101*;
    *00H01*;//NOT ACK
    *01H01*;//NOT ACK
    *00H01*;//NOT ACK
    *01H01*;//NOT ACK
    *00H01*;//NOT ACK
    *01H01*;//NOT ACK
    *00H01*;//NOT ACK  WEND
    *01H01*;//NOT ACK
    *00H01*;//NOT ACK
    *01H01*;//NOT ACK
    *00H01*;//NOT ACK
    *01H01*;//NOT ACK
    *00H01*;//NOT ACK
    *01H01*;//NOT ACK
    *00H01*;//NOT ACK
    *01H01*;//NOT ACK
    *00H01*;//NOT ACK
    *01H01*;//NOT ACK
    *00H01*;//NOT ACK
    *01H01*;//NOT ACK
    *00L01*;//ACK AK07
    *01L01*;
    *00X11*RPT 2000;//vpp 7.5V->3V
    *00111*;
    *01111*;
    *00111*;
    *01111*;
    *00111*;
    *01111*;
    *00111*;
    *01111*;
    *00111*;
    *01111*;
    *00111*;
    *01111*;
    *00111*;
    *01111*;
    *00111*;
    *01111*;
    *00111*;
    *01111*;
    *00111*;
    *01111*;
    *00011*;
    *01011*;//AKI8
    *00H11*;
    *01H11*;
    *00H11*;
    *01H11*;
    *00H11*;
    *01H11*;
    *00H11*;
    *01H11*;
    *00H11*;
    *01L11*;//AKO9
    *00L11*;
    *01L11*;
    *00111*;
    *01111*;
    *00011*;//STOP
    *01011*;
    *01111*;
    *01111*;
}
"""


def data2bitList(data):
    bitList = ["0"] * 8
    for i in range(8 - 1, -1, -1):
        if data >> i & 1:
            bitList[i] = "1"
        else:
            bitList[i] = "0"
    return bitList


def writeData2File(data, bitList, byteCnt, fp, fileSize):
    for i in range(8 - 1, -1, -1):
        if i == 7:
            fp.write(
                "    *00%s01*;//addr=%s(%d), data = %s => %s %s\n"
                % (
                    bitList[i],
                    "0x" + str(hex(byteCnt)[2:].zfill(5)).upper(),
                    byteCnt,
                    "0x" + str(hex(data)[2:].zfill(2)).upper(),
                    "".join(bitList[7:3:-1]),
                    "".join(bitList[-5:-9:-1]),
                )
            )
            fp.write("    *01%s01*;//D%s %s\n" % (bitList[i], i, bitList[i]))
        else:
            if i == 6 and byteCnt == 0x07A7:
                fp.write("O8M:")
                fp.write("*00%s01*;\n" % bitList[i])
                fp.write("    *01%s01*;//D%s %s\n" % (bitList[i], i, bitList[i]))
                continue
            if i == 5 and byteCnt == 0x07A8:
                fp.write("O32:")
                fp.write("*00%s01*;\n" % bitList[i])
                fp.write("    *01%s01*;//D%s %s\n" % (bitList[i], i, bitList[i]))
                continue
            fp.write("    *00%s01*;\n" % bitList[i])
            fp.write("    *01%s01*;//D%s %s\n" % (bitList[i], i, bitList[i]))
    if byteCnt != fileSize - 1:
        fp.write(patternForNotEnd)
    else:
        fp.write(patternForEnd)


def data2Pattern(self, dataList, patternFile, fileSize):
    byteCnt = 0
    bitList = ["0"] * 8
    with open(patternFile, "a", encoding="UTF-8") as fp:
        fp.write(patternHeadInfo)
        for data in dataList:
            bitList = data2bitList(data)
            writeData2File(data, bitList, byteCnt, fp, fileSize)
            byteCnt += 1
            if byteCnt % (int(fileSize / 100)) == 0 or byteCnt == fileSize:
                self.labelStatus.setText(
                    f"生成writeRom.pat: 共 {int(fileSize/1024)} KB, 已处理 {int(byteCnt/1024)} KB, {int((byteCnt/fileSize)*100)}%"
                )
                self.labelStatus.repaint()
                self.pBar.setValue(int((byteCnt / fileSize) * 100))
    return byteCnt


def checkFileSize(self, file, size):
    fileSize = os.path.getsize(file)
    if fileSize != size:
        QMessageBox.critical(
            self, "警告", f"{file} 不是{size/1024}KB 文件大小,请确认fpga文件是否正确!"
        )


def getFileData(file):
    dataList = list()
    with open(file, "rb") as fp:
        while True:
            data = fp.read(16)
            if not data:  # 文件末尾跳出
                break
            for metaData in data:
                dataList.append(metaData)
    return dataList


def writeRom(self, filePath, fileSize):
    parDir = os.path.dirname(filePath)
    _, file = os.path.split(filePath)
    fileName, _ = os.path.splitext(file)
    srcFile = parDir + "/" + "WRITE_" + fileName.upper() + ".pat"
    if os.path.exists(srcFile):
        os.remove(srcFile)
    checkFileSize(self, filePath, fileSize)
    dataList = getFileData(filePath)
    byteCnt = data2Pattern(self, dataList, srcFile, fileSize)
    if byteCnt != fileSize:
        QMessageBox.critical(
            self, "警告", f"生成的{srcFile} 写入字节数不是{fileSize},请确认！！！"
        )
    QMessageBox.information(self, "完成", "writeRom 任务完成!")
