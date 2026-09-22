import http.server
import socketserver
import os
import sys

PORT = 3000

class ReadmePreviewHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            try:
                with open('README.md', 'r', encoding='utf-8') as f:
                    readme_content = f.read()
            except Exception as e:
                readme_content = f"# Error reading README.md: {e}"

            # Escape backticks and backslashes for JS template literal
            escaped_md = (
                readme_content
                .replace('\\', '\\\\')
                .replace('`', '\\`')
                .replace('$', '\\$')
            )

            html = f"""<!DOCTYPE html>
<html lang="en" data-color-mode="dark" data-dark-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GitHub Profile Preview - Koushik Goud Shaganti</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-dark.min.css">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body {{
      box-sizing: border-box;
      min-width: 200px;
      max-width: 980px;
      margin: 0 auto;
      padding: 45px;
      background-color: #0d1117;
      color: #c9d1d9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    }}
    .preview-header {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 16px 24px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .preview-tag {{
      display: inline-block;
      padding: 4px 10px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 20px;
      background: #238636;
      color: #ffffff;
    }}
    .markdown-body {{
      box-sizing: border-box;
      background-color: #0d1117 !important;
      border: 1px solid #30363d;
      border-radius: 12px;
      padding: 36px;
    }}
    .markdown-body table {{
      display: table !important;
      width: 100% !important;
    }}
    .markdown-body img {{
      max-width: 100%;
      background-color: transparent;
    }}
  </style>
</head>
<body>
  <div class="preview-header">
    <div>
      <span class="preview-tag">LIVE LOCALHOST PREVIEW</span>
      <strong style="margin-left: 10px; font-size: 16px;">GitHub Profile README: koushik1133/koushik1133</strong>
    </div>
    <div style="font-size: 13px; color: #8b949e;">
      Running on <code>http://localhost:{PORT}</code>
    </div>
  </div>

  <article class="markdown-body" id="content">
    Loading preview...
  </article>

  <script>
    marked.setOptions({{
      gfm: true,
      breaks: true
    }});
    const markdownText = `{escaped_md}`;
    document.getElementById('content').innerHTML = marked.parse(markdownText);
  </script>
</body>
</html>"""
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
            return
        
        # Serve assets and static files
        super().do_GET()

if __name__ == '__main__':
    # Try PORT or PORT+1
    for p in [3000, 3001, 8080]:
        try:
            socketserver.TCPServer.allow_reuse_address = True
            with socketserver.TCPServer(("", p), ReadmePreviewHandler) as httpd:
                PORT = p
                print(f"Preview server running at http://localhost:{p}")
                sys.stdout.flush()
                httpd.serve_forever()
        except OSError:
            continue
