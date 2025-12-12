import psutil
import socket
import platform
import os
from datetime import datetime, timedelta

#System Information

hostname = platform.node()
os_name = f"{platform.system()} {platform.release()}"
boot_time = datetime.fromtimestamp(psutil.boot_time())
uptime = str(datetime.now() - boot_time).split('.')[0]
user_count = len(psutil.users())

#Cpu information

cpu_cores =  psutil.cpu_count(logical=True)
cpu_frequency = psutil.cpu_freq().current if psutil.cpu_freq() else 0
cpu_usage = psutil.cpu_percent(interval=1)

#Memory
mem = psutil.virtual_memory()
total_ram = round(mem.total / (1024 ** 3), 2) 
used_ram = round(mem.used / (1024 ** 3), 2) 
ram_usage = mem.percent

#Network

ip_address = socket.gethostbyname(socket.gethostname())

#Process formatting function

def format_process(proc):
    if proc is None:
        return "N/A"
    return f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%, RAM: {proc['memory_percent']:.2f}%"


#Processes

processes = []
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
    try:
        processes.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

cpu_sorted = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)

ram_sorted = sorted(processes, key=lambda p: p['memory_percent'], reverse=True)

# Top 3 processes by CPU and RAM
top_process_1 = cpu_sorted[0] if len(cpu_sorted) > 0 else None
top_process_2 = cpu_sorted[1] if len(cpu_sorted) > 1 else None
top_process_3 = cpu_sorted[2] if len(cpu_sorted) > 2 else None

#Files statistic

folder_to_scan = os.path.expanduser("~/Documents")  # Changez le chemin si besoin
file_extensions = ['.txt', '.py', '.pdf', '.jpg']
file_counts = {ext:0 for ext in file_extensions}
total_files = 0

# Analyse files

for root, dirs, files in os.walk(folder_to_scan):
    for file in files:
        total_files += 1
        for ext in file_extensions:
            if file.lower().endswith(ext):
                file_counts[ext] += 1

# Calculate percentages

file_percentages = {ext: (count / total_files) * 100 if total_files > 0 else 0 for ext, count in file_counts.items()}

#time stamp
 
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Load HTML template

with open("template.html", "r", encoding="utf-8") as f:
    html = f.read()

#  Replace variables in HTML {{}}   

variables = {
    "{{ timestamp }}": timestamp,
    "{{ hostname }}": hostname,
    "{{ os_name }}": os_name,
    "{{ boot_time }}": str(boot_time),
    "{{ uptime }}": uptime,
    "{{ user_count }}": str(user_count),
    "{{ ip_address }}": ip_address,
    "{{ cpu_cores }}": str(cpu_cores),
    "{{ cpu_frequency }}": str(cpu_frequency),
    "{{ cpu_usage }}": str(cpu_usage),
    "{{ total_ram }}": str(total_ram),
    "{{ used_ram }}": str(used_ram),
    "{{ ram_usage }}": str(ram_usage),
    "{{ top_process_1 }}": format_process(top_process_1),
    "{{ top_process_2 }}": format_process(top_process_2),
    "{{ top_process_3 }}": format_process(top_process_3),
    "{{ total_files }}": str(total_files),
    "{{ text_files }}": str(file_counts[".txt"]),
    "{{ py_files }}": str(file_counts[".py"]),
    "{{ pdf_files }}": str(file_counts[".pdf"]),
    "{{ jpg_files }}": str(file_counts[".jpg"]),
}

# Replace variables in HTML

for key, value in variables.items():
    html = html.replace(key, value)


# Save the final HTML

output = "dashboard.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dashboard generated: {output}")