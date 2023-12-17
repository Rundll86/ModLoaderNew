import zipfile, os, json


def ZipDir(DirName, FileName, DontZip: list = []):
    FolderPath = os.path.join(os.getcwd(), DirName)
    File = zipfile.ZipFile(FileName, "w")
    for Root, Dirs, Files in os.walk(FolderPath):
        if os.path.basename(Root) in DontZip:
            continue
        for File2 in Files:
            DontZip.append(FileName)
            if File2 in DontZip:
                continue
            FilePath = os.path.join(Root, File2)
            File.write(FilePath, os.path.relpath(FilePath, FolderPath))
        for Dir in Dirs:
            FilePath = os.path.join(Root, Dir, "thereIsSomething")
            zipfile.ZipFile(FilePath, "w")
            File.write(FilePath, os.path.join(os.path.relpath(FilePath, FolderPath)))
            os.system(f'del /s /q "{FilePath}"')
    File.close()


filename = f"ModLoaderNew v{json.load(open('dontDeleteMe/assets/info.json',encoding='utf8'))['version']}.zip"
ZipDir(
    "dist",
    f"dist\\{filename}",
    [filename],
)
