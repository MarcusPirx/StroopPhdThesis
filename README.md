# StroopPhdThesis
This is the code for the data processing in Eric's doctoral thesis. 

Title (provisional): 

Using of Stroop Task based on recognition of hands movement and voice auto detect by Kinect in patients with ADHD and Asperger disorder.

## ES








## EN



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

