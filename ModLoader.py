import os, json, ctypes, win32api, sys


def clearConsole():
    os.system("title ModLoaderNew")
    os.system("cls")


if not ctypes.windll.shell32.IsUserAnAdmin():
    win32api.ShellExecute(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

clearConsole()
infos = json.load(open("dontDeleteMe/assets/info.json", encoding="utf8"))
print(f"ModLoaderNew v{infos['version']}")
print("编写与开发 By <Rundll86> [ https://rundll86.github.io/ ]")
print("项目仓库 With <Github> [ https://github.com/Rundll86/ModLoaderNew/ ]")
print("！此程序是免费且开源的，如果你是付费购买的，那么你已经被骗了！")
print("")
print("正在初始化...")
os.environ["UNRAR_LIB_PATH"] = os.path.abspath("dontDeleteMe\\assets\\UnRAR64.dll")
from zipfile import *
from unrar import rarfile
from io import BytesIO
from PIL import Image
import shutil, msvcrt, subprocess, threading, time, tempfile, conkits, json, winreg, configparser, tarfile, requests, py7zr, winshell


def RunAsPowerShell(Cmd):
    subprocess.run(Cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


for root, dirs, files in os.walk("."):
    for i in files:
        if i == "thereIsSomething":
            RunAsPowerShell(f'del /s /q "{os.path.join(root,i)}"')


def extractfile(path, outdir):
    filetype: str = os.path.splitext(path)[1]
    filetype = filetype.strip(".")
    supporttype = ["zip", "rar", "tar", "7z"]
    if filetype not in supporttype:
        raise Exception("file not supported.")
    if filetype == "zip":
        ZipFile(path).extractall(outdir)
    if filetype == "rar":
        rarfile.RarFile(path).extractall(outdir)
    if filetype == "tar":
        tarfile.TarFile(path).extractall(outdir)
    if filetype == "7z":
        py7zr.SevenZipFile(path).extractall(outdir)


def aData(i):
    try:
        global needdelete
        extractfile(i, "mods")
        for root, dirs, files in os.walk("mods"):
            if "SHADERFIX" in os.path.basename(root).upper():
                for j in os.listdir(root):
                    if os.path.isfile(os.path.join(root, j)):
                        shutil.copy(os.path.join(root, j), os.path.abspath("shaderFix"))
                    else:
                        shutil.copy(os.path.join(root, j), "shaderFix")
                needdelete.append(root)
        RunAsPowerShell(f'del /s /q "{i}"')
        print(f" - 安装成功「{os.path.basename(i)}」。")
    except Exception as Error:
        print(f" - 安装失败「{os.path.basename(i)}」，其不是有效的模组文件。")
        print(Error)
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
                print("\n正在重新查找...\n")
    if ok:
        return gamepath
    else:
        return ""


def autoInstall():
    print("正在自动安装模组...", end="")
    modlist = os.listdir("autoInstall")
    if len(modlist) > 0:
        print("")
        global stime, waittime, finish, needdelete
        needdelete = []
        stime = time.time()
        for i in range(len(modlist)):
            modlist[i] = os.path.join("autoInstall", modlist[i])
        waittime = 0
        finish = 0
        for i in modlist:
            waittime += 1
            print(f" - 开始安装「{os.path.basename(i)}」。")
            threading.Thread(target=lambda: aData(i)).start()
        while waittime > finish:
            pass
        for i in needdelete:
            RunAsPowerShell(f'rmdir /s /q "{i}"')
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
    os.chdir(dmodspath)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen(
        "Fixing.exe",
        startupinfo=startupinfo,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    os.chdir(cd)


def fixmod_legacy():
    print("正在运行模组修复工具（传统模式）...")
    RunAsPowerShell(f"copy dontDeleteMe\\assets\\Fixing_legacy.exe {dmodspath}")
    os.chdir(dmodspath)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen(
        "Fixing_legacy.exe",
        startupinfo=startupinfo,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    os.chdir(cd)


def loadsf():
    print("正在加载渲染数据...")
    RunAsPowerShell(f"rmdir /s /q {dsfpath}")
    RunAsPowerShell(f"mkdir {dsfpath}")
    helpshort = (
        open("dontDeleteMe/assets/help_short.txt", encoding="utf8")
        .read()
        .format(version=infos["version"])
    )
    open("dontDeleteMe/help_short.txt", "w", encoding="utf8").write(helpshort)
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

    def switchDebug():
        print("")
        settings["debug_mode"] = getASwitch()
        json.dump(settings, open("setting.json", "w", encoding="utf8"))
        launchSetting()

    clearConsole()
    print("< ModLoaderNew-设置 >")
    setting = conkits.Choice(
        options=[
            "* 退出设置                        *",
            "* 拉起游戏时按键确认       <开关> *",
            "* 拉起模组加载器时按键确认 <开关> *",
            "* 是否启用调试模式         <开关> *",
        ],
        methods=[quitSetting, gameConfirm, modConfirm, switchDebug],
    )
    setting.set_keys({"up": "H", "down": "P", "confirm": "\r"})
    setting.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    setting.unchecked_ansi_code = conkits.Colors256.FORE255
    setting.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    setting.run()


def findGame_methodA():
    try:

        def pathExists(path):
            try:
                winreg.CloseKey(
                    winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ)
                )
                return True
            except:
                return False

        print("正在查找游戏路径（方式A）...")
        uninstallPath = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{}"
        availablePath = []
        if pathExists(uninstallPath.format("Genshin Impact")):
            availablePath.append(uninstallPath.format("Genshin Impact"))
        if pathExists(uninstallPath.format("原神")):
            availablePath.append(uninstallPath.format("原神"))
        global ok
        ok = False
        if len(availablePath) == 0:
            return ""
        gamepath = ""
        for i in availablePath:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, i, 0, winreg.KEY_READ)
            data = os.path.join(
                winreg.QueryValueEx(key, "InstallPath")[0], "config.ini"
            )
            parser = configparser.ConfigParser()
            parser.read(data)
            gamepath = os.path.join(
                parser["launcher"]["game_install_path"],
                parser["launcher"]["game_start_name"],
            )
            print(f"已找到「{parser['launcher']['game_start_name']}」，其在 [ {gamepath} ] 。")
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
                ok = True
                break
            else:
                print("\n正在重新查找...\n")
        return gamepath
    except:
        print("糟糕，出错了。")
        ok = False
        return ""


def findGame_methodB():
    print("正在查找游戏路径（方式B）...")
    print("这个步骤「可能」需要很长时间，请耐心等待。")
    global stime, disklist, ok, gamepath
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
        return gamepath
    else:
        return ""


def generateConfig(exit=True):
    global gamepath, config, ok
    gamepath = findGame_methodA()
    if not ok:
        gamepath = findGame_methodB()
    if ok:
        print("正在写入配置文件...")
        config = open("game.txt", "w", encoding="utf8")
        config.write(gamepath)
        config.close()
    else:
        print("没有在你的电脑中找到YuanShen.exe或GenshinImpact.exe，请确认你的电脑中已经安装了《原神》！")
        print(f"按下任意键{'退出' if exit else '继续'}。")
        msvcrt.getch()
        if exit:
            sys.exit()


def killGame():
    print("请先确保你的游戏资料已经保存！（例如尘歌壶建筑、活动奖励等）")
    print("按下任意键继续...")
    msvcrt.getch()
    RunAsPowerShell("taskkill /f /im YuanShen.exe")
    RunAsPowerShell("taskkill /f /im GenshinImpact.exe")
    RunAsPowerShell('taskkill /f /im "3DMigoto Loader.exe"')


def repeatlist(_object, count):
    result = []
    for i in range(count):
        result.append(_object)
    return result


def downloadMod(page=1, search="", searching=False, listing=False):
    global needreturn
    clearConsole()
    print("< ModLoaderNew-模组下载器 >")
    print("此功能正在实验，可能会出现一些问题。")
    print("请选择浏览模式：")
    if (not searching) and (not listing):
        selector = conkits.Choice(options=["* 按关键词搜索   *", "* 最新发布的模组 *"])
        selector.set_keys({"up": "H", "down": "P", "confirm": "\r"})
        selector.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        selector.unchecked_ansi_code = conkits.Colors256.FORE255
        selector.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        mode = selector.run()
    if searching:
        mode = 0
    if listing:
        mode = 1
    try:
        if mode:
            print(f"正在获取模组列表(第{page}页)...")
            jsondata = json.loads(
                requests.get(
                    f"https://gamebanana.com/apiv11/Game/8552/Subfeed?_sSort=default&_nPage={page}"
                ).text
            )
            print("获取成功！")
        else:
            if not searching:
                while True:
                    keyword = input("请输入关键词：")
                    if keyword.strip(" ") == "":
                        print("关键词不能为空！")
                    else:
                        break
            else:
                keyword = search
            print(f"正在使用关键词「{keyword}」搜索模组(第{page}页)...")
            jsondata = json.loads(
                requests.get(
                    f"https://gamebanana.com/apiv11/Game/8552/Subfeed?_sSort=default&_sName={keyword}&_nPage={page}"
                ).text
            )
            print("搜索完成！\n")
        result = []
        for i in jsondata["_aRecords"]:
            if i["_sModelName"] == "Mod":
                result.append(
                    {
                        "name": i["_sName"],
                        "author": i["_aSubmitter"]["_sName"],
                        "id": i["_idRow"],
                        "face": i["_aPreviewMedia"]["_aImages"][0]["_sBaseUrl"]
                        + "/"
                        + i["_aPreviewMedia"]["_aImages"][0]["_sFile"],
                    }
                )
        if len(result) == 0:
            print("已经到达最后一页！")
            print("按下任意键返回操作面板...")
            msvcrt.getch()
            needreturn = True
            return
        print("请选择你要安装的模组：")
        temp = [i["name"] for i in result]
        temp.insert(0, "[ 切换上一页 -> ]")
        temp.insert(0, "[ 切换下一页 -> ]")

        def newpage():
            downloadMod(
                page + 1,
                keyword if mode == 0 else search,
                not mode,
                mode,
            )
            global needreturn
            needreturn = True

        def lastpage():
            global needreturn
            if page == 1:
                print("已经到达最前一页！")
                print("按下任意键返回操作面板...")
                msvcrt.getch()
                needreturn = True
                return
            downloadMod(
                page - 1,
                keyword if mode == 0 else search,
                not mode,
                mode,
            )
            needreturn = True

        methods = [newpage, lastpage]
        selector = conkits.Choice(
            options=temp,
            methods=methods,
        )
        selector.set_keys({"up": "H", "down": "P", "confirm": "\r"})
        selector.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        selector.unchecked_ansi_code = conkits.Colors256.FORE255
        selector.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        print("")
        modid = selector.run() - 2
        try:
            if needreturn:
                del needreturn
                return
        except:
            pass
        print("")
        print(f"模组名：{result[modid]['name']}")
        print(f"模组作者：{result[modid]['author']}")
        print("正在下载模组封面...")
        img = Image.open(BytesIO(requests.get(result[modid]["face"]).content))
        print("下载完成！\n模组封面：")
        printImage(img, 50)
        print("你要下载这个模组吗？")
        print("")
        selector = conkits.Choice(options=["* 确定 *", "* 取消 *"])
        selector.set_keys({"up": "H", "down": "P", "confirm": "\r"})
        selector.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        selector.unchecked_ansi_code = conkits.Colors256.FORE255
        selector.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        confirm = selector.run()
        if confirm:
            print("按下任意键返回操作面板...")
            msvcrt.getch()
            needreturn = True
            return
        print(f"正在下载「{result[modid]['name']}」...")
        files = json.loads(
            requests.get(
                f"https://gamebanana.com/apiv11/Mod/{result[modid]['id']}/DownloadPage"
            ).text
        )["_aFiles"]
        index = 0
        if len(files) > 1:
            print("此模组有多个文件，你要下载哪一个？")
            selector = conkits.Choice(
                options=[
                    "文件名："
                    + i["_sFile"]
                    + "，文件大小："
                    + str(round(i["_nFilesize"] / 1024 / 1024, 2))
                    + "MB"
                    for i in files
                ]
            )
            selector.set_keys({"up": "H", "down": "P", "confirm": "\r"})
            selector.checked_ansi_code = (
                conkits.Colors256.BACK255 + conkits.Colors256.FORE0
            )
            selector.unchecked_ansi_code = conkits.Colors256.FORE255
            selector.click_ansi_code = (
                conkits.Colors256.BACK255 + conkits.Colors256.FORE0
            )
            index = selector.run()
            print("正在开始下载...")
        print("如果文件太大，下载将会耗费很长时间，请耐心等待。")
        open("autoInstall/" + files[index]["_sFile"], "wb").write(
            requests.get(files[index]["_sDownloadUrl"]).content
        )
        print("下载完成！使用自动安装模组功能即可！")
        print("按下任意键返回操作面板...")
        msvcrt.getch()
    except Exception as Error:
        print("糟糕，出错了。请检查你的网络是否正常。")
        print("错误信息：" + str(Error))
        print("按下任意键返回操作面板...")
        msvcrt.getch()


def striplist(target: list):
    result = []
    for i in target:
        if i not in result:
            result.append(i)
    return result


def manageMod():
    def renamemod():
        newname = input("\n请输入新的模组名：")
        try:
            os.chdir(os.path.dirname(modlist[modid][1]))
            os.renames(modlist[modid][1], newname)
            os.chdir(cd)
            print("重命名成功！")
        except Exception as E:
            print("重命名失败。")
            print(f"错误：{E}")

    def deletemod():
        print("\n你确定要删除此模组及其子模组？")
        selector2 = conkits.Choice(options=["* 确定 *", "* 取消 *"])
        selector2.set_keys({"up": "H", "down": "P", "confirm": "\r"})
        selector2.checked_ansi_code = (
            conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        )
        selector2.unchecked_ansi_code = conkits.Colors256.FORE255
        selector2.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        selected = not selector2.run()
        if selected:
            try:
                RunAsPowerShell(f'rmdir /s /q "{modlist[modid][1]}"')
                print(f"已删除「{modlist[modid][0]}」。")
            except Exception as E:
                print("删除失败。")
                print(f"错误：{E}")
        else:
            return

    def changemod():
        print("\nHash信息非常重要，如果不懂怎么改的请不要乱动！")
        moddata = configparser.ConfigParser()
        moddata.read(os.path.join(modlist[modid][1], modlist[modid][2]))
        print("请选择你要更改的配置文件节：")
        moddataSec = moddata.sections()
        selector2 = conkits.Choice(options=moddataSec)
        selector2.set_keys({"up": "H", "down": "P", "confirm": "\r"})
        selector2.checked_ansi_code = (
            conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        )
        selector2.unchecked_ansi_code = conkits.Colors256.FORE255
        selector2.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        selected = selector2.run()
        print("\n请选择你要更改的键：")
        keylist = [key[0] for key in moddata.items(moddataSec[selected])]
        selector2 = conkits.Choice(options=keylist)
        selector2.set_keys({"up": "H", "down": "P", "confirm": "\r"})
        selector2.checked_ansi_code = (
            conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        )
        selector2.unchecked_ansi_code = conkits.Colors256.FORE255
        selector2.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
        selected2 = selector2.run()
        print(f"\n当前值：{moddata[moddataSec[selected]][keylist[selected2]]}")
        newvalue = input("请输入新的值（为空则取消）：")
        if newvalue.strip(" ") == "":
            print("已取消。")
        else:
            moddata[moddataSec[selected]][keylist[selected2]] = newvalue
            moddata.write(
                open(
                    os.path.join(modlist[modid][1], modlist[modid][2]),
                    "w",
                    encoding="utf8",
                )
            )
            print("写入成功！")

    clearConsole()
    print("< ModLoaderNew-模组管理器 >")
    print("正在搜索模组目录...")
    modlist = []
    for root, dirs, files in os.walk("mods"):
        for i in files:
            if i.endswith(".ini") and len(i) > 4:
                if "BUFFERVALUE" in os.path.basename(root):
                    continue
                modlist.append([os.path.basename(root), os.path.abspath(root), i])
    modlist = striplist(modlist)
    if len(modlist) == 0:
        print("你还没有安装任何模组！")
        print("按下任意键返回操作面板...")
        msvcrt.getch()
        return
    print("请选择要更改的模组")
    selector = conkits.Choice(options=[i[0] for i in modlist])
    selector.set_keys({"up": "H", "down": "P", "confirm": "\r"})
    selector.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    selector.unchecked_ansi_code = conkits.Colors256.FORE255
    selector.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    modid = selector.run()
    print("")
    print(f"模组名称：{modlist[modid][0]}")
    print(f"模组路径：[ {modlist[modid][1]} ]")
    print(f"模组配置文件名：[ {modlist[modid][2]} ]")
    print("")
    print("请选择你要进行的操作")
    selector = conkits.Choice(
        options=[
            "* 重命名模组         *",
            "* 删除此模组         *",
            "* 更改模组的Hash信息 *",
            "* 取消操作           *",
        ],
        methods=[renamemod, deletemod, changemod],
    )
    selector.set_keys({"up": "H", "down": "P", "confirm": "\r"})
    selector.checked_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    selector.unchecked_ansi_code = conkits.Colors256.FORE255
    selector.click_ansi_code = conkits.Colors256.BACK255 + conkits.Colors256.FORE0
    selector.run()
    print("按下任意键返回操作面板...")
    msvcrt.getch()


def manageGame():
    clearConsole()
    print("< ModLoaderNew-游戏路径搜索器 >\n")
    global gamepath
    gamepathbackup = gamepath
    generateConfig(False)
    if not ok:
        gamepath = gamepathbackup


def printImage(img: Image.Image, width):
    img = img.resize((width, round(img.size[1] / img.size[0] * (width / 2))))
    pixels = img.load()
    RESET = "\033[0m"
    ANSI_COLOR = "\033[38;2;{r};{g};{b}m"
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            cpixel = pixels[x, y]
            if len(cpixel) == 3:
                r, g, b = cpixel
            else:
                r, g, b, _ = cpixel
            color_code = ANSI_COLOR.format(r=r, g=g, b=b)
            sys.stdout.write(color_code + "█")
        sys.stdout.write(RESET + "\n")


print("正在加载配置文件...")
if not os.path.exists("game.txt"):
    print("检测到配置文件不存在，正在生成...")
    generateConfig(True)
if not os.path.exists("setting.json"):
    json.dump(
        {"confirm_game": False, "confirm_modloader": False, "debug_mode": False},
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
cd = os.path.abspath(os.curdir)
print("正在加载核心脚本...")
ZipFile("dontDeleteMe/assets/core.ddm").extractall(temppath)
open(dconfigpath, "w", encoding="utf8").write(data)
autoInstall()
loadmod()
fixmod()
loadsf()
print("准备拉起模组加载器...", end="")
if not settings["debug_mode"]:
    if settings["confirm_modloader"]:
        print("请按下任意键继续。")
        msvcrt.getch()
    else:
        print("")
    os.chdir(os.path.join(temppath, "3dmigoto"))
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen(
        "3dMigoto Loader.exe",
        startupinfo=startupinfo,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    os.chdir(cd)
else:
    print("处于调试模式，操作取消。")
print("准备拉起你的游戏...", end="")
if not settings["debug_mode"]:
    if settings["confirm_game"]:
        print("请按下任意键继续。")
        msvcrt.getch()
    else:
        print("")
    try:
        os.startfile(config)
        print("游戏已启动！游戏窗口稍后将会出现。\n按下任意键进入操作面板。")
        msvcrt.getch()
    except Exception as Error:
        print("启动失败，可能是游戏文件不存在或已经损坏，请检查game.txt中的路径是否有效。")
        print("按下任意键退出。")
        msvcrt.getch()
        sys.exit()
else:
    print("处于调试模式，操作取消。")
    print("按下任意键进入操作面板。")
    msvcrt.getch()
console = conkits.Choice(
    options=[
        "* 退出程序         *",
        "* 退出《原神》     *",
        "* 重置配置文件     *",
        "* 进入设置         *",
        "* 自动安装模组     *",
        "* 重新加载模组     *",
        "* 重新加载渲染数据 *",
        "* 修复模组         *",
        "* 修复模组（传统） *",
        "* 模组下载器       *",
        "* 模组管理器       *",
        "* 修改游戏路径     *",
    ],
    methods=[
        lambda: (print("正在清理数据..."), sys.exit()),
        killGame,
        resetConfig,
        launchSetting,
        autoInstall,
        loadmod,
        loadsf,
        fixmod,
        fixmod_legacy,
        downloadMod,
        manageMod,
        manageGame,
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
    print(f"\n游戏路径：[ {gamepath} ]\n模组加载器：[ 已注入 ]")
    print("\n可执行的操作...\n")
    print("\x1b[33m↓ 使用箭头键切换，回车键确认 ↓\x1b[0m")
    console.run()
    print("完成。")
    print("按下任意键继续...")
    msvcrt.getch()
    clearConsole()
