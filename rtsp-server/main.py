import gi
import socket

#  Required tools
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer, GLib

class Stream:
    def __init__(
        self,
        name,
        pipeline,
        endpoint
    ):
        self.server = server
        self.name = name
        self.pipeline = pipeline
        self.endpoint = endpoint

    def register_stream(self, server):
        factory = GstRtspServer.RTSPMediaFactory.new()
        factory.set_launch(self.pipeline)
        factory.set_shared(True)
        server.get_mount_points().add_factory(self.endpoint, factory)

class RTSPServer:
    def __init__(self, address, port):
        self.server = GstRtspServer.RTSPServer.new()
        self.server.set_address(address)
        self.server.set_service(port)
        self.server.attach(None)
        self.streams = []

    def add_new_stream(self, name, pipeline, path):
        new_stream = Stream(name, pipeline, path)
        new_stream.register_stream(self.server)
        self.streams.append(new_stream)

    def stream_list(self):
        print("==============================================")
        index = 1
        for stream in self.streams:
            url = f"rtsp://{self.server.get_address()}:{self.server.get_service()}{stream.endpoint}"
            print(f"{index}. {stream.name} | {url}")
            index += 1

if __name__ == "__main__":
    Gst.init(None)

    server_address = socket.gethostbyname(socket.gethostname())
    server_port = "8554"

    server = RTSPServer(server_address, server_port)
    server.add_new_stream(
        "Video Pantai",
        "filesrc location=./videos/vid1.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96",
        "/vid1"
    )
    server.add_new_stream(
        "Video Air",
        "filesrc location=./videos/vid2.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96",
        '/vid2'
    )
    server.add_new_stream(
        "Video Senja",
        "filesrc location=./videos/vid3.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96",
        "/vid3"
    )
    server.add_new_stream(
        "Video Tempat Sampah",
        "filesrc location=./videos/vid4.mp4 ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96",
        "/vid4"
    )
    server.add_new_stream(
        "Webcam",
        "ksvideosrc device-index=0 ! videoconvert ! x264enc tune=zerolatency key-int-max=15 bitrate=1000 ! h264parse ! rtph264pay name=pay0 pt=96 mtu=1200",
        "/cam"
    )

    print(f"RTSP Server started on {server_address}:{server_port}")
    server.stream_list()

    main_loop = GLib.MainLoop()
    try:
        main_loop.run()
    except KeyboardInterrupt:
        main_loop.quit()




