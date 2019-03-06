time=$(date "+%Y%m%d")

output="/home/zhuxu/mmjs_server/gohttps_loader/static/weather/output"

weather_file_name=$time"_专家聊天气.mp3"

echo $time"_专家聊天气" | mailx -s $time"_天气和专家" -a $output/$weather_file_name  1077246@qq.com

 



