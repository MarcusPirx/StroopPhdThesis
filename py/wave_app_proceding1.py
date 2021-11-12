def wave_app_proceding(path_wave,path_App,path_save=None):
    """

    input:
    --------------------------------------------
    path_wave: file path of wave data.
    path_App: file path pf App data.
    path_save: path for save data.
    output:
    ---------------------------------------------
    a jason data of result
    a plot of the result
    a plot saved in the path save
    """
    import wave
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import noisereduce as nr #ruduce noise
    # open wave file
    f = wave.open(path_wave,"rb")
    # get parameters of file
    params = f.getparams()
    [nchannels, sampwidth, framerate, nframes] = params[:4]
    strData = f.readframes(nframes)
    f.close() # close file
    # read sound data
    waveData = np.frombuffer(strData,dtype=np.int16) #读取文件
    waveData = nr.reduce_noise(y=waveData, sr=framerate) #降噪
    waveData = waveData*1.0/(max(abs(waveData))) #压缩转化
    # Time data mapping
    time1=np.arange(0,nframes)/framerate #计算时间
    time1=time1[0:len(waveData)]
    # path_App App data processing 读取数据
    df=pd.read_csv(path_App,sep=' ',header=None)
    #提取需要的部分
    app=df.iloc[1:,[11,12,17,18,19,20,21,22]].rename(columns={11:'delta_time',12:"block_time",17:'IsShow',18:'ShowColor',19:'IsAnswer',20:'AnswerColor',21:'Wrong',22:'Right'})
    answer_data=app.loc[app['IsAnswer']==1,:] #回答的部分
    answer={'ID':[],'time':[],'type':[],'result':[]} #数据转化
    j=1;k=2
    for i in np.arange(len(answer_data)):
       if (answer_data.iloc[i,7]==k)&(answer_data.iloc[i,6]!=j):
           # right
           answer["result"].append('correct')
           answer["ID"].append(i)
           answer["time"].append(answer_data.iloc[i,0])
           answer["type"].append('response')
           k+=1;j+=0
       elif (answer_data.iloc[i,7]!=k)&(answer_data.iloc[i,6]==j):
           #wrong
           answer["result"].append('incorrect')
           answer["ID"].append(i)
           answer["time"].append(answer_data.iloc[i,0])
           answer["type"].append('response')
           k+=0;j+=1

    show_array=app.loc[app['IsShow']==1,:]["delta_time"][:-1] #显示的时间部分
    show={'ID':list(range(len(show_array))),'time':list(show_array),'type':list(np.repeat('show',len(show_array))),'result':answer['result']} #显示的时间处理
    answer_array=answer["time"] #回答的时间部分


    # 计算局部趋势
    def calculate_mean(x,num):
        res=[]
        for i in np.arange(len(x)):
            if i<num:
                x1=x[0:i]
                x2=x[i:i+num]
                res.append(np.mean(x1+x2))
            elif i+num>len(x):
                x1=x[i:]
                x2=x[i-num:i]
                res.append(np.mean(x1+x2))
            else:
                x1=x[i:i+num]
                x2=x[i-num:i]
                res.append(np.mean(x1+x2))
        return res
    # 局部趋势,根据每50ms计算
    tend_wave=calculate_mean(list(np.absolute(waveData)),800)

    # 获取35%的最小值
    tend_wave_sort=sorted(tend_wave)[0:int(len(tend_wave)*0.65)]
    # 计算切割值
    cut_value=np.max(tend_wave_sort)
    # index
    wave_index=[]
    for i in np.arange(len(tend_wave)):
         if tend_wave[i]>cut_value:
             wave_index.append(i)
    #范围
    def ranges(nums):
        nums = sorted(set(nums))
        gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
        edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
        return list(zip(edges, edges))
     
    edges=ranges(wave_index)
    # 发音大于100ms(1600),小于2s(32000)的才要。
    # 只有在波形图中有波形(绝对值)大于值域的30%的才保留，理论上大于这个程度才能被电脑识别结果?
    # 计算值域切割值
    abs_wave=np.absolute(waveData)
    cut_value=(np.max(abs_wave)-np.min(abs_wave))*0.15
    edges_final=[] #这是发音位置区间信息
    for n in edges:
        if ((n[1]-n[0])>1600)&((n[1]-n[0])<32000):
            if any([np.absolute(x)>cut_value for x in waveData[n[0]:n[1]]]):
                edges_final.append(n)
    
    edge_time=[(time1[x[0]],time1[x[1]]) for x in edges_final] #发音的时间信息

    #发音位置区间转为时间节点
    time_node={'ID':[],'time':[],'type':[],'result':[]}
    for edg in edge_time:
        time_0=edg[0]
        time_1=edg[1]
        for i in answer['ID']:
            ans_time=answer["time"][i]
            show_time=show["time"][i]
            if (time_0>show_time)&(time_0<=ans_time):
                time_node['ID'].append(i)
                time_node['time'].append(time_0)
                time_node['type'].append('start_voz')
                time_node['result'].append(answer['result'][i])
                time_node['ID'].append(i)
                time_node['time'].append(time_1)
                time_node['type'].append('end_voz')
                time_node['result'].append(answer['result'][i])
    #合并时间信息和分类
    info_time=pd.concat([pd.DataFrame(show),pd.DataFrame(answer),pd.DataFrame(time_node)]).sort_values(by=['time'],ignore_index=True)
    # 是否保留判定
    includ_decide=[]
    for i in info_time.ID:
        block_resp=info_time.loc[info_time.ID==i,:]
        if np.sum(block_resp.type=="start_voz")>1:
            #此时有多余两个的发音起始，那就剔除
            includ_decide.append("NoIncluded")
        elif np.sum(block_resp.type=="start_voz")==0:
            #此时是因为发音中途出现下一个词，识别的是下一个词的中间
            includ_decide.append("NoIncluded")
        else:
            includ_decide.append("Included")

    info_time['Includ_info']=includ_decide

    #plot data
    # 展示完整时间节点信息
    fig=plt.figure(figsize=(20,5))
    plt.plot(time1,waveData,color="#bababa") #波形图，灰色那个
    plt.plot(time1,tend_wave,lw=0.5,color="#fdae61")# 波形趋势图，黄色那个
    # 小三角
    #plt.plot([0,45.5],[-0.8,-0.8],lw=-0.8,color="#404040")#标准指示线，在-0.8的位置上
    plt.vlines(info_time.loc[info_time.type=='show','time'],ymin=0,ymax=1,colors="#e41a1c",lw=0.8) #show,red
    plt.vlines(info_time.loc[info_time.type=='response','time'],ymin=-1,ymax=0,colors="#377eb8",lw=0.8) #response blue
    plt.vlines(info_time.loc[info_time.type=='start_voz','time'],ymin=-0.5,ymax=0.5,colors="#4daf4a",lw=0.8) #start voz,green
    plt.vlines(info_time.loc[info_time.type=='end_voz','time'],ymin=-0.5,ymax=0.5,colors="#984ea3",lw=0.8) #end voz,purple
    # fill between
    result_data={"ID":[],"reaction_time":[],"result":[]}
    for i in info_time.ID.unique():
        blk=info_time.loc[info_time.ID==i,:]#每一个block
        if all(blk.Includ_info=='Included')&all(blk.result=='correct'):
            plt.fill_betweenx(y=(-1,1),x1=blk.loc[blk.type=='show','time'],x2=blk.loc[blk.type=='start_voz','time'],alpha=0.2,color="#abdda4")
            r_time=float(blk.loc[blk.type=='start_voz','time'])-float(blk.loc[blk.type=='show','time'])
            plt.text(x=np.mean([blk.loc[blk.type=='start_voz','time'],blk.loc[blk.type=='show','time']]),y=0.5,s="RT=%s ms" %str(int(r_time*1000)),rotation='vertical')
            result_data['ID'].append(i)
            result_data['reaction_time'].append(r_time)
            result_data['result'].append("correct")
        elif all(blk.Includ_info=='Included')&all(blk.result=='incorrect'):
            plt.fill_betweenx(y=(-1,1),x1=blk.loc[blk.type=='show','time'],x2=blk.loc[blk.type=='start_voz','time'],alpha=0.2,color="#fdae61")
            r_time=float(blk.loc[blk.type=='start_voz','time'])-float(blk.loc[blk.type=='show','time'])
            plt.text(x=np.mean([blk.loc[blk.type=='start_voz','time'],blk.loc[blk.type=='show','time']]),y=0.5,s="RT=%s ms" %str(int(r_time*1000)),rotation='vertical')
            result_data['ID'].append(i)
            result_data['reaction_time'].append(r_time)
            result_data['result'].append("incorrect")
        elif all(blk.Includ_info=='NoIncluded'):
            plt.fill_betweenx(y=(-1,1),x1=blk.loc[blk.type=='show','time'],x2=blk.loc[blk.type=='response','time'],alpha=0.2,color="#d7191c")
    # legend        
    plt.xlabel('Time(s)')
    plt.ylabel('Sound waveform')
    plt.tight_layout()
    if path_save!=None:
        plt.savefig(path_save,dpi=120)
    plt.show()
    return info_time,result_data