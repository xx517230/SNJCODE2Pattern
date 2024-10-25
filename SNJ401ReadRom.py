#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from MyWindow import *

patternHeadInfo = """SET_DEC_FILE "SNJ401.DEC"

HEADER  PA3,VPP,PB3,PB2;

SPM_PATTERN(readRom)
{
   //PVPP
   //APBB
   //3P32
ST: *00XX*TS1;//TS1 5uS
    *00XX*;//     0     To enter I2C mode: VPP= 0101 0011 1010 11 01
    *10XX*;
    *01XX*;//     1
    *11XX*;
    *00XX*;//     0
    *10XX*;
    *01XX*;//     1
    *11XX*;
    *00XX*;//     0
    *10XX*;
    *00XX*;//     0
    *10XX*;
    *01XX*;//     1
    *11XX*;
    *01XX*;//     1
    *11XX*;
    *01XX*;//     1
    *11XX*;
    *00XX*;//     0
    *10XX*;
    *01XX*;//     1
    *11XX*;
    *00XX*;//     0
    *10XX*;
    *01XX*;//     1
    *11XX*;
    *01XX*;//     1
    *11XX*;
    *00XX*;//     0
    *10XX*;
    *01XX*;//     1
    *11XX*;
    *0011*RPT 8; //delay
    *0011*;//I2C MODE
    *0011*;//I2C start
    *0010*;
    *0000*;//CCIN CC=0
    *0010*;
    *0010*;
    *0000*;
    *0000*;//0  COMMAND ADDR
    *0010*;
    *0010*;
    *0000*;
    *0000*;//0
    *0010*;
    *0010*;
    *0000*;
    *0001*;//1
    *0011*;
    *0011*;
    *0001*;
    *0000*;//0
    *0010*;
    *0010*;
    *0000*;
    *000X*;//ACK
    *001L*;
    *001L*;
    *000X*;
    *000X*;//H  READ ID0=11 0000 0001
    *001H*;
    *000X*;//H
    *001H*;
    *000X*;//L
    *001L*;
    *000X*;//L
    *001L*;
    *000X*;//L
    *001L*;
    *000X*;//L
    *001L*;
    *000X*;//L
    *001L*;
    *000X*;//L
    *001L*;
    *000X*;//L
    *001L*;
    *000X*;//H
    *001H*;
    *0000*;//STOP
    *0010*;
    *0011*;
    *0011*RPT 20;//VPP=0 delay
    *0111*RPT 100;//READ DATA VPP=3.0V
    *0111*TS2;//TS2 = 4uS,I2C start
    *0111*;
    *0110*;
    *0100*;
    *0100*;
    *0101*;//CCIN CC=1
    *0111*;
    *0111*;
    *0101*;
    *0101*;//RWB=1
    *0111*;
    *0111*;
    *0101*;
    *0100*RPT 3;
    *0100*TS7;
"""
patternDataACK = """    *0100*;
    *0110*;//AKI6
"""

patternDataACKForDebug = """    *0100*;
    *0100*;
    *0110*;//AKI6
    *0110*;
    *0100*;
    *0100*;
"""
patternForEnd = """    *0100*TS1;//STOP
    *0110*;
    *0111*;
    *0011*;//VPP=0V
    *0011*;
    *0011*;
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


def writeData2File(data, bitList, byteCnt, fp, debugFlag):
    outputList = ["0"] * 8
    if byteCnt % 2 == 0:
        for i in range(8 - 1, -1, -1):
            if bitList[i] == "1":
                outputList[i] = "H"
            else:
                outputList[i] = "L"
        for i in range(8 - 1, -1, -1):
            if i == 7:
                fp.write(
                    "    *010X*;//addr=%s(%d), data = %s => %s %s\n"
                    % (
                        "0x" + str(hex(byteCnt)[2:].zfill(5)).upper(),
                        byteCnt,
                        "0x" + str(hex(data)[2:].zfill(2)).upper(),
                        "".join(bitList[7:3:-1]),
                        "".join(bitList[-5:-9:-1]),
                    )
                )
                fp.write("    *011%s*;//D%s %s\n" % (outputList[i], i, outputList[i]))
            else:
                if i == 6 and byteCnt == 0x07A7:
                    fp.write("O8M:")
                    fp.write("*010X*;\n")
                    fp.write(
                        "    *011%s*;//D%s %s\n" % (outputList[i], i, outputList[i])
                    )
                    continue
                if i == 5 and byteCnt == 0x07A8:
                    fp.write("O32:")
                    fp.write("*010X*;\n")
                    fp.write(
                        "    *011%s*;//D%s %s\n" % (outputList[i], i, outputList[i])
                    )
                    continue
                fp.write("    *010X*;\n")
                fp.write("    *011%s*;//D%s %s\n" % (outputList[i], i, outputList[i]))
        if not debugFlag:
            fp.write(patternDataACK)
        else:
            fp.write(patternDataACKForDebug)
    else:
        for i in range(8 - 1, -1, -1):
            if bitList[i] == "1":
                outputList[i] = "L"
            else:
                outputList[i] = "H"
        for i in range(8 - 1, -1, -1):
            if i == 7:
                fp.write(
                    "    *010X*;//addr=%s(%d), data = %s => %s %s\n"
                    % (
                        "0x" + str(hex(byteCnt)[2:].zfill(5)).upper(),
                        byteCnt,
                        "0x" + str(hex(data)[2:].zfill(2)).upper(),
                        "".join(bitList[7:3:-1]),
                        "".join(bitList[-5:-9:-1]),
                    )
                )
                fp.write(
                    "    *011%s*;//D%s %s(%s) \n"
                    % (outputList[i], i, outputList[i], bitList[i])
                )
            else:
                if i == 6 and byteCnt == 0x07A7:
                    fp.write("O8M:")
                    fp.write("*010X*;\n")
                    fp.write(
                        "    *011%s*;//D%s %s(%s)\n"
                        % (outputList[i], i, outputList[i], bitList[i])
                    )
                    continue
                if i == 5 and byteCnt == 0x07A8:
                    fp.write("O32:")
                    fp.write("*010X*;\n")
                    fp.write(
                        "    *011%s*;//D%s %s(%s)\n"
                        % (outputList[i], i, outputList[i], bitList[i])
                    )
                    continue
                fp.write("    *010X*;\n")
                fp.write(
                    "    *011%s*;//D%s %s(%s)\n"
                    % (outputList[i], i, outputList[i], bitList[i])
                )
        if not debugFlag:
            fp.write(patternDataACK)
        else:
            fp.write(patternDataACKForDebug)


def data2Pattern(self, dataList, patternFile, debugFlag):
    byteCnt = 0
    bitList = ["0"] * 8
    fileSize = len(dataList)
    with open(patternFile, "a", encoding="UTF-8") as fp:
        fp.write(patternHeadInfo)
        for data in dataList:
            bitList = data2bitList(data)
            writeData2File(data, bitList, byteCnt, fp, debugFlag)
            byteCnt += 1
            if byteCnt % (int(fileSize / 100)) == 0 or byteCnt == fileSize:
                self.labelStatus.setText(
                    f"生成readRom.pat: 共 {int(fileSize/1024)} KB, 已处理 {int(byteCnt/1024)} KB, {int((byteCnt/fileSize)*100)}%"
                )
                self.labelStatus.repaint()
                self.pBar.setValue(int((byteCnt / fileSize) * 100))
        fp.write(patternForEnd)
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


def readRom(self, filePath, fileSize, debugFlag):
    parDir = os.path.dirname(filePath)
    _, file = os.path.split(filePath)
    fileName, _ = os.path.splitext(file)
    srcFile = parDir + "/" + "READ_" + fileName.upper() + ".pat"
    if os.path.exists(srcFile):
        os.remove(srcFile)
    checkFileSize(self, filePath, fileSize)
    dataList = getFileData(filePath)
    byteCnt = data2Pattern(self, dataList, srcFile, debugFlag)
    if byteCnt != fileSize:
        QMessageBox.critical(
            self, "警告", f"生成的{srcFile} 写入字节数不是{fileSize},请确认！！！"
        )
    QMessageBox.information(self, "完成", "readRom 任务完成!")
