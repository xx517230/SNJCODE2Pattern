import os
import struct


class SNJCodeConverter(object):
    filePath = ""

    def __init__(self):
        super().__init__()

    def __init__(self, filePath):
        super().__init__()
        self.filePath = filePath
        self.toHexTxtFile()

    def txtToHexBinFile(self):
        pass

    def toHexTxtFile(self):
        if not self.filePath:
            return False
        fileName, _ = os.path.splitext(self.filePath)
        # 用rb打开filePath,以二进制方式读取,并将每个byte转换为对应的16进制字符
        with open(self.filePath, "rb") as fp:
            hexContent = [hex(byte)[2:].zfill(2) for byte in fp.read()]
            with open(fileName + ".txt", "w") as hexFile:
                for cnt, hexNum in enumerate(hexContent, start=1):
                    hexFile.write("0x" + str(hexNum).upper())
                    if cnt % 16 == 0:
                        hexFile.write("\n")
                    else:
                        hexFile.write(",")

    def txtToBinFile(self):
        if not self.filePath:
            return False
        fileName, _ = os.path.splitext(self.filePath)

        # 用rb打开filePath,以二进制方式读取,并将每个byte转换为对应的16进制字符
        with open(self.filePath, "r") as fp:
            fileStr = fp.read()

        hexList = [hexStr.strip() for hexStr in fileStr.split("\n")]
        print(hexList)
        for line in hexList:
            for data in line.split(","):
                print(data)

        with open(fileName + ".dat", "wb") as hexFile:
            for line in hexList:
                for data in line.split(","):
                    if data:
                        hexFile.write(struct.pack("H", int(data, 16)))
