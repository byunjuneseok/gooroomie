from aiortc.contrib.media import MediaRelay
from dependency_injector import containers, providers
from starlette.templating import Jinja2Templates

from handlers.webcam_streamer import WebcamStreamer
from handlers.webrtc.peer_connection_manager import WebRTCPeerConnectionManager


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["applications"])
    config = providers.Configuration(yaml_files=["config.yml"])

    video_media_relay = providers.Singleton(MediaRelay)
    webcam_streamer = providers.Singleton(
        WebcamStreamer,
        video_media_relay=video_media_relay,
    )
    webrtc_peer_connection_manager = providers.Singleton(
        WebRTCPeerConnectionManager,
        webcam_streamer=webcam_streamer,
        audio_codec=config.webrtc.peer_connection_manager.audio_codec,
        video_codec=config.webrtc.peer_connection_manager.video_codec,
    )
    templates = providers.Resource(Jinja2Templates, directory="templates")
