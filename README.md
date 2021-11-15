# StroopPhdThesis

This is the code for the data processing in Eric's doctoral thesis. 

Title (provisional): 

Using of Stroop Task based on recognition of hands movement and voice auto detect by Kinect in patients with ADHD and Asperger disorder.

[TOC]




## English(EN)

** All original text files are separated by a "Space", all saved files are separated by a "Tab".**



## Experimental design





#### Audio data processing

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



### Technical Description





##  中文(CN)

### 实验设计:

基于Microsoft Kinect识别人体的姿态以及自动声音识别的Stroop实验，一共6组实验，前三组实验每组要求被试对象在45秒的时间内根据屏幕显示的颜色单词(包含红蓝绿三色)大声说出单词或者颜色，与标准Stroop实验(Golden, 1978,见下方引用)一致，分为三组，第一组显示黑色印刷颜色单词，要求读出单词。第二组显示带有颜色的"XXXXX"，要求说出颜色，第三组显示印刷颜色和单词词义不一致的单词，要求说出印刷颜色而不是单词。屏幕每次显示一个单词，电脑识别到被试者发音的结果后自动切换到下一个单词。第二部分同样分为三组，分别是黑色单词组，颜色"XXXX"组，和颜色词义不一致组，同样是每组45秒，实验根据Kinect识别全身25个关节位置的点，要求被试者站立在距离Kinect两米远距离屏幕三米远的位置，在屏幕显示单词的时候抬手指向与正确颜色一致的方块然后立即放下。被试可以实时看到自己的姿态和手腕的移动状态。被试腕部进入方块意味着选择该方块颜色作为答案，离开该方块方会显示下一个方块。

cite: 

```
@article{golden1978stroop,
  title={Stroop color and word test},
  author={Golden, Charles J and Freshwater, Shawna M},
  year={1978},
  publisher={Stoelting Chicago}
}
```

### 实验数据: 

- 第一部分实验(基于声音识别)包含了7个文件，头部1347个识别点的2D和3D数据(2D,3D)，身体的25个关节点的数据(Sk,SkI)，kinect和被试者的角度距离等数据(Sa)，声音识别的结果数据(app)， 以及音频文件(Sp)。

- 第二部分实验(基于腕部运动识别)包含6个文件，头部1347个识别点的2D和3D数据(2D,3D)，身体的25个关节点的数据(Sk,SkI)，kinect和被试者的角度距离等数据(Sa)，腕关节位置识别的结果数据(app)。



### 数据挖掘:

#### 平台

- 使用python version 3.9.7 (https://www.python.org/)进行数据挖掘和整理，使用IDE Visual Studio Code (https://code.visualstudio.com/)以及anaconda (https://www.anaconda.com/)做代码开发测试。

- 使用的包:

  - datetime

  - numpy

  - pandas

  - matplotlib

  - seaborn

  - scipy
  - noisereduce

#### 模块说明

##### main.py

python文件，主运行文件。

###### 处理流程:

> 1. 获取当前文件路径，根据当前文件路径识别数据存放路径(**运行时把py文件夹放置到数据文件夹HDRecs同级文件目录下运行**)， 并在当数据文件夹同级目录建立结果储存文件夹(result)以及在其下级路径建立每个实验部分的子文件夹(Bd_TEST1,Bd_TEST2,Bd_TEST3,Sp_TEST1,Sp_TEST2,Sp_TEST3)。
> 2. 识别HDRecs目录下子路径内所有文件，并建立变量。
> 3. 对语音实验的部分提取音频文件和实验结果文件进行结合分析(基于wave_app_procesing class)。



##### wave_app_procesing.py

python文件，包含了对基于声音识别实验部分的处理，包含Class(对象) wave_app_procesing。

> - 导入音频文件的波形并做降噪处理(func: **_read_wav**)。
> - 对降噪后音频文件使用语音活动检测（Voice Activity Detection， VAD）识别每个单词的发音起始时间和结束时间，基于短时能量方法，根据手动调整识别残余杂音，再根据实验的结果记录(App)，做出时间线标记，包括屏幕显示单词，开始发音，结束发音和电脑识别出单词的时间戳，识别的结果(回答对与错，<span style="color:Red">显示的单词，回答的单词(待添加)</span>，func: **_read_app**)并根据时间线排序。(func: **show_speech_labels**)
> - 按时间线划分每次从显示单词到电脑识别结果的时间段作为分区，识别每次显示单词后到电脑识别出结果之间只有一次发音开始和发音结束的分区，计算从显示单词到开始发音的时间作为可使用反应时间(reaction time)， 并记录单词发音持续时间(speech_during)。
> - 作图(func: **plot_detected_speech_regions**)，把波形图缩放到标准区间(-1,1)，标记显示单词(red line, \#e41a1c, 0-1)，电脑识别回答(bule line, #377eb8,  0-(-1))，发音开始(green line,\#4daf4a,  -0.5-0.5)，发音结束(purple line,\#984ea3 -0.5-0.5)，杂音开始(green dots line,\#4daf4a,  -0.5-0.5)，杂音结束(purple dots line,\#984ea3 -0.5-0.5)，正确回答和错误回答时间戳。

###### ~~self.plot_error_trend~~

目的:
建立一个模型，利用提取后可使用的反应时间数据(self.show_reaction_time)，根据时间顺序，在一个时间点(speech_begin)如果答案是正确的，那么就算作1，在另外一个时间点(speech_begin)，如果答案是错误的，那么就算作-1,这样子做逻辑回归模型就可以得到一个斜率和截距。如果在测试时间内所有可用的数据中，所有答案都是正确的，那么会得到一个斜率为0，截距为1的结果;如果所有答案都是错误的，那么会得到一个斜率为0，截距为-1的结果; 如果随着时间的进展，错误的频率增加，那么会得到一个斜率为负值的结果; 如果随着时间的进展， 错误的频率减少，那么会得到一个斜率为正值的结果。可以根据斜率和截距来判断在当前时间下的总体错误趋势和稳定性。

问题:

如果时间轴上缺失的数据较多，例如前半段有多次因为多次发音(本质上也是错误回答)导致无法获得反应时间，这些数据被当作无效数据，没有纳入计算，导致了前半段只有对的数据，后半段出现错误的数据，这样子会出现明显的后半段错误概率增加，斜率为负值。同理，如果是后半段那么就会出现斜率为正值。但是两种情况下都无法反应实际的情况。





## 技术名词解释(Explanation of technical terms)



### 语音活动检测/Voice Activity Detection(VAD)

语音活动检测（Voice Activity Detection， VAD）用于检测出语音信号的起始位置，分离出语音段和非语音（静音或噪声）段。VAD算法大致分为三类：基于阈值的VAD、基于分类器的VAD和基于模型的VAD。

基于阈值的VAD是通过提取时域（短时能量、短时过零率等）或频域（MFCC、谱熵等）特征，通过合理的设置门限，达到区分语音和非语音的目的；

基于分类的VAD是将语音活动检测作为（语音和非语音）二分类，可以通过机器学习的方法训练分类器，达到语音活动检测的目的；

基于模型的VAD是构建一套完整的语音识别模型用于区分语音段和非语音段，考虑到实时性的要求，并未得到实际的应用。

**代码里是基于短时能量做出区分的 (cite: https://github.com/marsbroshok/VAD-python)**



### 平均绝对偏差









## 限制(Limitations)


### 反应时间和错误率
理论上随着实验时间的推移，ADHD患者是否有可能出现反应时间延长和错误率增加，但是因为设计的三组Stroop不是同样的操作，所以很难计算得出。只能是按照常规理论计算反应时间，错误率因为Speech 的第二组记录(color)没有记录到正确和错误个数，所以没法计算各组的错误率。唯一能观察的只有忽略对错的反应时间。















