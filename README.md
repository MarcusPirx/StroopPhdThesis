# StroopPhdThesis
This is the code for the data processing in Eric's doctoral thesis. 

Title (provisional): 

Using of Stroop Task based on recognition of hands movement and voice auto detect by Kinect in patients with ADHD and Asperger disorder.

## ES








## EN

** All original text files are separated by a "Space", all saved files are separated by a "Tab".**

Audio data processing

1. load the audio file (_Sp.wav), load the result record file (App.text).

   ```
	Audio file parameters(_Sp.wav):
	nchannels=1,
	sampwidth=2,
	framerate=16000,
	comptype="NONE"
	compname="not compressed"
	
	result recording parameters(_App.txt): 
0-3 columns are the computer's timestamps.
4-7 columns are Kinect system timestamps.
9-10 columns of patient names.
11 column is the delta time of the task.
12 column is the delta time in every block.
13-16 columns are ????? all -1, the status of recording.
17 column is the display status of the Stroop task (1 means starting to display the word at this time).
18 column is the colour (word) displayed at this time.
19 column is the answer status of the Stroop task ( 1 means the answer detected at this time).
20 column is the word(colour) detected in the answer. 
21 column is the number of wrong answers.
22 column is the number of right answers.
	```

2. Apply noise reduction processing to the loaded waveform (use `noisereduce` package https://github.com/timsainb/noisereduce , see cite information below ).

   cite :
```
   @software{tim_sainburg_2019_3243139,
     author       = {Tim Sainburg},
     title        = {timsainb/noisereduce: v1.0},
     month        = jun,
     year         = 2019,
     publisher    = {Zenodo},
     version      = {db94fe2},
     doi          = {10.5281/zenodo.3243139},
     url          = {https://doi.org/10.5281/zenodo.3243139}
   }

   @article{sainburg2020finding,
     title={Finding, visualizing, and quantifying latent structure across diverse animal vocal repertoires},
     author={Sainburg, Tim and Thielk, Marvin and Gentner, Timothy Q},
     journal={PLoS computational biology},
     volume={16},
     number={10},
     pages={e1008228},
     year={2020},
     publisher={Public Library of Science}
   }
```

3. Scale the waveform to the range -1 and 1.
4. Estimate timeline by the frame rate. 
4. Estimate the average fluctuation range of the waveform per millisecond.
4. 





##  CN
### 依赖包
【datetime】,【numpy】，【pandas】，【matplotlib】，【seaborn】
\rhd  【load_folder】文件，输入一个文件夹位置，识别出这个文件夹下子文件夹，并且根据子文件夹的文件名称，判定文件夹是voice测试，还是gesture测试，并且对每个....

### py folder
**python 文件夹，主要运行`main.py`文件。
\rhd  【main.py】文件,



## Voice Activity Detection(VAD)

语音活动检测（Voice Activity Detection， VAD）用于检测出语音信号的起始位置，分离出语音段和非语音（静音或噪声）段。VAD算法大致分为三类：基于阈值的VAD、基于分类器的VAD和基于模型的VAD。

基于阈值的VAD是通过提取时域（短时能量、短时过零率等）或频域（MFCC、谱熵等）特征，通过合理的设置门限，达到区分语音和非语音的目的；

基于分类的VAD是将语音活动检测作为（语音和非语音）二分类，可以通过机器学习的方法训练分类器，达到语音活动检测的目的；

基于模型的VAD是构建一套完整的语音识别模型用于区分语音段和非语音段，考虑到实时性的要求，并未得到实际的应用。


## 反应时间和错误率
理论上随着实验时间的推移，ADHD患者是否有可能出现反应时间延长和错误率增加，但是因为设计的三组Stroop不是同样的操作，所以很难计算得出。只能是按照常规理论计算反应时间，错误率因为Speech 的第二组记录(color)没有记录到正确和错误个数，所以没法计算各组的错误率。唯一能观察的只有忽略对错的反应时间。



## 平均绝对偏差




## Functions:

### wave_app_procesing (Class)

这是用来处理语音Stroop实验中语音部分的Class，其中



#### ~~self.plot_error_trend~~
目的:
建立一个模型，利用提取后可使用的反应时间数据(self.show_reaction_time)，根据时间顺序，在一个时间点(speech_begin)如果答案是正确的，那么就算作1，在另外一个时间点(speech_begin)，如果答案是错误的，那么就算作-1,这样子做逻辑回归模型就可以得到一个斜率和截距。如果在测试时间内所有可用的数据中，所有答案都是正确的，那么会得到一个斜率为0，截距为1的结果;如果所有答案都是错误的，那么会得到一个斜率为0，截距为-1的结果; 如果随着时间的进展，错误的频率增加，那么会得到一个斜率为负值的结果; 如果随着时间的进展， 错误的频率减少，那么会得到一个斜率为正值的结果。可以根据斜率和截距来判断在当前时间下的总体错误趋势和稳定性。

问题:

如果时间轴上缺失的数据较多，例如前半段有多次因为多次发音(本质上也是错误回答)导致无法获得反应时间，这些数据被当作无效数据，没有纳入计算，导致了前半段只有对的数据，后半段出现错误的数据，这样子会出现明显的后半段错误概率增加，斜率为负值。同理，如果是后半段那么就会出现斜率为正值。但是两种情况下都无法反应实际的情况。



