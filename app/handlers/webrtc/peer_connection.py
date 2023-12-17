import uuid
from typing import Optional

from aiortc import RTCConfiguration, RTCPeerConnection


class PeerConnection(RTCPeerConnection):
    connection_id: str

    def __init__(self, configuration: Optional[RTCConfiguration] = None) -> None:
        super().__init__(configuration)
        self.connection_id = uuid.uuid4().__str__()
