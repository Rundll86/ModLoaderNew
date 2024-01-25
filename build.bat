echo off
cls
rmdir /s /q dist
Pyinstaller --add-data "fixing_4-1.json;." --add-data "fixing_4-3.json;." -F Fixing.py
del /s /q dontDeleteMe\assets\Fixing.exe
copy dist\Fixing.exe dontDeleteMe\assets
del /s /q dist\Fixing.exe
Pyinstaller -F ModLoader.py -i favicon.ico
del /s /q ModLoader.spec
del /s /q Fixing.spec
rmdir /s /q build
xcopy /e /i /h /y dontDeleteMe dist\dontDeleteMe
mkdir dist\mods
mkdir dist\shaderFix
mkdir dist\autoInstall
python dist-data.py
pause