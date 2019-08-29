from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests
from requests.exceptions import HTTPError, ConnectionError

# AUTHOR: L. Diaz
# DATE CREATED: 27/08/2019
# LAST EDITED: 27/08/2019

#   On a GET request to the / path, it displays an HTML form with two fields. One field is where you put the long URI you want to shorten. The other is where you put the short name you want to use for it. Submitting this form sends a POST to the server.
#   On a POST request, the server looks for the two form fields in the request body. If it has those, it first checks the URI with requests.get to make sure that it actually exists (returns a 200).
#       If the URI exists, the server stores a dictionary entry mapping the short name to the long URI, and returns an HTML page with a link to the short version.
#       If the URI doesn't actually exist, the server returns a 404 error page saying so.
#       If either of the two form fields is missing, the server returns a 400 error page saying so.
#   On a GET request to an existing short URI, it looks up the corresponding long URI and serves a redirect to it.
#
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=UTF-8')
        self.end_headers()
        with open('index.html', 'r') as file:
            for line in file:
                self.wfile.write(line.encode())

    def do_POST(self):
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()


if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()