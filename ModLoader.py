print("ModLoader New v1.3.0 (!-Alpha)")
print("编写与开发 By <Rundll86> [ https://rundll86.github.io/ ]")
print("项目仓库 With <Github> [ https://github.com/Rundll86/ModLoaderNew/ ]")
print("！此程序是免费且开源的，如果你是付费购买的，那么你已经被骗了！")
print("")
print("正在初始化...")
from zipfile import *
import os, shutil, msvcrt, subprocess, threading, time, sys, tempfile


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


print("正在加载配置文件...")
if not os.path.exists("game.txt"):
    print("检测到配置文件不存在，正在生成...")
    print("正在自动查找游戏...")
    print("这个步骤「可能」需要很长时间，请稍等。")
    stime = time.time()
    disklist = "DEFGHIJKLMNOPQRSTUVWXYZ"
    ok = False
    gamepath = ""
    for i in disklist:
        if os.path.exists(f"{i}:\\"):
            for root, dir, file in os.walk(f"{i}:\\"):
                if "YuanShen.exe" in file or "GenshinImpact.exe" in file:
                    if "YuanShen.exe" in file:
                        gametype = "YuanShen"
                        gamepath = os.path.join(root, "YuanShen.exe")
                    if "GenshinImpact.exe" in file:
                        gametype = "GenshinImpact"
                        gamepath = os.path.join(root, "GenshinImpact.exe")
                    ok = True
                    print(f"已找到「{gametype}.exe」，其在 [ {gamepath} ] 。")
                    print(f"用时：{round(time.time()-stime,2)}秒。")
                    break
            if ok:
                break
        else:
            continue
    if not ok:
        Cdirlist = os.listdir("C:\\")
        Cdirlist.remove("Windows")
        for i in Cdirlist:
            for root, dir, file in os.walk("C:\\" + i):
                if "YuanShen.exe" in file or "GenshinImpact.exe" in file:
                    if "YuanShen.exe" in file:
                        gametype = "YuanShen"
                        gamepath = os.path.join(root, "YuanShen.exe")
                    if "GenshinImpact.exe" in file:
                        gametype = "GenshinImpact"
                        gamepath = os.path.join(root, "GenshinImpact.exe")
                    ok = True
                    print(f"已找到「{gametype}.exe」，其在 [ {gamepath} ] 。")
                    print(f"用时：{round(time.time()-stime,2)}秒。")
                    break
            if ok:
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
config = open("game.txt", "r", encoding="utf8").read()
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
print("正在自动安装Mod...", end="")
modlist = os.listdir("autoInstall")
if len(modlist) > 0:
    print("")
    stime = time.time()
    for i in range(len(modlist)):
        modlist[i] = os.path.join("autoInstall", modlist[i])
    waittime = 0
    finish = 0
    for i in modlist:
        if os.path.isdir(i):
            print(f"   - 跳过安装「{os.path.basename(i)}」，其不是有效的Mod文件。")
            continue
        try:
            ZipFile(i)
        except:
            print(f"   - 跳过安装「{os.path.basename(i)}」，其不是有效的Mod文件。")
            continue
        waittime += 1
        print(f" - 开始安装「{i}」。")
        threading.Thread(target=lambda: aData(i)).start()
    while waittime != finish:
        pass
    print(f"用时：{round(time.time()-stime,2)}秒。")
else:
    print("好吧，并没有。")
print("正在加载Mod...")
os.system(f"rmdir /s /q {dmodspath}")
shutil.copytree("mods", dmodspath)
print("正在运行Mod修复工具...")
RunAsPowerShell(f"copy dontDeleteMe\\assets\\Fixing.exe {dmodspath}")
os.system("start " + os.path.join(dmodspath, "Fixing.exe"))
RunAsPowerShell(f"del /s /q {os.path.join(dmodspath,'Fixing.exe')}")
print("正在拷贝ShaderFix...")
RunAsPowerShell(f"rmdir /s /q {dsfpath}")
RunAsPowerShell(f"mkdir {dsfpath}")
flist = os.listdir("dontDeleteMe")
for i in flist:
    RunAsPowerShell(f"copy dontDeleteMe\\{i} {dsfpath}")
flist = os.listdir("shaderFix")
for i in flist:
    RunAsPowerShell(f"copy shaderFix\\{i} {dsfpath}")
RunAsPowerShell(f"rmdir /s /q {os.path.join(dsfpath,'assets')}")
print("准备拉起Mod加载器...请按下任意键继续。")
msvcrt.getch()
os.chdir(os.path.join(temppath, "3dmigoto"))
os.startfile("3DMigoto Loader.exe")
print("请检查新出现的窗口，如果出现了“Now run the game.”则模组加载器已经启动成功。\n请按下任意键继续。")
msvcrt.getch()
print("正在启动你的游戏...")
try:
    os.startfile(config)
except Exception as Error:
    print("启动失败，可能是游戏文件不存在或已经损坏，请检查game.txt中的路径是否有效。")
    print(f"错误：{Error}")
else:
    print("成功启动游戏，游戏窗口稍后将会出现。")
print("按下任意键退出。")
msvcrt.getch()
