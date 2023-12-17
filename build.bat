echo off
cls
rmdir /s /q dist
Pyinstaller -F ModLoader.py
del /s /q ModLoader.spec
rmdir /s /q build
xcopy /e /i /h /y dontDeleteMe dist\dontDeleteMe
mkdir dist\mods
mkdir dist\shaderFix
mkdir dist\autoInstall
python dist-data.py
.\pushing.bat