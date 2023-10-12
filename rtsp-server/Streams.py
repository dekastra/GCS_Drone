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