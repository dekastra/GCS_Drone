import gi
import socket

#  Required tools
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer, GLib

class Stream:
    def __init__(
        self,
        server,
        pipeline,
        endpoint
    ):
        self.server = server
        self.pipeline = pipeline
        self.endpoint = endpoint

    def video_stream(self):
        factory = GstRtspServer.RTSPMediaFactory.new()
        factory.set_launch(self.pipeline)
        factory.set_shared(True)
        self.server.get_mount_points().add_factory(self.endpoint, factory)

def main():
    Gst.init(None)

    server_address = socket.gethostbyname(socket.gethostname())
    server_port = "8554"

    server = GstRtspServer.RTSPServer.new()
    server.set_address(server_address)
    server.set_service(server_port)

    # RTSP path for vid1
    pipeline_vid1 = (
        "filesrc location=./videos/vid1.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96"
    )
    stream_1 = Stream(server, pipeline_vid1, '/vid1')
    stream_1.video_stream()


    # RTSP path for vid2
    pipeline_vid2 = (
        "filesrc location=./videos/vid2.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96"
    )
    stream_2 = Stream(server, pipeline_vid2, '/vid2')
    stream_2.video_stream()


    # RTSP path for vid3
    pipeline_vid3 = (
        "filesrc location=./videos/vid3.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96"
    )
    stream_3 = Stream(server, pipeline_vid3, '/vid3')
    stream_3.video_stream()


    # RTSP path for vid4
    pipeline_vid4 = (
        "filesrc location=./videos/vid4.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96"
    )
    stream_4 = Stream(server, pipeline_vid4, '/vid4')
    stream_4.video_stream()


    # RTSP path for webcam
    pipeline_webcam = (
        "ksvideosrc device-index=0 ! videoconvert ! x264enc tune=zerolatency key-int-max=15 bitrate=1000 ! h264parse ! rtph264pay name=pay0 pt=96 mtu=1200 ! rtspclientsink location=rtsp://127.0.0.1:8554/live sync=false"
    )
    stream_4 = Stream(server, pipeline_webcam, '/live')
    stream_4.video_stream()

    print(f"RTSP Server started on {server_address}:{server_port}")
    server.attach(None)

    main_loop = GLib.MainLoop()
    try:
        main_loop.run()
    except KeyboardInterrupt:
        main_loop.quit()

if __name__ == "__main__":
    main()
