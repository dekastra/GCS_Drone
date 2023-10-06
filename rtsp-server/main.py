import gi

#  Required tools
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GObject, GstRtspServer

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
    GObject.threads_init()
    Gst.init(None)

    server = GstRtspServer.RTSPServer.new()
    server.set_service("8554")

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
      "ksvideosrc ! decodebin ! videoconvert ! autovideosink ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96"
    )
    stream_4 = Stream(server, pipeline_webcam, '/live')
    stream_4.video_stream()

    server.attach(None)

    main_loop = GObject.MainLoop()
    main_loop.run()

if __name__ == "__main__":
    main()
