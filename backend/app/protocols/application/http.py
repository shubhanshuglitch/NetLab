from typing import Dict, Any, Optional
from backend.app.schemas.packets import ApplicationHeader


def create_http_request(
    method: str = "GET",
    url: str = "/index.html",
    host: str = "www.google.com",
    cookie: Optional[str] = None,
    if_none_match: Optional[str] = None
) -> ApplicationHeader:
    headers = {
        "Host": host,
        "User-Agent": "NetLab-Browser/1.0 (Educational Network Simulator)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive"
    }
    if cookie:
        headers["Cookie"] = cookie
    if if_none_match:
        headers["If-None-Match"] = if_none_match

    payload_text = f"{method} {url} HTTP/1.1\r\n" + "".join([f"{k}: {v}\r\n" for k, v in headers.items()]) + "\r\n"

    return ApplicationHeader(
        protocol="HTTP",
        message_type="REQUEST",
        method_or_status=method,
        url_or_path=url,
        headers=headers,
        payload=payload_text
    )


def create_http_response(
    status_code: int = 200,
    status_text: str = "OK",
    body: str = "<html><body><h1>Welcome to NetLab</h1></body></html>",
    content_type: str = "text/html",
    set_cookie: Optional[str] = None,
    etag: str = '"33a64df551425fcc3e397f8"'
) -> ApplicationHeader:
    headers = {
        "Content-Type": content_type,
        "Content-Length": str(len(body)),
        "Server": "NetLab-Edge-Server/2.0",
        "ETag": etag,
        "Cache-Control": "max-age=3600, public"
    }
    if set_cookie:
        headers["Set-Cookie"] = set_cookie

    payload_text = f"HTTP/1.1 {status_code} {status_text}\r\n" + "".join([f"{k}: {v}\r\n" for k, v in headers.items()]) + f"\r\n{body}"

    return ApplicationHeader(
        protocol="HTTP",
        message_type="RESPONSE",
        method_or_status=str(status_code),
        url_or_path="",
        headers=headers,
        payload=payload_text
    )

