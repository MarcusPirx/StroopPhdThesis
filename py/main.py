#runtime begin
from datetime import datetime
time_start=datetime.now() #开始运行时间
# import packages
#导入包
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

###################################路径读取和相关变量命名#############################
# Current folder path 
# 当前文件路径
from os import getcwd
cur_path=getcwd() #当前文件路径
print("Current folder path: "+cur_path)
# Parent folder path (top path of data files)
# 父级路径，因为需要访问放在父级文件夹的数据文件
from os.path import abspath
from os import pardir
par_dir=abspath(pardir) #父级文件路径
print("Parent folder path: "+par_dir)
# Data read path
# 数据文件存放路径(基于当前文件父级目录)
Bd_TEST1=par_dir+"\\HDRecs\\Bd_TEST1"
Bd_TEST2=par_dir+"\\HDRecs\\Bd_TEST2"
Bd_TEST3=par_dir+"\\HDRecs\\Bd_TEST3"
Sp_TEST1=par_dir+"\\HDRecs\\Sp_TEST1"
Sp_TEST2=par_dir+"\\HDRecs\\Sp_TEST2"
Sp_TEST3=par_dir+"\\HDRecs\\Sp_TEST3"

# Data save path
# 设定文件保存目录
Bd_TEST1_save=par_dir+"\\result\\Bd_TEST1"
Bd_TEST2_save=par_dir+"\\result\\Bd_TEST2"
Bd_TEST3_save=par_dir+"\\result\\Bd_TEST3"
Sp_TEST1_save=par_dir+"\\result\\Sp_TEST1"
Sp_TEST2_save=par_dir+"\\result\\Sp_TEST2"
Sp_TEST3_save=par_dir+"\\result\\Sp_TEST3"
# check and make save path
from os import path
if path.exists(Bd_TEST1_save)==False:
    from os import makedirs
    makedirs(Bd_TEST1_save),makedirs(Bd_TEST2_save),makedirs(Bd_TEST3_save)
    makedirs(Sp_TEST1_save),makedirs(Sp_TEST2_save),makedirs(Sp_TEST3_save)

# read data files in Bd_TEST1 dir
from os import listdir
Bd_TEST1_file=listdir(Bd_TEST1) # get all sub-files name
Bd_TEST1_2D=Bd_TEST1+"\\"+list(filter(lambda x: '_2D' in x, Bd_TEST1_file))[0] # mathch 2D data file
Bd_TEST1_3D=Bd_TEST1+"\\"+list(filter(lambda x: '_3D' in x, Bd_TEST1_file))[0] #match 3D data file
Bd_TEST1_App=Bd_TEST1+"\\"+list(filter(lambda x: '_App' in x, Bd_TEST1_file))[0] #match App data file
Bd_TEST1_Sa=Bd_TEST1+"\\"+list(filter(lambda x: '_Sa' in x, Bd_TEST1_file))[0] #match Sa data file
Bd_TEST1_Sk=Bd_TEST1+"\\"+list(filter(lambda x: '_Sk' in x, Bd_TEST1_file))[0] #match Sk data file
Bd_TEST1_SkI=Bd_TEST1+"\\"+list(filter(lambda x: '_SkI' in x, Bd_TEST1_file))[0] #match SkI data file
# print("Read data from:")
# print(Bd_TEST1)
# print("Load file:")
# print(Bd_TEST1_2D),print(Bd_TEST1_3D),print(Bd_TEST1_App),print(Bd_TEST1_Sa),print(Bd_TEST1_Sk),print(Bd_TEST1_SkI)

# read data files in Bd_TEST2 dir
from os import listdir
Bd_TEST2_file=listdir(Bd_TEST2) # get all sub-files name
Bd_TEST2_2D=Bd_TEST2+"\\"+list(filter(lambda x: '_2D' in x, Bd_TEST2_file))[0] # mathch 2D data file
Bd_TEST2_3D=Bd_TEST2+"\\"+list(filter(lambda x: '_3D' in x, Bd_TEST2_file))[0] #match 3D data file
Bd_TEST2_App=Bd_TEST2+"\\"+list(filter(lambda x: '_App' in x, Bd_TEST2_file))[0] #match App data file
Bd_TEST2_Sa=Bd_TEST2+"\\"+list(filter(lambda x: '_Sa' in x, Bd_TEST2_file))[0] #match Sa data file
Bd_TEST2_Sk=Bd_TEST2+"\\"+list(filter(lambda x: '_Sk' in x, Bd_TEST2_file))[0] #match Sk data file
Bd_TEST2_SkI=Bd_TEST2+"\\"+list(filter(lambda x: '_SkI' in x, Bd_TEST2_file))[0] #match SkI data file
# print("Read data from:")
# print(Bd_TEST2)
# print("Load file:")
# print(Bd_TEST2_2D),print(Bd_TEST2_3D),print(Bd_TEST2_App),print(Bd_TEST2_Sa),print(Bd_TEST2_Sk),print(Bd_TEST2_SkI)
# read data files in Bd_TEST3 dir
from os import listdir
Bd_TEST3_file=listdir(Bd_TEST3) # get all sub-files name
Bd_TEST3_2D=Bd_TEST3+"\\"+list(filter(lambda x: '_2D' in x, Bd_TEST3_file))[0] # mathch 2D data file
Bd_TEST3_3D=Bd_TEST3+"\\"+list(filter(lambda x: '_3D' in x, Bd_TEST3_file))[0] #match 3D data file
Bd_TEST3_App=Bd_TEST3+"\\"+list(filter(lambda x: '_App' in x, Bd_TEST3_file))[0] #match App data file
Bd_TEST3_Sa=Bd_TEST3+"\\"+list(filter(lambda x: '_Sa' in x, Bd_TEST3_file))[0] #match Sa data file
Bd_TEST3_Sk=Bd_TEST3+"\\"+list(filter(lambda x: '_Sk' in x, Bd_TEST3_file))[0] #match Sk data file
Bd_TEST3_SkI=Bd_TEST3+"\\"+list(filter(lambda x: '_SkI' in x, Bd_TEST3_file))[0] #match SkI data file
# print("Read data from:")
# print(Bd_TEST3)
# print("Load file:")
# print(Bd_TEST3_2D),print(Bd_TEST3_3D),print(Bd_TEST3_App),print(Bd_TEST3_Sa),print(Bd_TEST3_Sk),print(Bd_TEST3_SkI)
# read data files in Sp_TEST1 dir
from os import listdir
Sp_TEST1_file=listdir(Sp_TEST1) # get all sub-files name
Sp_TEST1_2D=Sp_TEST1+"\\"+list(filter(lambda x: '_2D' in x, Sp_TEST1_file))[0] # mathch 2D data file
Sp_TEST1_3D=Sp_TEST1+"\\"+list(filter(lambda x: '_3D' in x, Sp_TEST1_file))[0] #match 3D data file
Sp_TEST1_App=Sp_TEST1+"\\"+list(filter(lambda x: '_App' in x, Sp_TEST1_file))[0] #match App data file
Sp_TEST1_Sa=Sp_TEST1+"\\"+list(filter(lambda x: '_Sa' in x, Sp_TEST1_file))[0] #match Sa data file
Sp_TEST1_Sk=Sp_TEST1+"\\"+list(filter(lambda x: '_Sk' in x, Sp_TEST1_file))[0] #match Sk data file
Sp_TEST1_SkI=Sp_TEST1+"\\"+list(filter(lambda x: '_SkI' in x, Sp_TEST1_file))[0] #match SkI data file
Sp_TEST1_Sp=Sp_TEST1+"\\"+list(filter(lambda x: '_Sp' in x, Sp_TEST1_file))[0] #match wave data file
# print("Read data from:")
# print(Sp_TEST1)
# print("Load file:")
# print(Sp_TEST1_2D),print(Sp_TEST1_3D),print(Sp_TEST1_App),print(Sp_TEST1_Sa),print(Sp_TEST1_Sk),print(Sp_TEST1_SkI),print(Sp_TEST1_Sp)
# read data files in Sp_TEST2 dir
from os import listdir
Sp_TEST2_file=listdir(Sp_TEST2) # get all sub-files name
Sp_TEST2_2D=Sp_TEST2+"\\"+list(filter(lambda x: '_2D' in x, Sp_TEST2_file))[0] # mathch 2D data file
Sp_TEST2_3D=Sp_TEST2+"\\"+list(filter(lambda x: '_3D' in x, Sp_TEST2_file))[0] #match 3D data file
Sp_TEST2_App=Sp_TEST2+"\\"+list(filter(lambda x: '_App' in x, Sp_TEST2_file))[0] #match App data file
Sp_TEST2_Sa=Sp_TEST2+"\\"+list(filter(lambda x: '_Sa' in x, Sp_TEST2_file))[0] #match Sa data file
Sp_TEST2_Sk=Sp_TEST2+"\\"+list(filter(lambda x: '_Sk' in x, Sp_TEST2_file))[0] #match Sk data file
Sp_TEST2_SkI=Sp_TEST2+"\\"+list(filter(lambda x: '_SkI' in x, Sp_TEST2_file))[0] #match SkI data file
Sp_TEST2_Sp=Sp_TEST2+"\\"+list(filter(lambda x: '_Sp' in x, Sp_TEST2_file))[0] #match wave data file
# print("Read data from:")
# print(Sp_TEST2)
# print("Load file:")
# print(Sp_TEST2_2D),print(Sp_TEST2_3D),print(Sp_TEST2_App),print(Sp_TEST2_Sa),print(Sp_TEST2_Sk),print(Sp_TEST2_SkI),print(Sp_TEST2_Sp)
# read data files in Sp_TEST3 dir
from os import listdir
Sp_TEST3_file=listdir(Sp_TEST3) # get all sub-files name
Sp_TEST3_2D=Sp_TEST3+"\\"+list(filter(lambda x: '_2D' in x, Sp_TEST3_file))[0] # mathch 2D data file
Sp_TEST3_3D=Sp_TEST3+"\\"+list(filter(lambda x: '_3D' in x, Sp_TEST3_file))[0] #match 3D data file
Sp_TEST3_App=Sp_TEST3+"\\"+list(filter(lambda x: '_App' in x, Sp_TEST3_file))[0] #match App data file
Sp_TEST3_Sa=Sp_TEST3+"\\"+list(filter(lambda x: '_Sa' in x, Sp_TEST3_file))[0] #match Sa data file
Sp_TEST3_Sk=Sp_TEST3+"\\"+list(filter(lambda x: '_Sk' in x, Sp_TEST3_file))[0] #match Sk data file
Sp_TEST3_SkI=Sp_TEST3+"\\"+list(filter(lambda x: '_SkI' in x, Sp_TEST3_file))[0] #match SkI data file
Sp_TEST3_Sp=Sp_TEST3+"\\"+list(filter(lambda x: '_Sp' in x, Sp_TEST3_file))[0] #match wave data file
# print("Read data from:")
# print(Sp_TEST3)
# print("Load file:")
# print(Sp_TEST3_2D),print(Sp_TEST3_3D),print(Sp_TEST3_App),print(Sp_TEST3_Sa),print(Sp_TEST3_Sk),print(Sp_TEST3_SkI),print(Sp_TEST3_Sp)
# runtime end
time_end=datetime.now()
time_delta=time_end-time_start
running_date=time_start.strftime("%Y-%m-%d %H:%M:%S")
print("Running date: "+running_date)
print("Running time: "+str(time_delta.seconds)+'s')
print("Success!!!")

#################################################声音文件读取和处理########################################

# 引入wave_app_proceding，这个功能需要app文件以及wave文件， 处理后除了显示图像以外
# 还保存了每个的时间节点，以及有效的反应时间数据。
# wave_sp3_info_time: 时间节点记录文件
# wave_sp3_reaction_time: 有效反应时间记录文件
# from wave_app_proceding import wave_app_proceding
# # Sp_TEST3 
# wave_sp3_info_time,wave_sp3_reaction_time=wave_app_proceding(path_wave=Sp_TEST3_Sp,path_App=Sp_TEST3_App,path_save=Sp_TEST3_save+'\\wave_sp3.png')

# #######################################
# # test 语音活动检测
# from vad1 import VoiceActivityDetector

# v = VoiceActivityDetector(Sp_TEST3_Sp)
# raw_detection=v.detect_speech()
# speech_labels=v.convert_windows_to_readible_labels(detected_windows=raw_detection)
# #print(raw_detection)
# print(speech_labels)
# v.plot_detected_speech_regions()
# #######################################

#######################################
# test new class wave data transform
from wave_app_procesing import wave_app_procesing
exp=wave_app_procesing(Sp_TEST3_Sp,Sp_TEST3_App)
# print(pd.DataFrame(exp.vad_time()))
# 所有的显示回答发音起始结束和是否纳入，表格
speech_labels=exp.show_speech_labels(save_path=Sp_TEST3_save+"\\show_speech_labels.csv")
print(speech_labels)
# print(exp.rate)
# print(exp.time)
# print(exp.channels)
# 所有的显示回答发音起始结束和结果显示成图片
exp.plot_detected_speech_regions(save_path=Sp_TEST3_save+"\\waveform.png")
# 可以使用的部分的反应时间，发音时间等
print(exp.show_reaction_time())

#######################################
