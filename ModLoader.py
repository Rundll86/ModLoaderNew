print("ModLoaderNew v1.3.2")
print("编写与开发 By <Rundll86> [ https://rundll86.github.io/ ]")
print("项目仓库 With <Github> [ https://github.com/Rundll86/ModLoaderNew/ ]")
print("！此程序是免费且开源的，如果你是付费购买的，那么你已经被骗了！")
print("")
print("正在初始化...")
from zipfile import *
import os, shutil, msvcrt, subprocess, threading, time, sys, tempfile, conkits, json


def clearConsole():
    os.system("cls")


def RunAsPowerShell(Cmd):
    subprocess.run(Cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def popPath(path: str):
    return "\\".join(path.split("\\")[1:])


def aData(i):
    path = i + "___EXTRACT"
    ZipFile(i).extractall(path)
    RunAsPowerShell(f'del /s /q "{i}"')
    src_dir = path
    suffix = "Mod"
    dest_dir = "mods"
    for root, dirs, files in os.walk(src_dir):
        for dir in dirs:
            dir: str
            if (suffix in dir) and ("Mods" not in dir):
                src_path = os.path.join(root, dir)
                dest_path = os.path.join(dest_dir, dir)
                shutil.copytree(src_path, dest_path)
    directory_name = "ShaderFixes"
    directory_path = os.path.join(src_dir, directory_name)
    dest_path = os.path.join(dest_dir, "..\\shaderFix")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            src_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest_path, file)
            shutil.copy2(src_file_path, dest_file_path)
    test_directory_path = src_dir
    for file in os.listdir(test_directory_path):
        src_file_path = os.path.join(test_directory_path, file)
        dest_file_path = os.path.join(dest_dir, file)
        if os.path.isfile(src_file_path):
            shutil.copy2(src_file_path, dest_file_path)
    RunAsPowerShell(f'rmdir /s /q "{path}"')
    print(f" - 安装成功「{i}」。")
    global finish
    finish += 1


def checkGame(path):
    for root, dir, file in os.walk(path):
        if "YuanShen.exe" in file or "GenshinImpact.exe" in file:
            if "YuanShen.exe" in file:
                gametype = "YuanShen"
            if "GenshinImpact.exe" in file:
                gametype = "GenshinImpact"
            gamepath = os.path.join(root, f"{gametype}.exe")
            print(f"已找到「{gametype}.exe」，其在 [ {gamepath} ] 。")
            global stime
            print(f"用时：{round(time.time()-stime,2)}秒。")
            print("这是你的游戏吗？")
            print("\x1b[33m↓ 使用箭头键切换，回车键确认 ↓\x1b[0m")
            selector = conkits.Choice(options=["* 是   *", "* 不是 *"])
            selector.set_keys({"up": "H", "down": "P", "confirm": "\r"})
            selector.checked_ansi_code = (
                conkits.Colors256.BACK255 + conkits.Colors256.FORE0
            )
            selector.unchecked_ansi_code = conkits.Colors256.FORE255
            selector.click_ansi_code = (
                conkits.Colors256.BACK255 + conkits.Colors256.FORE0
            )
            selected = not selector.run()
            if selected:
                global ok
                ok = True
                break
            else:
                stime = time.time()
                print("正在重新查找...")
    if ok:
        return gamepath
    else:
        return ""


def autoInstall():
    print("正在自动安装模组...", end="")
    modlist = os.listdir("autoInstall")
    if len(modlist) > 0:
        print("")
        global stime, waittime, finish
        stime = time.time()
        for i in range(len(modlist)):
            modlist[i] = os.path.join("autoInstall", modlist[i])
        waittime = 0
        finish = 0
        for i in modlist:
            if os.path.isdir(i):
                print(f"   - 跳过安装「{os.path.basename(i)}」，其不是有效的模组文件。")
                continue
            try:
                ZipFile(i)
            except:
                print(f"   - 跳过安装「{os.path.basename(i)}」，其不是有效的模组文件。")
                continue
            waittime += 1
            print(f" - 开始安装「{i}」。")
            threading.Thread(target=lambda: aData(i)).start()
        while waittime != finish:
            pass
        print(f"用时：{round(time.time()-stime,2)}秒。")
    else:
        print("好吧，并没有。")


def loadmod():
    print("正在加载模组...")
    RunAsPowerShell(f"rmdir /s /q {dmodspath}")
    shutil.copytree("mods", dmodspath)


def fixmod():
    print("正在运行模组修复工具...")
    RunAsPowerShell(f"copy dontDeleteMe\\assets\\Fixing.exe {dmodspath}")
    RunAsPowerShell("start " + os.path.join(dmodspath, "Fixing.exe"))
    RunAsPowerShell(f"del /s /q {os.path.join(dmodspath,'Fixing.exe')}")


def loadsf():
    print("正在加载渲染数据...")
    RunAsPowerShell(f"rmdir /s /q {dsfpath}")
    RunAsPowerShell(f"mkdir {dsfpath}")
    ddmlist = os.listdir("dontDeleteMe")
    ddmlist.remove("assets")
    for i in ddmlist:
        RunAsPowerShell(f"copy dontDeleteMe\\{i} {dsfpath}")
    for i in os.listdir("shaderFix"):
        RunAsPowerShell(f"copy dontDeleteMe\\{i} {dsfpath}")


def resetConfig():
    RunAsPowerShell("del /s /q game.txt")
    RunAsPowerShell("del /s /q setting.json")


def getASwitch():
    print("选择开关状态：")
    switch = conkits.Choice(options=["* 开 *", "* 关 *"])
    switch.set_keys({"up": "H", "down": "P", "confirm": "\r"})
    switch.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    switch.unchecked_ansi_code = conkits.Colors256.FORE255
    switch.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    return not switch.run()


def launchSetting():
    def quitSetting():
        pass

    def gameConfirm():
        print("")
        settings["confirm_game"] = getASwitch()
        json.dump(settings, open("setting.json", "w", encoding="utf8"))
        launchSetting()

    def modConfirm():
        print("")
        settings["confirm_modloader"] = getASwitch()
        json.dump(settings, open("setting.json", "w", encoding="utf8"))
        launchSetting()

    def setGame():
        pass

    clearConsole()
    print("\n< ModLoaderNew-设置 >")
    setting = conkits.Choice(
        options=[
            "* 退出设置                        *",
            "* 拉起游戏时按键确认       <开关> *",
            "* 拉起模组加载器时按键确认 <开关> *",
            "* 游戏路径                 <文本> *",
        ],
        methods=[quitSetting, gameConfirm, modConfirm, setGame],
    )
    setting.set_keys({"up": "H", "down": "P", "confirm": "\r"})
    setting.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    setting.unchecked_ansi_code = conkits.Colors256.FORE255
    setting.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    setting.run()


print("正在加载配置文件...")
if not os.path.exists("game.txt"):
    print("检测到配置文件不存在，正在生成...")
    print("正在自动查找游戏...")
    print("这个步骤「可能」需要很长时间，请耐心等待。")
    stime = time.time()
    disklist = "DEFGHIJKLMNOPQRSTUVWXYZ"
    ok = False
    gamepath = ""
    for i in disklist:
        if os.path.exists(f"{i}:\\"):
            result = checkGame(f"{i}:\\")
            if result == "":
                ok = False
            else:
                ok = True
                gamepath = result
                break
        else:
            continue
    if not ok:
        Cdirlist = os.listdir("C:\\")
        Cdirlist.remove("Windows")
        for i in Cdirlist:
            result = checkGame("C:\\" + i)
            if result == "":
                ok = False
            else:
                ok = True
                gamepath = result
                break
    if ok:
        print("正在写入配置文件...")
        config = open("game.txt", "w", encoding="utf8")
        config.write(gamepath)
        config.close()
    else:
        print("没有在你的电脑中找到YuanShen.exe或GenshinImpact.exe，请确认你的电脑中已经安装了《原神》！")
        print("按下任意键退出。")
        msvcrt.getch()
        sys.exit()
if not os.path.exists("setting.json"):
    json.dump(
        {"confirm_game": False, "confirm_modloader": False},
        open("setting.json", "w", encoding="utf8"),
    )
config = open("game.txt", "r", encoding="utf8").read()
gamepath = config
settings = json.load(open("setting.json", encoding="utf8"))
tconfigpath = "dontDeleteMe\\assets\\d3dx.ini"
temppath = os.path.join(tempfile.gettempdir(), "ModLoaderNew")
dconfigpath = os.path.join(temppath, "3dmigoto\\d3dx.ini")
dmodspath = os.path.join(temppath, "3dmigoto\\Mods")
dsfpath = os.path.join(temppath, "3dmigoto\\ShaderFixes")
cg = open(tconfigpath, encoding="utf8")
data = cg.read().format(GamePath=config)
print("正在加载核心脚本...")
ZipFile("dontDeleteMe/assets/core.ddm").extractall(temppath)
open(dconfigpath, "w", encoding="utf8").write(data)
autoInstall()
loadmod()
fixmod()
loadsf()
print("准备拉起模组加载器...", end="")
if settings["confirm_modloader"]:
    print("请按下任意键继续。")
    msvcrt.getch()
else:
    print("")
cd = os.path.abspath(os.curdir)
os.chdir(os.path.join(temppath, "3dmigoto"))
os.startfile("3DMigoto Loader.exe")
print("请检查新出现的窗口，如果出现了“Now run the game.”则模组加载器已经启动成功。")
print("准备拉起你的游戏...", end="")
if settings["confirm_game"]:
    print("请按下任意键继续。")
    msvcrt.getch()
else:
    print("")
try:
    os.startfile(config)
    print("游戏已启动！按下任意键进入操作面板")
    msvcrt.getch()
except Exception as Error:
    print("启动失败，可能是游戏文件不存在或已经损坏，请检查game.txt中的路径是否有效。")
    print("按下任意键退出。")
    msvcrt.getch()
    sys.exit()
console = conkits.Choice(
    options=[
        "* 退出程序         *",
        "* 重置配置文件     *",
        "* 进入设置         *",
        "* 自动安装模组     *",
        "* 重新加载模组     *",
        "* 重新加载渲染数据 *",
        "* 运行模组修复工具 *",
    ],
    methods=[
        sys.exit,
        resetConfig,
        launchSetting,
        autoInstall,
        loadmod,
        loadsf,
        fixmod,
    ],
)
console.set_keys({"up": "H", "down": "P", "confirm": "\r"})
console.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
console.unchecked_ansi_code = conkits.Colors256.FORE255
console.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
os.chdir(cd)
clearConsole()
while True:
    print("< ModLoaderNew-操作面板 >")
    print(f"\n游戏路径：[ {gamepath} ]\n模组加载器：[ 注入成功 ]")
    print("\n可执行的操作...\n")
    print("\x1b[33m↓ 使用箭头键切换，回车键确认 ↓\x1b[0m")
    console.run()
    print("完成。")
    print("按下任意键继续...")
    msvcrt.getch()
    clearConsole()
