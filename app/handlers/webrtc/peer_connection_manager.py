import asyncio
from typing import TYPE_CHECKING

from aiortc import RTCRtpSender, RTCSessionDescription

from handlers.webrtc.peer_connection import PeerConnection

if TYPE_CHECKING:
    from handlers.webcam_streamer import WebcamStreamer


class WebRTCPeerConnectionManager:
    def __init__(self, webcam_streamer: "WebcamStreamer", audio_codec: str, video_codec: str):
        self.peer_connections: set[PeerConnection] = set()
        self.webcam_streamer = webcam_streamer
        self.audio_codec = audio_codec
        self.video_codec = video_codec

    def _create_new_peer_connection(self) -> PeerConnection:
        peer_connection = PeerConnection()
        self.peer_connections.add(peer_connection)

        @peer_connection.on("connectionstatechange")
        async def on_connection_state_change():
            if peer_connection.connectionState == "failed":
                await peer_connection.close()
                self.peer_connections.remove(peer_connection)

        return peer_connection

    def _force_codec(self, peer_connection, sender, forced_codec):
        kind = forced_codec.split("/")[0]
        codecs = RTCRtpSender.getCapabilities(kind).codecs
        transceiver = next(t for t in peer_connection.getTransceivers() if t.sender == sender)
        transceiver.setCodecPreferences([codec for codec in codecs if codec.mimeType == forced_codec])

    def add_track(self, peer_connection: PeerConnection):
        audio_track, video_track = self.webcam_streamer.create_local_tracks(False)
        if audio_track:
            audio_sender = peer_connection.addTrack(audio_track)
            self._force_codec(peer_connection, audio_sender, self.audio_codec)

        if video_track:
            video_sender = peer_connection.addTrack(video_track)
            self._force_codec(peer_connection, video_sender, self.video_codec)

    async def create_answer(self, offer) -> RTCSessionDescription:
        pc = self._create_new_peer_connection()
        self.add_track(pc)
        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        return pc.localDescription

    async def close_all_peer_connections(self):
        await asyncio.gather(*[pc.close() for pc in self.peer_connections])
        self.peer_connections.clear()
