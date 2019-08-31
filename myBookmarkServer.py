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

# DATABASE:
db = {}
# Placeholders
ph = ['','','']

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Placeholder count
        ph_count = 0

        # Send response and header
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=UTF-8')
        self.end_headers()

        # Fetch index.html and substitute placeholders
        with open('index.html', 'r') as file:
            for line in file:
                # Find python injection placeholders (can be refined)
                ind = line.find('$P$')
                if ind != -1:
                    line = line[0:ind] + ph[ph_count] + line[ind+3:]
                    # Reset ph
                    ph[ph_count] = ''
                    ph_count += 1
                
                self.wfile.write(line.encode())

    def do_POST(self):
        # Get the length of the request for reading
        qsLength = int(self.headers.get('Content-length',0))
        
        # Read the data and decode (bytes) from the request rfile
        query = self.rfile.read(qsLength).decode()

        # Form sends two fields: uri & shorty
        parsedQuery = parse_qs(query)
        uriData = parsedQuery.get('uri')
        shortyData = parsedQuery.get('shorty')
        
        # Check form's inputs
        if uriData:
            if shortyData:
                # Check if uri is valid
                # First add schema if not in URI
                if uriData[0].find("https://") !=0:
                    uriData[0] = "https://" + uriData[0]
                    print(uriData[0])
                # Then do a request for the uri
                try:
                    response = requests.get(uriData[0])
                    if response.status_code == 200:
                        db[shortyData[0]] = uriData[0] #Only add when its a valid URI
                        ph[2] = '<em style=\'color:blue\'>{} succesfully added as {}</em>'.format(uriData[0],shortyData[0])
                except: # Dangerous and needs FIXME!
                    ph[0] = '<em style=\'color:red\'>Please enter a valid URI and bookmark</em>'
            else:
                # Add "Please enter valid short" error
                ph[1] = "<em style=\'color:red\'>Please enter a valid short</em>"
                
        elif shortyData:
            # Add "Please enter valid URI" error
            ph[0] = "<em style=\'color:red\'>Please enter a URI</em>"
            
        else:
            # Add "Please enter valid URI" and "Please enter valid shorty"
            ph[2] = "<em style=\'color:red\'>No values entered</em>"

        print(db)
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()


if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()