#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import os

working_dir = '/var/lib/version-counter/'

def iterate_counter(repo, ver):

    data = {}
    try:
        json_file = open(working_dir + 'db.json', 'r')
        data = json.load(json_file)
        logging.info("read JSON from file")
    except Exception as e:
        logging.info("{0}".format(e))
        logging.info("JSON file will be created")

    if repo not in data:
        data[repo] = {ver: 0}
    if ver not in data[repo]:
        data[repo].update({ver: 0})
    data[repo][ver] += 1

    with open(working_dir + 'db.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return data[repo][ver]

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers(

    )
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        repo = self.path.split('&')[0][1:]
        ver = self.path.split('&')[1]
        print("repository name is \"{}\"".format(repo))
        print("version is \"{}\"".format(ver))
        if not repo:
            logging.error("Repository name is empty!")
            return
        if not ver:
            logging.error("Version is empty!")
            return

        new_ver = iterate_counter(repo, ver)
        self._set_response()
        self.wfile.write("{}".format(new_ver).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=11011):
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

