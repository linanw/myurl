"""
URL redirection example.
"""
import concurrent.futures
import http.server
import time
import sys
import os
import re
import json
from urllib.parse import urlparse
from urllib.request import urlopen


LOG_PATH = './'
ACCESS_RIGHTS = 0o755
HOST_NAME = ''  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080  # Maybe set this to 9000.


def log_to_file(s, logPath):
    if not os.path.exists(logPath):
        try:
            os.mkdir(logPath, ACCESS_RIGHTS)
        except OSError:
            print("Creation of the directory %s failed" % logPath)
        else:
            print("Successfully created the directory %s" % logPath)
    filename = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + \
        '_' + str(time.time()).replace('.', '') + '.txt'
    print('filename: ' + filename)
    print('X-Real-IP: ' + str(s.headers['X-Real-IP']))
    f = open(logPath + '/' + filename, 'w')
    f.write(str(s.headers))
    f.write(str(s.requestline) + '\n')
    f.close()
    if s.headers['X-Real-IP'] is not None:
        response = urlopen('http://ipinfo.io/' + s.headers['X-Real-IP'] + '/json')
        data = json.load(response)
        print(data['country'])
        f = open(logPath + '/' + filename, 'a')
        f.write(str(data))
        f.close()
        os.rename(logPath + '/' + filename, logPath + '/' +
                    filename.split('.txt')[0] + '_' + data['country'] + '.txt')


def redirect(s, redirectUrl):
    s.send_response(301)
    # REDIRECTIONS.get(s.path, LAST_RESORT))
    s.send_header("Location", redirectUrl)
    s.end_headers()


class RedirectHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        print('path: ' + s.path)
        o = urlparse(s.path,  allow_fragments=True)
        print(o.netloc)
        print('o.path: ' + o.path)
        print('o.query: ' + o.query)
        print('o.params: ' + o.params)
        print('o.query: ' + o.query)
        if o.path[1:].startswith('bbf'):
            redirectUrl = 'https://www.youtube.com/channel/UCTZhtqLXebU-4IZRAYxam1g'
        elif o.query=='':
            redirectUrl = 'https://ipinfo.io/json'
        else:
            redirectUrl = 'https://' + o.query
        print('redirectUrl: ' + redirectUrl)
        if o.path[1:] == '':
            logPath = LOG_PATH + 'default'
        else:
            logPath = LOG_PATH + o.path[1:]
        print('logPath: ' + logPath)
        print('header keys: ' + str(s.headers.keys()))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.submit(log_to_file, s, logPath)
            executor.submit(redirect, s, redirectUrl)

    def do_GET(s):
        s.do_HEAD()


if __name__ == '__main__':
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), RedirectHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
