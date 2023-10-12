import gi
import socket
from RTSPServer import RTSPServer
from Stream import Stream

#  Required tools
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GLib

if __name__ == "__main__":
    Gst.init(None)

    rtsp = RTSPServer(socket.gethostbyname(socket.gethostname()),"8554")

    # Video streams
    s1 = Stream(
        "Video Pantai",
        "filesrc location=./videos/vid1.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96",
        "/vid1"
    )

    s2 = Stream(
        "Video Air",
        "filesrc location=./videos/vid2.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96",
        "/vid2"
    )

    s3 = Stream(
        "Video Senja",
        "filesrc location=./videos/vid3.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96",
        "/vid3"
    )

    s4 = Stream(
        "Video Tempat Sampah",
        "filesrc location=./videos/vid4.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96",
        "/vid4"
    )

    s5 = Stream(
        "Webcam",
        "ksvideosrc device-index=0 ! videoconvert ! x264enc tune=zerolatency key-int-max=15 bitrate=1000 ! h264parse ! rtph264pay name=pay0 pt=96 mtu=1200",
        "/cam"
    )

    rtsp.add_streams(s1, s2, s3, s4, s5)

    main_loop = GLib.MainLoop()
    try:
        print(f"RTSP Server started on {rtsp.server.get_address()}:{rtsp.server.get_service()}")
        rtsp.stream_list()
        main_loop.run()
    except KeyboardInterrupt:
        main_loop.quit()




