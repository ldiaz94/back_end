from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests
from requests.exceptions import HTTPError, ConnectionError

# AUTHOR: L. Diaz
# DATE CREATED: 27/08/2019
# LAST EDITED: 31/08/2019


# DATABASE:
db = {}
# Placeholders
ph = ['','','']

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if a shorty was used:
        path = self.path
        if path == "/index.html" or path == '/':
            # Load main homepage
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
        else:
            if db.get(path[1:]):
                self.send_response(303)
                self.send_header("Location", db[path[1:]])
                self.end_headers()
            else:
                self.send_error(404)

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
                    # Original task wanted:
                    # self.send_error(404) # but I feel this handling is better
                    return()
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