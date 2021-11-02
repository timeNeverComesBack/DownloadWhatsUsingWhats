import re
import pymysql
from time import sleep

import readPlainText as p
import readExcel as e

print("""


  ______                        __                __ _______ __          __               ___ ___       __             _______ _______ ___     
 |   _  \ .-----.--.--.--.-----|  .-----.---.-.--|  |   _   |  |--.-----|  |_.-----.-----|   Y   .-----|__.-----.-----|   _   |   _   |   |    
 |.  |   \|  _  |  |  |  |     |  |  _  |  _  |  _  |.  1   |     |  _  |   _|  _  |__ --|.  |   |__ --|  |     |  _  |   1___|.  |   |.  |    
 |.  |    |_____|________|__|__|__|_____|___._|_____|.  ____|__|__|_____|____|_____|_____|.  |   |_____|__|__|__|___  |____   |.  |   |.  |___ 
 |:  1    /                                         |:  |                                |:  1   |              |_____|:  1   |:  1   |:  1   |
 |::.. . /                                          |::.|                                |::.. . |                    |::.. . |::..   |::.. . |
 `------'                                           `---'                                `-------'                    `-------`----|:.`-------'
                                                                                                                                   `--'        


""")
print("请选择下载方法：")
# 支持下载方法列表
methodsArray = ("连接MySQL", "Excel列表", "TXT列表")

# 交互式MySQL登录信息采集
def useMySQLToLoginIn():
    print("请输入主机IP或键入如下组合：")
    print("IP,端口,用户名,密码 (使用一个英文逗号或一个英文空格分隔)")
    loginArray = []
    host = input("请输入：")
    while 1:
        # 输入组合
        if "," in host:
            loginArray = host.split(",")
            for element in loginArray:
                loginArray[loginArray.index(element)] = element.strip()
            if not re.match("[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?", loginArray[0]):
                print("IP格式有误，请重新输入")
                temp = input("请输入IP：")
                while not re.match("[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?", temp):
                    print("IP格式有误，请重新输入")
                    temp = input("请输入IP：")
                loginArray[0] = temp
            else:
                temp = "开始测试端口"
                while 1:
                    try:
                        if 0 <= int(loginArray[1]) <= 65535:
                            break
                        if 0 <= int(temp) <= 65535:
                            loginArray[1] = temp
                            break
                        else:
                            print("端口号的范围应为0-65535，请重新输入!")
                            temp = input("请输入端口：")
                    except:
                        print("非法字符，请重新输入！")
                        temp = input("请输入端口：")
                        loginArray[1] = temp
            break

        if " " in host:
            loginArray = host.split(" ")
            for element in loginArray:
                loginArray[loginArray.index(element)] = element.strip()
            if not re.match("[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?", loginArray[0]):
                print("IP格式有误，请重新输入")
                temp = input("请输入IP：")
                while not re.match("[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?", temp):
                    print("IP格式有误，请重新输入")
                    temp = input("请输入IP：")
                loginArray[0] = temp
            else:
                temp = "开始测试端口"
                while 1:
                    try:
                        if 0 <= int(loginArray[1]) <= 65535:
                            break
                        if 0 <= int(temp) <= 65535:
                            loginArray[1] = temp
                            break
                        else:
                            print("端口号的范围应为0-65535，请重新输入!")
                            temp = input("请输入端口：")
                    except:
                        print("非法字符，请重新输入！")
                        temp = input("请输入端口：")
                        loginArray[1] = temp
            break

        # 依次输入IP，端口，用户名，密码
        if re.match("[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?", host):
            loginArray.append(host)
            port = input("请输入端口：")
            while 1:
                try:
                    if 0 <= int(port) <= 65535:
                        loginArray.append(port)
                        break
                    else:
                        print("端口号的范围应为0-65535，请重新输入!")
                        port = input("请输入端口：")
                except:
                    print("非法字符，请重新输入！")
                    port = input("请输入端口：")

            userName = input("请输入用户名：")
            loginArray.append(userName)
            password = input("请输入密码：")
            loginArray.append(password)
            break
        else:
            print("格式输入有误, 请重新输入：")
            host = input("请输入：")

    return loginArray

# 从文件中读取MySQL连接信息
def readMySQLConnectionFromText():
    print("""
文件格式应为：
数据库服务器地址IP（例：127.0.0.1）
数据库服务器端口PORT（例：3306）
数据库用户名（例：root）
数据库用户密码（例：123456）
数据库名称：（例：db1， 可选）
查询语句：（例：select * from tb1， 可选）
    """
    )
    print("\n请输入文件的相对路径或绝对路径：")
    fileLocation = input("文件位置：")
    with open(fileLocation, "r", encoding='utf-8') as f:
        print(f.read())


# 连接MySQL数据库，获取数据二维表
def useMySQLGetData(loginArray):
    isSelectedDB = input("是否指定数据库：y or n：")
    if isSelectedDB == "y":
        db = input("请输入数据库名称：")

    else:
        print("还是指定一下吧！")
        db = input("请输入数据库名称：")

    sql1 = input("请输入查询语句(还不支持)或查询文件的位置(建议预存为纯文本文件)：")
    try:
        with open(sql1, "r", encoding='utf-8') as f:
            sql1 = f.read()
    except:
        if (re.match("[^select]i", sql1.strip())):
            pass
        else:
            print("查询语句存在格式错误！")

    try:
        link = pymysql.connect(
            host = loginArray[0],
            port = int(loginArray[1]),
            user = loginArray[2],
            password = loginArray[3],
            database = str(db),
            charset = "utf8"
        )
        print("MySQL数据库连接成功")
        cursor = link.cursor()
        try:
            num = cursor.execute(sql1)
            # data = cursor.fetchall()
            data = cursor.fetchone()
            sleep(1)
            print(data)
            print(type(data))
        except:
            print("查询执行失败！")

    except:
        print("MySQL数据库连接失败！")

# 输出方法列表
def outputMethodsArray(methodsArray):
    i = 0
    for element in methodsArray:
        print(str(i).rjust(2) + ". " + element )
        i += 1

outputMethodsArray(methodsArray)

# 监听键盘输入，输入方法列表的序号
def inputMethodsArrayId(methodsArray):
    id = input("请选择下载方法的序号：")
    while 1:
        try:
            if 0 <= int(id) <= len(methodsArray) - 1:
                return int(id)
                break
            else:
                id = input("不在范围内，请重新选择下载方法的序号：")
        except:
            id = input("非数字，请重新选择下载方法的序号：")

# 下载方法入点
def methodEnterPoint(id, methodsArray):
    if methodsArray[id] == "连接MySQL":
        print("请选择：1.交互式填写连接信息 2.从文件中读取连接信息（还没写好）")
        choice = input("请选择 1 或者 2：")
        while not (choice == "1" or choice == "2"):
            choice = input("请选择 1 或者 2：")
        if int(choice) == 1:
            loginArray = useMySQLToLoginIn()
            print("当前连接信息为：")
            print("数据库服务器地址：" + loginArray[0])
            print("数据库服务器端口：" + loginArray[1])
            print("数据库用户名：" + loginArray[2])
            print("数据库用户密码：" + loginArray[3])
            useMySQLGetData(loginArray)
        elif int(choice) == 2:
            readMySQLConnectionFromText()

    elif methodsArray[id] == "Excel列表":
        e.readExcel()
    elif methodsArray[id] == "TXT列表":
        p.readPlainText()

methodEnterPoint(inputMethodsArrayId(methodsArray), methodsArray)
