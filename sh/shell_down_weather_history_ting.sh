# 下载交通台早上一路畅通，截取天气部分00:31:50-00:37:30
# http://playback.rbc.cn/audioD/fm1039/20180319/0730007200_mp4/073000_7200_96K.mp4

if [ "$1" = "" ];then
time=$(date "+%Y%m%d")
else
time=$1
fi

# output="/Users/zhuxu/Downloads"
output="/home/zhuxu/mmjs_server/gohttps_loader/static/weather"

rm -rf $output/*.mp4
rm -rf $output/*.mp3
rm -rf $output/*.wav

# 下载直播
# ffmpeg -y -i http://audiolive.rbc.cn:1935/live/fm1039/96K/tzwj_video.m3u8 -ss 0 -to 120  test.mp4
#url="http://audiolive.rbc.cn:1935/live/fm1039/96K/tzwj_video.m3u8"
#name=$time"_ylct.mp4"
#echo $url
#echo $name
# wget -O $output/$name $url
weather_name=$time"_专家聊天气.mp4"
weather_name_wav=$time"_专家聊天气.wav"
echo $weather_name
/home/zhuxu/mmjs_server/sh/py_weather_serial_ting.py $time
#ffmpeg -y -i $url -ss 00:00:00 -to 00:30:30 $output/$weather_name
ffmpeg -y -i $output/$weather_name -ss 00:26:00 -to 00:34:30 -ac 1 -ar 16000 $output/$weather_name_wav
rm -rf $output/$weather_name



/home/zhuxu/mmjs_server/sh/py_weather_serial.py $time
echo $time"_专家聊天气his" | mailx -s $time"_天气和专家" -a $output/$weather_file_name  1077246@qq.com

 


