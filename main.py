import re

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

# MySQL登录信息采集
def useMySQLToLoginIn():
    print("请输入主机IP或键入如下组合：")
    print("IP, 端口, 用户名, 密码 (使用英文逗号分隔，允许使用空格)")
    loginArray = []
    host = input("请输入：")
    while 1:
        # 输入组合
        if "," in host:
            loginArray = host.split(",")
            if not re.match("[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?", loginArray[0]):
                print("IP格式有误，请重新输入")
                temp = input("请输入IP：")
                while not re.match("[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?\.[0-2]?[0-9]?[0-9]?", temp):
                    print("IP格式有误，请重新输入")
                    temp = input("请输入IP：")
                loginArray[0] = temp
            else:
                try:
                    if 0 <= int(loginArray[1]) <= 65535:
                        pass
                    else:
                        print("端口号的范围应为0-65535，请重新输入!")
                        temp = input("请输入端口：")
                        while not 0 <= temp <= 65535:
                            print("端口号的范围应为0-65535，请重新输入!")
                            temp = input("请输入端口：")
                except:

            break
        # 依次输入ip
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

# 

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
        loginArray = useMySQLToLoginIn()
        for i in loginArray:
            print(i)

    elif methodsArray[id] == "Excel列表":
        print("打开Excel文件……")
    elif methodsArray[id] == "TXT列表":
        print("打开TXT文件……")

methodEnterPoint(inputMethodsArrayId(methodsArray), methodsArray)
