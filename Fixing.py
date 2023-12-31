import os, json


def processfolder(folder_path):
    ini_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isdir(file_path):
            processfolder(file_path)
        elif (
            os.path.splitext(filename)[1] == ".ini"
            and "desktop" not in filename.lower()
            and "ntuser" not in filename.lower()
            and "disabled_backup" not in filename.lower()
        ):
            ini_files.append(filename)
    for ini_file in ini_files:
        try:
            print(f"已找到: {folder_path} {ini_file}")
            counter = 0
            with open(os.path.join(folder_path, ini_file), "r+", encoding="utf-8") as f:
                data = f.read()
                matching = [x for x in old_hashes_vb_41 if x in data] or [
                    x for x in postionhashes_41 if x in data
                ]
                if len(matching) < 1:
                    print("\t不认识此VB Hash")
                for match in matching:
                    if match in oldvsnew_41 and oldvsnew_41[match] not in data:
                        print("\t正在更新到4.1版本")
                        with open(
                            os.path.join(
                                folder_path,
                                "DISABLED_Backup_41"
                                + os.path.splitext(ini_file)[0]
                                + ".txt",
                            ),
                            "w",
                            encoding="utf-8",
                        ) as g:
                            g.write(data)
                        data += f"\n\n; 4.1 Character Fix \n[TextureOverride41FixVertexLimitRaise{counter}]\nhash = {oldvsnew_41[match]}\nmatch_priority = 1"
                        counter += 1
                    elif (
                        match in DetermineCharacterBasedOnPositionHash_41
                        and DetermineCharacterBasedOnPositionHash_41[match] not in data
                    ):
                        print("\t正在更新到4.1版本")
                        with open(
                            os.path.join(
                                folder_path,
                                "DISABLED_Backup_41"
                                + os.path.splitext(ini_file)[0]
                                + ".txt",
                            ),
                            "w",
                            encoding="utf-8",
                        ) as g:
                            g.write(data)
                        data += f"\n\n; 4.1 Character Fix \n[TextureOverride41FixVertexLimitRaise{counter}]\nhash = {DetermineCharacterBasedOnPositionHash_41[match]}\nmatch_priority = 1"
                        counter += 1
                    else:
                        print("\t配置文件已经升级到了4.1！")
                matching = [x for x in old_hashes_ib_43 if str(x) in data] or [
                    x for x in new_hashes_ib_43 if str(x) in data
                ]
                if len(matching) < 1:
                    print("\t不认识此IB Hash")
                for match in matching:
                    if match in oldvsnew_43 and oldvsnew_43[match] not in data:
                        print("\t正在更新到4.3版本")
                        with open(
                            os.path.join(
                                folder_path,
                                "DISABLED_Backup_43"
                                + os.path.splitext(ini_file)[0]
                                + ".txt",
                            ),
                            "w",
                            encoding="utf-8",
                        ) as g:
                            g.write(data)
                        output = ""
                        for line in data.splitlines():
                            if match in line:
                                updated_line = line.replace(match, oldvsnew_43[match])
                                output += updated_line + "\n"
                                line = ";" + line
                            output += line + "\n"
                        data = output
                    else:
                        print("\t配置文件已经升级到了4.3！")
                f.seek(0)
                f.write(data)
                f.truncate()
        except Exception as e:
            print("无法打开，已跳过。")
            print(f"错误：{e}")


old_hashes_vb_41 = []
new_hashes_vb_41 = []
postionhashes_41 = []
oldvsnew_41 = {}
DetermineCharacterBasedOnPositionHash_41 = {}
old_hashes_ib_43 = []
new_hashes_ib_43 = []
oldvsnew_43 = {}
alljson_41 = json.load(open("fixing_4-1.json", encoding="utf8"))
alljson_43 = json.load(open("fixing_4-3.json", encoding="utf8"))
for j in alljson_41:
    print(j)
    if j["new_draw_vb"] != "":
        if j["old_draw_vb"] != "":
            old_hashes_vb_41.append(j["old_draw_vb"])
            new_hashes_vb_41.append(j["new_draw_vb"])
            oldvsnew_41[j["old_draw_vb"]] = j["new_draw_vb"]
        if j["position_vb"] != "":
            postionhashes_41.append(j["position_vb"])
        DetermineCharacterBasedOnPositionHash_41[j["position_vb"]] = j["new_draw_vb"]
for j in alljson_43:
    if j["new_ib"] != "":
        if j["old_ib"] != "":
            old_hashes_ib_43.append(j["old_ib"])
            new_hashes_ib_43.append(j["new_ib"])
            oldvsnew_43[j["old_ib"]] = j["new_ib"]
if __name__ == "__main__":
    print("正在搜索模组配置文件...")
    processfolder(os.getcwd())
    print("全部修复完成！")
