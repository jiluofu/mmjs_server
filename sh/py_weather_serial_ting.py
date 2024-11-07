#!/home/zhuxu/vnev/bin/python3

import sys
import subprocess
import re
import os
import time
import requests
import json
import wget

import librosa
# import tkinter
# import matplotlib.pyplot as plt
from dtw import dtw
from numpy.linalg import norm


arr = [
	'20180203',
	'20180205',
	'20180207',
	'20180208',
	'20180210',
	'20180211',
	'20180304',
	'20180305',
	'20180306',
	'20180311',
	'20180312',
	'20180313',
	'20180314',
	'20180315',
	'20180316',
	'20180317',
	'20180320',
	'20180321',
	'20180322',

]

# arr = [
# 	'20180207',
# 	'20180314',
# 	'20180322',

# ]

arr = ['20180715']
# 20180329 33s 114s 306s

# pre = '/Users/zhuxu'
# path = pre + '/Downloads'
# shellPath = pre + '/Documents/sh'

pre = '/home/zhuxu'
path = pre + '/mmjs_server/gohttps_loader/static/weather'
shellPath = pre + '/mmjs_server/sh'



def getMFCC(fileName, start = 0, len = None):
	mfcc = 0
	y, sr = librosa.load(fileName, offset = start, duration = len)
	
	try:
		mfcc = librosa.feature.mfcc(y = y, sr = sr)
	except:
		if y.size == 0:
			return None
	return mfcc


def getDistance(model, sample):
	
	y1, sr1 = librosa.load(model) 
	y2, sr2 = librosa.load(sample) 
	mfcc1 = librosa.feature.mfcc(y1,sr1)
	mfcc2 = librosa.feature.mfcc(y2,sr2)
	dist, cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
	print("****The normalized distance between the two : ",dist)   
	return dist

def getDist(mfcc1, mfcc2):

	if mfcc1 is None:
		return -1
	dist, cost, acc_cost, pathmfcc = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
	return dist

def getSecPosPrecise(date, modelMFCC, sec, modelSecLength, dist):

	distArr = []
	distDict = {}

	stopAfterNum = 2
	closeToTarget = False
	modelSecLength = modelSecLength / 2
	multiNum = 1
	if dist > 70:
		multiNum = 2
	else:
		multiNum = 1.2

	searchStart = int(sec - multiNum * modelSecLength)
	if searchStart < 0:
		searchStart = 0
	searchEnd = int(sec + multiNum * modelSecLength)

	for i in range(searchStart, searchEnd, 3):
		
		sampleName = path + '/' + date + '_专家聊天气.wav'
		mfccSam = getMFCC(sampleName, i, modelSecLength)
		dist = getDist(mfccSam, modelMFCC)
		if dist < 0:
			break;
		

		distArr.append(dist)
		distDict[dist] = i
		
		print('presice sec:' + str(i) + ',dist:' + str(dist))
		if int(min(distArr)) < 100:
			print('presice ***' + str(int(min(distArr))))
			closeToTarget = True
			# break;
		if closeToTarget:
			if stopAfterNum == 0:
				break
			else:
				stopAfterNum = stopAfterNum - 1

	distMin = min(distArr)
	print('precise min dist:' + str(distMin))
	print('precise min sec:' + str(distDict[distMin]))

	return distDict[distMin]

# def getSecPos(date, title, modelMFCC, modelName, modelSecLength, searchStart = 0, searchEnd = 100):

	
# 	distArr = []
# 	distDict = {}

# 	stopAfterNum = 2
# 	closeToTarget = False

	

# 	for i in range(searchStart, searchEnd, int(modelSecLength / 2)):
		
# 		# sampleName = path + '/wout/' + date + '_' + title + str(i) + '.wav'
# 		# subprocess.check_output('ffmpeg -y -i ' + path + '/' + date + '_专家聊天气.wav -ss ' + str(i) + ' -to ' + str(i + modelSecLength) + '  -f wav ' + sampleName, shell=True)
# 		# dist = getDistance(modelName, sampleName)
		
# 		sampleName = path + '/' + date + '_专家聊天气.wav'
# 		mfccSam = getMFCC(sampleName, i, modelSecLength)
# 		dist = getDist(mfccSam, modelMFCC)
# 		if dist < 0:
# 			break
			

# 		distArr.append(dist)
# 		distDict[dist] = i
# 		# print(min(distArr))
# 		print('sec:' + str(i) + ',dist:' + str(dist))
# 		if int(min(distArr)) < 80:
# 			print('***' + str(int(min(distArr))))
# 			closeToTarget = True
# 			break;
# 		if closeToTarget:
# 			if stopAfterNum == 0:
# 				break
# 			else:
# 				stopAfterNum = stopAfterNum - 1

# 	distMin = min(distArr)
# 	print('min dist:' + str(distMin))
# 	print('min sec:' + str(distDict[distMin]))
# 	secPrecise = getSecPosPrecise(date, modelMFCC, distDict[distMin], modelSecLength, distMin)
# 	if secPrecise > 0:
# 		return secPrecise
# 	else:
# 		return distDict[distMin]

# 	#a = subprocess.check_output('rm -rf ' + path + '/wout/*', shell=True)
# 	return distDict[distMin]

def getSecPosSerial(date, title, modelMFCC, modelSecLength, searchStart = 0, searchEnd = 600):

	
	distArr = []
	distDict = {}

	for i in range(searchStart, searchEnd, int(modelSecLength / 3)):
		
		if i + modelSecLength > secs:
			break;

		sampleName = path + '/' + date + '_专家聊天气.wav'
		mfccSam = getMFCC(sampleName, i, modelSecLength)
		dist = getDist(mfccSam, modelMFCC)
		if dist < 0:
			break

		distArr.append(dist)
		distDict[dist] = i

		if int(min(distArr)) < 80:
			print('***' + str(int(min(distArr))))
			return i

		print('sec:' + str(i) + ',dist:' + str(dist))
		

	distMin = min(distArr)
	print('min dist:' + str(distMin))
	print('min sec:' + str(distDict[distMin]))
	
	return distDict[distMin]

def trim(str):
    pattern = r'(^([\s])+)|(([\s])+$)'
    res = re.sub(pattern, '', str)
    return res;

def getHistoryRes(date):
    url = "https://api-v3.tingtingfm.com//albumaudio/play_audio?version=h5_5.24&client=h5_1b48aff64fe4c08c775a8e14e41da52a&type=&sort=-1&audio_id=PorqsN44zd&api_sign=f52e16d37cc8f095754b6d4070dd6aa0"
    print(url)
    response = requests.get(url=url)
    jsondata = response.text
    play_url = json.loads(jsondata)['data']['list'][0]['play_url']
    print(play_url)
    audioFile = path + '/' + date + '_专家聊天气.mp4'
    print(audioFile)
    wget.download(play_url, out=audioFile)
    exit()

def getWeather(date):

	audioFile = path + '/' + date + '_专家聊天气.wav'
	res = subprocess.check_output('ffprobe -i ' + audioFile + ' -show_entries stream=codec_type,duration -of compact=p=0:nk=1|grep audio', shell=True)
	res = trim(res.decode())
	res = res.split('|')
	global secs
	secs = int(float(res[1]))
	print('secs:' + str(secs))

	a = subprocess.check_output('rm -rf ' + path + '/wout/*', shell=True)

	secZj = getSecPosSerial(date, '专家聊天气', mfccZJ, 12, 0, secs)
	secFinish = getSecPosSerial(date, '专家聊天气', mfccFIN, 7, secZj, secs)
	print('secZj:' + str(secZj))
	print('secFinish:' + str(secFinish))
	output(date, secZj, secFinish - secZj + 10, '专家聊天气')
	# if secFinish > secZj and (secFinish - secZj - 10 > 100):
	# 	output(date, secZj, secFinish - secZj - 10, '专家聊天气')
	# else:
	# 	output(date, secZj, 350, '专家聊天气')
	
def output(date, secStart, secLength, name):

	outputName = path + '/output/' + date + '_' + name + '.wav'
	outputNameMp3 = path + '/output/' + date + '_' + name + '.mp3'
	subprocess.check_output('ffmpeg -loglevel quiet -y -i ' + path + '/' + date + '_专家聊天气.wav -ss ' + str(secStart) + ' -to ' + str(secStart + secLength) + '  -f wav ' + outputName, shell=True)
	subprocess.check_output('ffmpeg -loglevel quiet -y -i ' + path + '/' + date + '_专家聊天气.wav -ss ' + str(secStart) + ' -to ' + str(secStart + secLength) + '  -f mp3 ' + outputNameMp3, shell=True)
	title = date + '_' + name
	#subprocess.check_output('echo ' + title + ' | mailx -s ' + title + ' -a ' + outputNameMp3 + '  1077246@qq.com', shell=True)
	os.system('echo ' + title + ' | mailx -s ' + title + ' -a ' + outputNameMp3 + '  1077246@qq.com')
	
start = time.time()
# 天气开始
# mfccTQ = getMFCC(shellPath + '/model_tq.wav')
# 专家开始
mfccZJ = getMFCC(shellPath + '/model_zhuanjia.wav')
# 专家结束
mfccFIN = getMFCC(shellPath + '/model_finish.wav')
# print(mfccFIN)

if len(sys.argv) == 2 and sys.argv[1] != '':
	getHistoryRes(sys.argv[1])

elapsed = (time.time() - start)
print("Time used:", elapsed)












