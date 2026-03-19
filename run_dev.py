import http.server
import socketserver
import os
import re
import urllib.request
import urllib.error

PORT = 3000
BACKEND_URL = "http://localhost:5000"

class ViteIncludeHandler(http.server.SimpleHTTPRequestHandler):
    def handle_proxy(self):
        url = f"{BACKEND_URL}{self.path}"
        print(f"[Proxy] {self.command} {self.path} -> {url}")
        
        try:
            # Read request body for POST
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Prepare headers
            headers = {k: v for k, v in self.headers.items() if k.lower() not in ['host', 'content-length']}
            
            # Send request to backend
            req = urllib.request.Request(url, data=body, headers=headers, method=self.command)
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for key, value in response.getheaders():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            print(f"[Proxy] Error: {str(e)}")
            self.send_error(500, str(e))

    def do_POST(self):
        if self.path.startswith('/api/'):
            return self.handle_proxy()
        return super().do_POST()

    def do_GET(self):
        if self.path.startswith('/api/'):
            return self.handle_proxy()
            
        # Default to index.html if root is requested
        request_path = self.path
        if request_path == '/':
            request_path = '/index.html'
            
        # Remove query parameters if any
        request_path = request_path.split('?')[0]
        
        # Get the absolute path of the requested file
        file_path = os.path.join(os.getcwd(), request_path.lstrip('/'))
        
        # If it's an HTML file, process the includes
        if file_path.endswith('.html') and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Replace <!-- include: ... --> with actual content
                def replacer(match):
                    include_path = match.group(1).strip()
                    include_full_path = os.path.join(os.getcwd(), include_path)
                    if os.path.exists(include_full_path):
                        with open(include_full_path, 'r', encoding='utf-8') as inc_f:
                            return inc_f.read()
                    else:
                        print(f"[Run Dev] File not found: {include_full_path}")
                        return f"<!-- ERROR: Could not include {include_path} -->"
                        
                processed_content = re.sub(r'<!--\s*include:\s*(.+?)\s*-->', replacer, content)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(processed_content.encode('utf-8'))))
                self.end_headers()
                self.wfile.write(processed_content.encode('utf-8'))
                return
            except Exception as e:
                self.send_error(500, f"Error processing HTML: {str(e)}")
                return
                
        # For all other files, use the default handler
        return super().do_GET()

# Ensure we're in the right directory
os.chdir('e:/Work/Python/Director_website')

with socketserver.ThreadingTCPServer(("", PORT), ViteIncludeHandler) as httpd:
    print(f"🚀 Serving frontend at http://localhost:{PORT} (with /api proxy to {BACKEND_URL})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")

