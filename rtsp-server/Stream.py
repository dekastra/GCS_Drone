import gi

#  Required tools
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import GstRtspServer

class Stream:
    def __init__(
        self,
        name,
        pipeline,
        endpoint
    ):
        self.name = name
        self.pipeline = pipeline
        self.endpoint = endpoint

    def register_stream(self, server):
        factory = GstRtspServer.RTSPMediaFactory.new()
        factory.set_launch(self.pipeline)
        factory.set_shared(True)
        server.get_mount_points().add_factory(self.endpoint, factory)