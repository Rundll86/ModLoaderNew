那么，截止到v1.4.4，目前ModLoaderNew的功能有：  
- 自动查找游戏路径  
- 自动安装模组  
- 隐藏按下F1时出现的菜单（便于深渊开书吃球）  
- 重写3DMigoto的帮助文本  
- 自动生成 `d3dx.ini`  
- 模组修复器（最新+传统）  
- 自动拉起3DMigoto与游戏  
- 对游戏隐藏了3DMigoto的进程（包括其本身的窗口）
- 自动从GameBanana获取模组供玩家选择性下载
- 模组管理器
- Whatever will be, will be...

Todo-list：  
- 游戏路径管理器
- Whatever will be, will be...

快速部署并使用  
先决条件：`Python 3.8.5`、`PIP` 与 `Git Bash`  
配置 `Git Bash` 用户信息
```plain
> git config --global user.email "UserEmail"
> git config --global user.name "UserName"
```
克隆代码并编译
```plain
> git clone https://github.com/Rundll86/ModLoaderNew.git
> cd ModLoaderNew
> .\init.bat
> .\build.bat
> start dist\ModLoader.exe
```