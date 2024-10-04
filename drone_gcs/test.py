from video_utility import GetVideo, ShowVideo, VideoData
from detector import Detector

data = VideoData()
fetcher = GetVideo(data, 0)
window = ShowVideo(data, title="Video1")
detector = Detector(data)


fetcher.start_fetch()
window.start()
detector.start_detect()

