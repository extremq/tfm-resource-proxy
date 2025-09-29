from http.server import BaseHTTPRequestHandler
import httpx
import os

mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.wav': 'audio/wav',
    '.mp4': 'video/mp4',
    '.woff': 'application/font-woff',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
    '.wasm': 'application/wasm',
    '.swf': 'application/x-shockwave-flash'
}

def getMimeType(filePath):
    _, ext = os.path.splitext(filePath)
    return mimeTypes.get(ext.lower(), 'application/octet-stream')

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Transformice-Url")
        self.end_headers()

    def do_GET(self):
        transformice_url = self.headers.get("Transformice-Url")
        if not transformice_url:
            self.send_error(404, "Transformice-Url header missing")
            return

        try:
            with httpx.Client() as client:
                resp = client.get(
                    f"http://transformice.com{transformice_url}",
                    timeout=10.0,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

            content_type = resp.headers.get("Content-Type") or getMimeType(transformice_url)


            self.send_response(resp.status_code)
            self.send_header("Content-Type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")

            content_length = resp.headers.get("Content-Length")
            if content_length:
                self.send_header("Content-Length", content_length)

            self.end_headers()
            self.wfile.write(resp.content)

        except httpx.RequestError as e: 
            self.send_error(500, f"Proxy error: {str(e)}")