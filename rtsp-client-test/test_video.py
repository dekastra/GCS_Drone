from video_utils import GetVideo, ShowVideo, VideoData

data = VideoData()
fetcher = GetVideo(data, "rtsp://192.168.50.116:8554/cam")
window = ShowVideo(data)

fetcher.start_fetch()
window.start()

command = input()
if command == 'exit':
    fetcher.stop_fetch()
    window.stop()