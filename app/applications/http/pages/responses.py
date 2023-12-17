from starlette.responses import Response


class JavascriptResponse(Response):
    media_type = "application/javascript"
