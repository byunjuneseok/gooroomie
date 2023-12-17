import platform

from aiortc import MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay


class WebcamStreamer:
    def __init__(self, video_media_relay: MediaRelay, audio_media_relay: MediaRelay):
        self.audio_media_relay = audio_media_relay
        self.video_media_relay = video_media_relay

    def create_local_tracks(self) -> tuple[MediaStreamTrack | None, MediaStreamTrack | None]:
        video_options = dict(framerate="30", video_size="640x480")
        audio_player, video_player = None, None
        match platform.system():
            case "Darwin":
                video_player = MediaPlayer("default:none", format="avfoundation", options=video_options)
            case "Windows":
                video_player = MediaPlayer("video=Integrated Camera", format="dshow", options=video_options)
            case _:
                video_player = MediaPlayer("/dev/video0", format="v4l2", options=video_options)
                audio_player = MediaPlayer("default", format="alsa")
        return (
            self.audio_media_relay.subscribe(audio_player.audio) if audio_player else None,
            self.video_media_relay.subscribe(video_player.video) if video_player else None,
        )
