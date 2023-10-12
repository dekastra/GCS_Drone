import gi

#  Required tools
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import GstRtspServer

class RTSPServer:
    def __init__(self, address, port):
        self.server = GstRtspServer.RTSPServer.new()
        self.server.set_address(address)
        self.server.set_service(port)
        self.server.attach(None)
        self.streams = []

    def add_streams(self, *streams):
        for stream in streams:
            stream.register_stream(self.server)
            self.streams.append(stream)

    def stream_list(self):
        print("==============================================")
        index = 1
        for stream in self.streams:
            url = f"rtsp://{self.server.get_address()}:{self.server.get_service()}{stream.endpoint}"
            print(f"{index}. {stream.name} | {url}")
            index += 1