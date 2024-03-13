import base64
import json
import socketserver
from http.server import BaseHTTPRequestHandler
import urllib.parse
import SpiderUtil
import time
import NewsAnalysis
import os

IP = '127.0.0.1'
PORT = 2233

class myHandler(BaseHTTPRequestHandler):
     
    def do_OPTIONS(self):
        self.send_OK('ok')
        return

    def do_GET(self):
        # url = self.path
        self.send_OK('ok')
        return
        
    def do_POST(self):
        # print(self.path)
        if self.path == '/create':
            content_length = int(self.headers['Content-Length'])
            if content_length ==0:
                self.send_Error()
                return
            body_bytes = self.rfile.read(content_length)
            body_str = str(body_bytes, encoding = "utf8")
            body = json.dumps(urllib.parse.parse_qs(body_str))
            # print('***********')
            # print(body)
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

            # if 'cookie' in data:
            #     options['cookie'] = data['cookie']
            if 'rules' in data:
                # rules = data['rules'][0]
                options['rules'] = data['rules'][0]
                # rule_list = rules.split(', ')
                # for item in rule_list:
                #     options['rules']+=(Rule(LinkExtractor(allow=r"%s" % item), callback="parse_item", follow=True),)
            if 'driver_open' in data and data['driver_open'][0]=='true':
                options['DOWNLOADER_MIDDLEWARES'] = '{"spider.middlewares.SpiderDownloaderMiddleware": 300}'

            self.send_OK('ok')
            # print(job_name, job_url, options)
            SpiderUtil.create_spider(job_name, job_url) # 创建爬虫
            # time.sleep(3)
            SpiderUtil.run_spider(job_name, options)
        elif self.path == '/wordCloud':
            content_length = int(self.headers['Content-Length'])
            if content_length ==0:
                self.send_Error()
                return
            body_bytes = self.rfile.read(content_length)
            body_str = str(body_bytes, encoding = "utf8")
            body = json.dumps(urllib.parse.parse_qs(body_str))
            data = json.loads(bytes(body, encoding = "utf8").decode())
            content = data['content'][0]
            if NewsAnalysis.draw_wordcloud(content) == True:
                self.send_wordCloud()
        elif self.path == '/sentiment':
            content_length = int(self.headers['Content-Length'])
            if content_length ==0:
                self.send_Error()
                return
            body_bytes = self.rfile.read(content_length)
            body_str = str(body_bytes, encoding = "utf8")
            body = json.dumps(urllib.parse.parse_qs(body_str))
            data = json.loads(bytes(body, encoding = "utf8").decode())
            content = data['content'][0]
            res = NewsAnalysis.sentiment_analysis(content)
            self.send_OK(res)
        return
    
    def send_wordCloud(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        file = open('./wordCloud.jpg', 'rb')
        img_base64 = base64.b64encode(file.read())
        self.wfile.write(img_base64)
        file.close()
        # self.send_header("Content-Length", str(os.path.getsize('./wordCloud.jpg')))
        
    
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