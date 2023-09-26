cmd
ffmpeg -re -i rtsp://192.168.1.7:1935 -c:v copy -c:a aac -strict experimental -f hls -hls_flags delete_segments -hls_time 1 -hls_list_size 2 ./static/output.m3u8
