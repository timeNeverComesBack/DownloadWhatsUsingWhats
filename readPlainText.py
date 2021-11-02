def readPlainText():
    print("请输入纯文本文件位置：")
    fileLocation = input("请输入：")
    with open(fileLocation, "r", encoding="utf-8") as f:
