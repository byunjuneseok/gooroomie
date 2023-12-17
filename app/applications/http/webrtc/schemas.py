from aiortc import RTCSessionDescription
from pydantic import BaseModel


class Description(BaseModel):
    sdp: str
    type: str

    @classmethod
    def from_rtc_session_description(cls, rtc_session_description: RTCSessionDescription):
        return cls(
            sdp=rtc_session_description.sdp,
            type=rtc_session_description.type,
        )

    def to_rtc_session_description(self):
        return RTCSessionDescription(
            sdp=self.sdp,
            type=self.type,
        )
