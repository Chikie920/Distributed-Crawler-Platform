import json
import socketserver
from http.server import BaseHTTPRequestHandler
import urllib.parse
import SpiderUtil

IP = '192.168.146.128'
PORT = 2233

class myHandler(BaseHTTPRequestHandler):
     
    def do_OPTIONS(self):
        # elif self.path == '/'
        self.send_OK('ok')
        return

    def do_GET(self):
        # url = self.path
        if self.path == '/kill_driver':
            SpiderUtil.kill_driver()
            self.send_OK('ok')
        else:
            self.send_Error()
        return
        
    def do_POST(self):
        if self.path == '/create':
            content_length = int(self.headers['Content-Length'])
            if content_length ==0:
                self.send_Error()
                return
            body_bytes = self.rfile.read(content_length)
            body_str = str(body_bytes, encoding = "utf8")
            body = json.dumps(urllib.parse.parse_qs(body_str))
            data = json.loads(bytes(body, encoding = "utf8").decode())
            options = {}
            print(data)
            if 'name' in data:
                job_name = data['name'][0]
            else:
                self.send_Error()
                return

            if 'url' in data:
                job_url = data['url'][0]
            else:
                self.send_Error()
                return

            if 'delay' in data:
                options['DOWNLOAD_DELAY'] = data['delay'][0]

            if 'request_counts' in data:
                options['CONCURRENT_REQUESTS'] = data['request_counts'][0]

            if 'rules' in data:
                options['rules'] = data['rules'][0]
            if 'driver_open' in data and data['driver_open'][0]=='true':
                options['DOWNLOADER_MIDDLEWARES'] = '{"spider.middlewares.SpiderDownloaderMiddleware": 300}'

            self.send_OK('ok')
            SpiderUtil.create_spider(job_name, job_url) # 创建爬虫
            SpiderUtil.run_spider(job_name, options)
        else:
            self.send_Error()
        return
        
    
    def send_OK(self, resp):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header("Content-Length", str(len(resp.encode())))
        self.end_headers()
        self.wfile.write(resp.encode())

    def send_Error(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header("Content-Length", str(len("error".encode())))
        self.end_headers()
        self.wfile.write("error".encode())

with socketserver.TCPServer((IP, PORT), myHandler) as httpd:
    print("Start Server Listening At - ", IP, PORT, "......")
    httpd.serve_forever()