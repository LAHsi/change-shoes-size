from typing import Counter
import speech_recognition as sr
import os
import pygame    
import re
import math
import tempfile
import pyaudio
import gtts
from gtts import gTTS
from io import BytesIO    

#'''*********************class***********************'''
class speech_to_text:
  def __init__(self):  
    self.rg = sr.Recognizer()
  def listen(self,lang='zh-tw'): 
    print('Listening ...') 
    with sr.Microphone() as source:
      audioData = self.rg.listen(source)
      try:
        text = self.rg.recognize_google(audioData, language=lang)  
      except:
        text = '我沒聽到你在說甚麼'
    return text

class text_to_speech:
  def __init__(self):
    self.active_mp3  = 'test00.mp3'
    pygame.mixer.init()
  def __del__(self):
    try:
      os.unlink(self.active_mp3)  
    except:
      pass  

  def speak(self,text,lang='zh-tw'): 
    tts= gTTS(text, lang=lang, slow=False)
    tts.save(self.active_mp3)
    pygame.mixer.music.load(self.active_mp3)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
      continue
    pygame.mixer.music.unload()
    return

#'''*********************globals***********************'''
st = speech_to_text()
ts = text_to_speech()
countryOri = str()
countryChange = str()
numToChange = float()
numAfterChange = float()

#'''*********************funcs***********************'''
def wrongFormatFun():
  ts.speak('格式錯誤!')
  print('格式錯誤!', '請再說一次!')
  ts.speak('請再說一次')

def startListen():
  while(1):
    print('語音格式: (台灣/歐洲/美國/中國)N號轉(台灣/歐洲/美國/中國) 或 (台灣/歐洲/美國/中國)轉(台灣/歐洲/美國/中國)N號')    
    speaktxt = st.listen()
    print(speaktxt)
    if speaktxt != '我沒聽到你在說甚麼':
      return speaktxt
    ts.speak(speaktxt)
    print('請再說一次')
    ts.speak('請再說一次')

def CHtoTW(x):
  return (x+10)/2 if x >= 34 and x <= 50 else -1
def EUtoTW(x):
  if x < 36 or x > 46 :
    return -1
  nx=0.75*x-5
  camp=nx-math.floor(nx)
  if camp>=0   and camp<=0.3 : return math.floor(nx)
  if camp>0.3 and camp<=0.6 : return math.floor(nx)+0.5
  if camp>0.6 and camp<=0.9 : return math.ceil(nx)
def UStoTW(x):
    return x+18 if x >= 5 and x <= 12 else -1
def TWtoEU(x):
    return (4/3)*x+(20/3) if x >= 22 and x <= 30 else -1
def TWtoUS(x):
    return x-18 if x >= 22 and x <= 30 else -1
def TWtoCH(x):
    return x*2-10 if x >= 22 and x <= 30 else -1
def CHtoUS(x):
    return x/2-13 if x >= 34 and x <= 50 else -1
def UStoCH(x):
    return 2*x+26 if x >= 5 and x <= 12 else -1
def CHtoEU(x):
    return (2/3)*x+(40/3) if x >= 34 and x <= 50 else -1
def EUtoCH(x):
    return 1.5*x-20 if x >= 36 and x <= 46 else -1
def EUtoUS(x):
    if x < 36 or x > 46 :
      return -1
    nx=x*0.75-23
    camp=nx-math.floor(nx)
    if camp>=0   and camp<=0.3 : return math.floor(nx)
    if camp>0.3 and camp<=0.6 : return math.floor(nx)+0.5
    if camp>0.6 and camp<=0.9 : return math.ceil(nx)
def UStoEU(x):
    return (4/3)*x+(92/3) if x >= 5 and x <= 12 else -1

#'''*********************dict***********************'''
zh2digit_table = {'零': 0, '一': 1, '二': 2, '兩': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100, '千': 1000, '〇': 0, '○': 0, '○': 0, '０': 0, '１': 1, '２': 2, '３': 3, '４': 4, '５': 5, '６': 6, '７': 7, '８': 8, '９': 9, '壹': 1, '貳': 2, '參': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '拾': 10, '佰': 100, '仟': 1000, '萬': 10000, '億': 100000000}
d = {"台灣":0, "歐制":0, '美制':0, '中國':0}
country = {"台":'台灣', "阿":'歐制', '優':'歐制', '後':'歐制', 'L':'歐制', "歐":'歐制', '每':'美制', '美':'美制', '中':'中國'}
changeDict = {"中國轉台灣":CHtoTW, "歐制轉台灣":EUtoTW, "美制轉台灣":UStoTW, "台灣轉歐制":TWtoEU, "台灣轉美制":TWtoUS, "台灣轉中國":TWtoCH, "中國轉美制":CHtoUS, "美制轉中國":UStoCH, "中國轉歐制":CHtoEU, "歐制轉中國":EUtoCH, "歐制轉美制":EUtoUS, "美制轉歐制":UStoEU}

#'''*********************project***********************'''
while(1):
  found = False
  speaktxt = startListen()
  try:
    for i in re.finditer(r"(?P<country1>[台歐阿L優美每中後])[劇灣制製國治志智G巨質緻日次洲週][轉專船](?P<change1>[台歐阿L優美每中後])[劇灣制製國治志智G巨質緻日次洲週](?P<num1>.*(?P<float1>[點]\d)*)[號]|(?P<country2>[台歐阿L優美每中後])[劇灣制製國治志智G巨質緻日次洲](?P<num2>.+(?P<float2>[點]\d)*)[號][轉專船](?P<change2>[台歐阿L優美每中後]).*",speaktxt):
      found = True
      tmp = i.group('num1') if not i.group('num2') else i.group('num2')
      numToChange = zh2digit_table[tmp] if (float(tmp)-float(tmp)//1 < 0) and (tmp <'0' or tmp > '9') else tmp
      countryOri = country[(i.group('country2') if not i.group('country1') else i.group('country1'))]
      countryChange = country[(i.group('change2') if not i.group('change1') else i.group('change1'))]
    if found:
      numAfterChange = round(changeDict[countryOri+"轉"+countryChange](float(numToChange)),1)
      speaktxt = countryChange + str(numAfterChange) + '號' if numAfterChange > 0 else '不在範圍內'
      print(speaktxt)
      ts.speak(speaktxt)
      del ts
      break
    else:
      wrongFormatFun()
  except:
    print('There is something wrong')
    ts.speak('意外錯誤')
