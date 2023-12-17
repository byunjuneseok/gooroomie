import platform

from aiortc import MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay


class WebcamStreamer:
    def __init__(self, video_media_relay: MediaRelay):
        self.video_media_relay = video_media_relay

    def create_local_tracks(self, decode) -> tuple[MediaStreamTrack | None, MediaStreamTrack | None]:
        options = dict(framerate="30", video_size="640x480")
        match platform.system():
            case "Darwin":
                webcam = MediaPlayer("default:none", format="avfoundation", options=options)
            case "Windows":
                webcam = MediaPlayer("video=Integrated Camera", format="dshow", options=options)
            case _:
                webcam = MediaPlayer("/dev/video0", format="v4l2", options=options)
        return None, self.video_media_relay.subscribe(webcam.video)
