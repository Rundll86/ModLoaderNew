那么，截止到v1.3.5，目前ModLoaderNew的功能有  
- 自动查找游戏路径  
- 自动安装模组  
- 隐藏按下F1时出现的菜单（便于深渊开书吃球）  
- 重写3DMigoto的帮助文本  
- 自动生成 `d3dx.ini`  
- 模组修复器（最新+传统）  
- 自动拉起3DMigoto与游戏

快速部署并使用  
前提条件：`Python 3.8.5` 与 `PIP`  
WindowsPowershell：
```plain
> git clone https://github.com/Rundll86/ModLoaderNew.git
> cd ModLoaderNew
> .\init.bat
> .\build.bat
> start dist\ModLoader.exe
```