from http.server import BaseHTTPRequestHandler, HTTPServer

description = """
Reads a JSON schema model in JSON our YAML and start a simple http server on a given
port. A simple request on that port with `/{TYPENAME}` will return random data
of that type.
"""


hostName = "localhost"
serverPort = 8080


class RandomServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        pathAndParameters = self.path.split("?")
        currentPath = pathAndParameters[0]
        parameters = {}
        if len(pathAndParameters) > 1:
            for p in pathAndParameters[1].split("&"):
                keyAndValue = p.split("=")
                if len(keyAndValue) == 2:
                    parameters[keyAndValue[0]] = keyAndValue[1]
        content = '{{"path": "{}", parameters: {}}}'.format(currentPath, parameters)
        self.wfile.write(bytes(content, "utf-8"))


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), RandomServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
