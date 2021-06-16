# -*- coding:utf-8 -*-
# coding: utf-8
# !/usr/bin/python
# !/usr/bin/env python
import json
import time
import os


def T2TStamp(timestr):
    a = timestr.replace("T", " ").split('.')
    timeArray = time.strptime(a[0], "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    b = int(a[1].split('+')[0]) / 1000
    return timeStamp + b


def spi_data(source_dir, data_dir, csv_name, starttime, endtime):
    attempts = 0
    success = False
    with open(csv_name, 'a', encoding='utf-8') as f:
        # f.write("coulumn name"+"\n")
        # while attempts < 3 and not success:
        try:
            for root, dir, files in os.walk(source_dir):
                for file in files:
                    # print(file.split("-")[-cryptography-linux离线安装][:-5])
                    if "ProcessStepStatus" in file and starttime <= int(
                            file.split("-")[-1][:-5]) <= endtime and "E53SBSPI" in file:
                        pathfile = os.path.join(root, file)
                        print(pathfile)
                        with open(pathfile, 'r') as jsonfile:
                            v = json.load(jsonfile)
                            dateTime = str(T2TStamp(v["dateTime"]))
                            itemInstanceId = v["content"]["itemInstanceId"]  # barcode
                            imageId = v["content"]["imageId"]
                            model = v["content"]["inspectionData"]["cModel"]
                            measureList = v["content"]["inspectionData"]["boardList"][0]["measureList"]
                            for i in measureList:
                                CompName = i["CompName"]
                                windowList = i["windowList"]
                                H = A = V = X = Y = {}
                                for j in windowList:
                                    Windownum = j["Name"]
                                    Status = j["Status"]
                                    MachineDefect = j["MachineDefect"]
                                    ConfirmDefect = j["ConfirmDefect"]
                                    for a in j["algorithmList"]:
                                        if a["Name"] == "H":
                                            H = a
                                        elif a["Name"] == "A":
                                            A = a
                                        elif a["Name"] == "V":
                                            V = a
                                        elif a["Name"] == "X":
                                            X = a
                                        elif a["Name"] == "Y":
                                            Y = a
                                            f.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23},{24},{25},{26},{27},{28}".format(dateTime, itemInstanceId, imageId, model, CompName, Windownum, Status,MachineDefect, ConfirmDefect, H.get('Upper'), H.get('Value'), H.get('Low'),H.get('Std'), A.get('Upper'), A.get('Value'), A.get('Low'), A.get('Std'),V.get('Upper'), V.get('Value'), V.get('Low'), V.get('Std'), X.get('Upper'),X.get('Value'), X.get('Low'), X.get('Std'), Y.get('Upper'), Y.get('Value'),Y.get('Low'), Y.get('Std')) + "\n")
        # except Exception as e:
        #     print(e)
        except:
            pass
spi_data(r"/mnt/data_disk/SMT/cogiscan/upload/02_E53SBBSPI1", r".", "spi_data_0113_test.csv", 20190113000000000,20190113000200000)