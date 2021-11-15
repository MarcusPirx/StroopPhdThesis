# Standard module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import noisereduce as nr #ruduce noise
import scipy.io.wavfile as wf
from itertools import compress
import warnings
warnings.filterwarnings("ignore")

class wave_app_procesing():
    """
    Process audio files and result recording data, align timeline , 
    extract useable reaction time , plot data, save data. 

    **
    if the result is unsatisfactory, try to change the `speech_start_band`
    and `speech_end_band`.
    """
    def __init__(self, wave_input_filename,resut_recording_filename):
        self._read_wav(wave_input_filename)
        self._read_app(resut_recording_filename)
        self.sample_window = 0.02 #20 ms
        self.sample_overlap = 0.01 #10ms
        self.speech_window = 0.5 #half a second
        self.speech_energy_threshold = 0.6 #60% of energy in voice band
        self.speech_start_band = 300
        self.speech_end_band = 3000
        # 根据平均发音时间和取多少个标准差区间调整最小发音时间
        self.n_std=1 
        

    def _read_wav(self, wave_file):
        """
        读取wav文件，计算时间线，提取波形图
        """
        self.rate, self.data_original = wf.read(wave_file)
        # Noise reduction processing
        self.data=nr.reduce_noise(y=self.data_original, sr=self.rate) 
        self.channels = len(self.data.shape)
        self.filename = wave_file
        self.time=np.arange(0,len(self.data))/self.rate
        return self
    
    #############################################
    # Voice activity detector based on ration between energy 
    # in speech band and total energy.
    def _calculate_frequencies(self, audio_data):
        data_freq = np.fft.fftfreq(len(audio_data),1.0/self.rate)
        data_freq = data_freq[1:]
        return data_freq    
    
    def _calculate_amplitude(self, audio_data):
        data_ampl = np.abs(np.fft.fft(audio_data))
        data_ampl = data_ampl[1:]
        return data_ampl
        
    def _calculate_energy(self, data):
        data_amplitude = self._calculate_amplitude(data)
        data_energy = data_amplitude ** 2
        return data_energy
        
    def _znormalize_energy(self, data_energy):
        energy_mean = np.mean(data_energy)
        energy_std = np.std(data_energy)
        energy_znorm = (data_energy - energy_mean) / energy_std
        return energy_znorm
    
    def _connect_energy_with_frequencies(self, data_freq, data_energy):
        energy_freq = {}
        for (i, freq) in enumerate(data_freq):
            if abs(freq) not in energy_freq:
                energy_freq[abs(freq)] = data_energy[i] * 2
        return energy_freq
    
    def _calculate_normalized_energy(self, data):
        data_freq = self._calculate_frequencies(data)
        data_energy = self._calculate_energy(data)
        #data_energy = self._znormalize_energy(data_energy) #znorm brings worse results
        energy_freq = self._connect_energy_with_frequencies(data_freq, data_energy)
        return energy_freq
    
    def _sum_energy_in_band(self,energy_frequencies, start_band, end_band):
        sum_energy = 0
        for f in energy_frequencies.keys():
            if start_band<f<end_band:
                sum_energy += energy_frequencies[f]
        return sum_energy
    
    def _median_filter (self, x, k):
        assert k % 2 == 1, "Median filter length must be odd."
        assert x.ndim == 1, "Input must be one-dimensional."
        k2 = (k - 1) // 2
        y = np.zeros ((len (x), k), dtype=x.dtype)
        y[:,k2] = x
        for i in range (k2):
            j = k2 - i
            y[j:,i] = x[:-j]
            y[:j,i] = x[0]
            y[:-j,-(i+1)] = x[j:]
            y[-j:,-(i+1)] = x[-1]
        return np.median (y, axis=1)
        
    def _smooth_speech_detection(self, detected_windows):
        median_window=int(self.speech_window/self.sample_window)
        if median_window%2==0: median_window=median_window-1
        median_energy = self._median_filter(detected_windows[:,1], median_window)
        return median_energy
        
    def convert_windows_to_readible_labels(self, detected_windows):
        """ Takes as input array of window numbers and speech flags from speech
        detection and convert speech flags to time intervals of speech.
        Output is array of dictionaries with speech intervals.
        """
        speech_time = []
        is_speech = 0
        for window in detected_windows:
            if (window[1]==1.0 and is_speech==0): 
                is_speech = 1
                speech_label = {}
                speech_time_start = window[0] / self.rate
                speech_label['speech_begin'] = speech_time_start
                # print(window[0], speech_time_start)
                #speech_time.append(speech_label)
            if (window[1]==0.0 and is_speech==1):
                is_speech = 0
                speech_time_end = window[0] / self.rate
                speech_label['speech_end'] = speech_time_end
                speech_time.append(speech_label)
                # print(window[0], speech_time_end)
        return speech_time
      
       
    def detect_speech(self):
        """ Detects speech regions based on ratio between speech band energy
        and total energy.
        Output is array of window numbers and speech flags (1 - speech, 0 - nonspeech).
        """
        detected_windows = np.array([])
        sample_window = int(self.rate * self.sample_window)
        sample_overlap = int(self.rate * self.sample_overlap)
        data = self.data
        sample_start = 0
        start_band = self.speech_start_band
        end_band = self.speech_end_band
        while (sample_start < (len(data) - sample_window)):
            sample_end = sample_start + sample_window
            if sample_end>=len(data): sample_end = len(data)-1
            data_window = data[sample_start:sample_end]
            energy_freq = self._calculate_normalized_energy(data_window)
            sum_voice_energy = self._sum_energy_in_band(energy_freq, start_band, end_band)
            sum_full_energy = sum(energy_freq.values())
            speech_ratio = sum_voice_energy/sum_full_energy
            # Hipothesis is that when there is a speech sequence we have ratio of energies
            #  more than Threshold
            speech_ratio = speech_ratio>self.speech_energy_threshold
            detected_windows = np.append(detected_windows,[sample_start, speech_ratio])
            sample_start += sample_overlap
        detected_windows = detected_windows.reshape(int(len(detected_windows)/2),2)
        detected_windows[:,1] = self._smooth_speech_detection(detected_windows)
        return detected_windows
    
    ##############################
    # refrence : https://github.com/marsbroshok/VAD-python
    ##############################
    
    def _read_app(self,app_file):
        """
        读取app文件，提取显示和回答的时间戳，正确与否.
        """
        self.app=np.array(pd.read_csv(app_file,sep=' ',header=None).iloc[1:,[11,12,17,18,19,20,21,22]])
        ## answer data proceding
        answer_data=self.app[self.app[:,4]==1,:] #回答的部分
        self.answer={'ID':[],'time':[],'type':[],'result':[]} #数据转化
        j=1;k=2
        for i in np.arange(len(answer_data)):
            if (answer_data[i,7]==k)&(answer_data[i,6]!=j):
                # right
                self.answer["result"].append('correct')
                self.answer["ID"].append(i)
                self.answer["time"].append(answer_data[i,0])
                self.answer["type"].append('response')
                k+=1;j+=0
            elif (answer_data[i,7]!=k)&(answer_data[i,6]==j):
                #wrong
                self.answer["result"].append('incorrect')
                self.answer["ID"].append(i)
                self.answer["time"].append(answer_data[i,0])
                self.answer["type"].append('response')
                k+=0;j+=1
        ## show data proceding
        show_array=self.app[self.app[:,2]==1,:][:len(self.answer["ID"]),0]
        self.show={'ID':self.answer["ID"],'time':list(show_array),'type':list(np.repeat('show',len(show_array))),'result':self.answer['result']} #显示的时间处理
        return self

    def vad_time(self):
        """
        n_std: Set the value range, within one standard deviation,
                发音时间取值范围在多少个标准差范围内，调整大小以保证极小发音被忽略。
        确定时间节点(开始和结束)，并且标注，计算所有词语的平均发音时间，把极端值部分去除。
        output:
        --------
        Dict with 'ID',"speech_begin","speech_end","speech_dur","included"
        """
        raw_detection=self.detect_speech()
        speech_labels=self.convert_windows_to_readible_labels(raw_detection)
        ls_speech=[] #Collect pronunciation time
        for speech in speech_labels:
            ls_speech.append(speech["speech_end"]-speech["speech_begin"])
        dict_speech={'ID':[],"speech_begin":[],"speech_end":[],"speech_dur":[],"included":[]}
        ID=0
        for speech in speech_labels:
            dict_speech['ID'].append(ID)
            dict_speech["speech_begin"].append(speech["speech_begin"])
            dict_speech["speech_end"].append(speech["speech_end"])
            dur=speech["speech_end"]-speech["speech_begin"]
            dict_speech["speech_dur"].append(dur)
            if dur>(np.mean(ls_speech)-self.n_std*np.std(ls_speech)):
                dict_speech["included"].append("Yes")
            else:
                dict_speech["included"].append("No")
            ID+=1 
        return dict_speech

    def show_speech_labels(self,save_path=None):
        """
        显示说话标签位置
        "ID","timeline","type","result","included","block","final_solution"
        """
        speech_time=self.vad_time()
        speech_timeline={'time':speech_time["speech_begin"]+speech_time["speech_end"],
                'type':list(np.repeat("speech_begin",len(speech_time["speech_begin"])))+list(np.repeat("speech_end",len(speech_time["speech_end"]))),
                'included':speech_time["included"]+speech_time["included"]}
        combined_data=pd.concat([pd.DataFrame(self.show),pd.DataFrame(self.answer),pd.DataFrame(speech_timeline)]).sort_values(by=["time","ID"]).reset_index().iloc[:,1:]
        combined_data["block"]=0
        # 分区编号处理
        block=0
        index_num=0
        while index_num<len(combined_data):
            if combined_data.iloc[index_num,2]=="show":
                block+=1
            combined_data.iloc[index_num,5]=block
            index_num+=1
        # 提取可用的分区，显示和回答区间只有一个"speech_begin"和一个"speech_end".
        combined_data["included"]=combined_data["included"].replace(np.NaN,"Yes")
        dcombined_array=np.array(combined_data.loc[:,['time','type','included','block']])
        final_solution=np.array([])
        for bo in combined_data.block.unique():
            name=dcombined_array[(dcombined_array[:,3]==bo)&(dcombined_array[:,2]=='Yes'),1]
            if len(name)==4:
                if all(name==['show','speech_begin', 'speech_end', 'response']):
                    final_solution=np.concatenate((final_solution,np.repeat('included',len(dcombined_array[dcombined_array[:,3]==bo,1]))),axis=0)
                else:
                    final_solution=np.concatenate((final_solution,np.repeat('NoNincluded',len(dcombined_array[dcombined_array[:,3]==bo,1]))),axis=0)
            else:
                final_solution=np.concatenate((final_solution,np.repeat('NoNincluded',len(dcombined_array[dcombined_array[:,3]==bo,1]))),axis=0)
        combined_data["final_solution"]=final_solution
        # save file
        if save_path!=None:
            combined_data.to_csv(save_path,sep='\t',index=False)
        return combined_data

    def show_reaction_time(self,path_save=None):
        """
        提取可以使用的数据部分，记录"show",'speech_begin','speech_end','response',
        'reaction_time','speech_during','result(correct/incorrect)'
        """
        data=self.show_speech_labels()
        data=data.loc[data.final_solution=="included",["time","type","result","block"]]
        result={'show':[],'speech_begin':[],"speech_end":[],"response":[],"result":[],"reaction_time":[],"speech_during":[]}
        for i in data.block.unique():
            sp_block=np.array(data.loc[data.block==i,:])
            reaction_time=sp_block[1,0]-sp_block[0,0]
            speech_dur=sp_block[2,0]-sp_block[1,0]
            res=sp_block[0,2]
            result['show'].append(sp_block[0,0])
            result['speech_begin'].append(sp_block[1,0])
            result['speech_end'].append(sp_block[2,0])
            result['response'].append(sp_block[3,0])
            result['reaction_time'].append(reaction_time)
            result['speech_during'].append(speech_dur)
            result['result'].append(res)
        # save file 
        if path_save!=None:
            pd.DataFrame(result).to_csv(path_save,sep='\t',index=False)
        return pd.DataFrame(result)


    def plot_detected_speech_regions(self,save_path=None):
        data=self.data*1.0/(max(abs(self.data))) #压缩转化
        timeline=self.show_speech_labels()
        including_data=self.show_reaction_time()
        fig=plt.figure(figsize=(20,5))
        plt.plot(self.time,data,color="#bababa") #波形图，灰色那个
        plt.vlines(timeline.loc[timeline.type=="show","time"],ymin=0,ymax=1,color="#e41a1c") # display word
        plt.vlines(timeline.loc[timeline.type=="response","time"],ymin=-1,ymax=0,color="#377eb8") # answer word
        plt.vlines(timeline.loc[(timeline.type=="speech_begin")&(timeline.included=='Yes'),"time"],ymin=-0.5,ymax=0.5,color="#4daf4a") # speech_begin, included
        plt.vlines(timeline.loc[(timeline.type=="speech_end")&(timeline.included=='Yes'),"time"],ymin=-0.5,ymax=0.5,color="#984ea3") # speech_end, included
        plt.vlines(timeline.loc[(timeline.type=="speech_begin")&(timeline.included=='No'),"time"],ymin=-0.5,ymax=0.5,linestyles="dotted",color="#4daf4a") # speech_begin, Not included
        plt.vlines(timeline.loc[(timeline.type=="speech_end")&(timeline.included=='No'),"time"],ymin=-0.5,ymax=0.5,linestyles="dotted",color="#984ea3") # speech_end, Not included
        # fill included zone
        for i in including_data.index:
            if including_data.iloc[i,4]=='correct':
                plt.fill_betweenx(y=(-1,1),x1=including_data.iloc[i,0],x2=including_data.iloc[i,1],alpha=0.2,color="#abdda4")
                plt.text(x=np.mean([including_data.iloc[i,0],including_data.iloc[i,1]]),y=0.5,s="RT=%s s" %str(np.around(including_data.iloc[i,5],decimals=2)),rotation='vertical')
            else:
                plt.fill_betweenx(y=(-1,1),x1=including_data.iloc[i,0],x2=including_data.iloc[i,1],alpha=0.2,color="#fdae61")
                plt.text(x=np.mean([including_data.iloc[i,0],including_data.iloc[i,1]]),y=0.5,s="RT=%s s" %str(np.around(including_data.iloc[i,5],decimals=2)),rotation='vertical')
        # legend        
        plt.xlabel('Time(s)')
        plt.ylabel('Sound waveform')
        plt.tight_layout()
        if save_path!=None:
            plt.savefig(save_path,dpi=120)
        plt.show()
    
    
