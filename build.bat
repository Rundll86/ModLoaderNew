echo off
cls
rmdir /s /q dist
Pyinstaller -F ModLoader.py
del /s /q ModLoader.spec
rmdir /s /q build
xcopy /e /i /h /y mods dist\mods
xcopy /e /i /h /y shaderFix dist\shaderFix
xcopy /e /i /h /y dontDeleteMe dist\dontDeleteMe
xcopy /e /i /h /y autoInstall dist\autoInstall