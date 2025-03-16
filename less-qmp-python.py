import http.server
import socketserver
import time
import platform
import psutil
import os

PORT = 8000

def get_system_info():
    try:
        system_info = {}
        system_info['hostname'] = platform.node()
        system_info['platform'] = platform.platform()
        system_info['python_version'] = platform.python_version()
        system_info['uptime'] = time.time() - psutil.boot_time()
        system_info['cpu_percent'] = psutil.cpu_percent(interval=0.1)
        system_info['cpu_count'] = psutil.cpu_count()
        memory = psutil.virtual_memory()
        system_info['total_memory'] = memory.total
        system_info['available_memory'] = memory.available
        system_info['memory_percent'] = memory.percent
        disk = psutil.disk_usage('/')
        system_info['disk_total'] = disk.total
        system_info['disk_free'] = disk.free
        system_info['disk_percent'] = disk.percent
        return system_info
    except Exception as e:
        return {'error': str(e)}

def format_bytes(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def format_uptime(seconds):
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        sys_info = get_system_info()
        cpu_color = "#4CAF50" if sys_info.get('cpu_percent', 0) < 70 else "#FF9800" if sys_info.get('cpu_percent', 0) < 90 else "#F44336"
        memory_color = "#4CAF50" if sys_info.get('memory_percent', 0) < 70 else "#FF9800" if sys_info.get('memory_percent', 0) < 90 else "#F44336"
        disk_color = "#4CAF50" if sys_info.get('disk_percent', 0) < 70 else "#FF9800" if sys_info.get('disk_percent', 0) < 90 else "#F44336"
        uptime_formatted = format_uptime(sys_info.get('uptime', 0))
        total_memory_formatted = format_bytes(sys_info.get('total_memory', 0))
        available_memory_formatted = format_bytes(sys_info.get('available_memory', 0))
        disk_total_formatted = format_bytes(sys_info.get('disk_total', 0))
        disk_free_formatted = format_bytes(sys_info.get('disk_free', 0))
        html = '''<!DOCTYPE html><html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QEMU VM Dashboard</title>
<style>
:root {--bg-color: #121212; --card-bg: #1e1e1e; --text-primary: #ffffff; --text-secondary: #b0b0b0; --accent: #7289da; --divider: #2d2d2d;}
* {box-sizing: border-box; margin: 0; padding: 0;}
body {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-color); color: var(--text-primary); line-height: 1.6; padding: 20px; min-height: 100vh;}
.container {max-width: 1200px; margin: 0 auto;}
header {text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 1px solid var(--divider);}
h1 {font-size: 2.5rem; margin-bottom: 10px; color: var(--accent);}
.subtitle {color: var(--text-secondary); font-size: 1.2rem;}
.stats-container {display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px;}
.card {background-color: var(--card-bg); border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease, box-shadow 0.3s ease;}
.card:hover {transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);}
.card-title {font-size: 1.25rem; margin-bottom: 15px; color: var(--accent); display: flex; align-items: center; gap: 10px;}
.info-row {display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 0.9rem;}
.info-label {color: var(--text-secondary);}
.info-value {font-weight: 500;}
.progress-container {margin-top: 15px;}
.progress-bar {width: 100%; background-color: #2d2d2d; border-radius: 4px; height: 8px; overflow: hidden; margin-top: 5px;}
.progress-fill {height: 100%; border-radius: 4px; transition: width 0.5s ease;}
.system-info {grid-column: 1 / -1;}
.refresh-time {text-align: center; margin-top: 30px; color: var(--text-secondary); font-size: 0.9rem;}
footer {text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--divider); color: var(--text-secondary);}
.card-icon {font-size: 1.5rem;}
@media (max-width: 768px) {.stats-container {grid-template-columns: 1fr;}}
</style></head>
<body><div class="container">
<header><h1>QEMU VM Dashboard</h1><p class="subtitle">System Monitoring Interface</p></header>
<div class="stats-container">
<div class="card system-info"><div class="card-title"><span class="card-icon">💻</span>System Overview</div>
<div class="info-row"><span class="info-label">Hostname:</span><span class="info-value">''' + sys_info.get('hostname', 'Unknown') + '''</span></div>
<div class="info-row"><span class="info-label">Platform:</span><span class="info-value">''' + sys_info.get('platform', 'Unknown') + '''</span></div>
<div class="info-row"><span class="info-label">Python Version:</span><span class="info-value">''' + sys_info.get('python_version', 'Unknown') + '''</span></div>
<div class="info-row"><span class="info-label">System Uptime:</span><span class="info-value">''' + uptime_formatted + '''</span></div>
</div>
<div class="card"><div class="card-title"><span class="card-icon">🔄</span>CPU Usage</div>
<div class="info-row"><span class="info-label">CPU Cores:</span><span class="info-value">''' + str(sys_info.get('cpu_count', 'Unknown')) + '''</span></div>
<div class="info-row"><span class="info-label">CPU Usage:</span><span class="info-value">''' + str(sys_info.get('cpu_percent', 0)) + '''%</span></div>
<div class="progress-container"><div class="progress-bar"><div class="progress-fill" style="width: ''' + str(sys_info.get('cpu_percent', 0)) + '''%; background-color: ''' + cpu_color + ''';"></div></div></div>
</div>
<div class="card"><div class="card-title"><span class="card-icon">🧠</span>Memory</div>
<div class="info-row"><span class="info-label">Total Memory:</span><span class="info-value">''' + total_memory_formatted + '''</span></div>
<div class="info-row"><span class="info-label">Available Memory:</span><span class="info-value">''' + available_memory_formatted + '''</span></div>
<div class="info-row"><span class="info-label">Memory Usage:</span><span class="info-value">''' + str(sys_info.get('memory_percent', 0)) + '''%</span></div>
<div class="progress-container"><div class="progress-bar"><div class="progress-fill" style="width: ''' + str(sys_info.get('memory_percent', 0)) + '''%; background-color: ''' + memory_color + ''';"></div></div></div>
</div>
<div class="card"><div class="card-title"><span class="card-icon">💾</span>Disk</div>
<div class="info-row"><span class="info-label">Total Disk Space:</span><span class="info-value">''' + disk_total_formatted + '''</span></div>
<div class="info-row"><span class="info-label">Free Disk Space:</span><span class="info-value">''' + disk_free_formatted + '''</span></div>
<div class="info-row"><span class="info-label">Disk Usage:</span><span class="info-value">''' + str(sys_info.get('disk_percent', 0)) + '''%</span></div>
<div class="progress-container"><div class="progress-bar"><div class="progress-fill" style="width: ''' + str(sys_info.get('disk_percent', 0)) + '''%; background-color: ''' + disk_color + ''';"></div></div></div>
</div>
</div>
<p class="refresh-time">Last updated: ''' + time.strftime('%Y-%m-%d %H:%M:%S') + '''</p>
<footer><p>QEMU VM Dashboard - Powered by Python</p></footer>
</div>
<script>setTimeout(function() {window.location.reload();}, 5000);</script>
</body></html>'''
        self.wfile.write(html.encode())
        print(f"Received request from {self.client_address[0]}")

print("Starting enhanced web server...")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server started at port {PORT}")
    print(f"Open http://localhost:{PORT} in your browser")
    httpd.serve_forever()
