import psutil
import socket
import platform
import os
from datetime import datetime, timedelta

def get_usage_class(usage_percent):
    """Returns CSS class based on usage percentage."""
    if usage_percent <= 50:
        return "usage-vert"
    elif usage_percent <= 80:
        return "usage-orange"
    else:
        return "usage-rouge"

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
cpu_usage_value = int(cpu_usage)

load1, load5, load15 = psutil.getloadavg()
cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
cpu_per_core_html = ""
for i, usage in enumerate(cpu_per_core):
    css_class = get_usage_class(usage)
    cpu_per_core_html += f'<li>Core {i+1}: <span class="{css_class}">{usage}%</span></li>'


#Memory
mem = psutil.virtual_memory()
total_ram = round(mem.total / (1024 ** 3), 2) 
used_ram = round(mem.used / (1024 ** 3), 2) 
ram_usage = mem.percent
ram_usage_value = int(ram_usage)

# Appliquer la classe CSS à CPU et RAM
cpu_usage_html = f'<span class="{get_usage_class(cpu_usage)}">{cpu_usage}%</span>'
ram_usage_html = f'<span class="{get_usage_class(ram_usage)}">{ram_usage}%</span>'


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
file_extensions = [
    '.txt', '.py', '.pdf', '.jpg', '.png', '.docx', '.xlsx', '.mp3', '.mp4', '.zip'
]
file_counts = {ext:0 for ext in file_extensions}
total_files = 0

# Analyse files

file_counts = {ext: 0 for ext in file_extensions}
file_sizes = {ext: 0 for ext in file_extensions}
total_files = 0
total_size = 0

largest_files = []
MAX_LARGEST = 5

for root, dirs, files in os.walk(folder_to_scan):
    for file in files:
        total_files += 1
        file_path = os.path.join(root, file)
        try:
            size = os.path.getsize(file_path)
        except OSError:
            size = 0

        total_size += size

        for ext in file_extensions:
            if file.lower().endswith(ext):
                file_counts[ext] += 1
                file_sizes[ext] += size
                break

        if len(largest_files) < MAX_LARGEST:
            largest_files.append((size, file_path))
            largest_files.sort(reverse=True)
        else:
            if size > largest_files[-1][0]:
                largest_files[-1] = (size, file_path)
                largest_files.sort(reverse=True)

file_size_percentages = {
    ext: (size / total_size) * 100 if total_size > 0 else 0
    for ext, size in file_sizes.items()
}


# Calculate percentages

file_percentages = {ext: (count / total_files) * 100 if total_files > 0 else 0 for ext, count in file_counts.items()}

#time stamp
 
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Load HTML template

with open("template.html", "r", encoding="utf-8") as f:
    html = f.read()

file_stats_html = ""
for ext in file_extensions:
    file_stats_html += f"<li>{ext}: {file_counts[ext]} fichiers, {file_sizes[ext] / (1024 ** 2):.2f} MB ({file_size_percentages[ext]:.2f}%)</li>"

largest_files_html = ""
for size, path in largest_files:
    size_mb = size / (1024 ** 2)
    largest_files_html += f"<li>{path} - {size_mb:.2f} MB</li>"


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
    "{{ cpu_usage }}": cpu_usage_html,
    "{{ total_ram }}": str(total_ram),
    "{{ used_ram }}": str(used_ram),
    "{{ ram_usage }}": ram_usage_html, 
    "{{ load_avg }}": f"{load1:.2f} / {load5:.2f} / {load15:.2f}",
    "{{ cpu_per_core }}": cpu_per_core_html,
    "{{ cpu_usage_value }}": str(cpu_usage_value),
    "{{ ram_usage_value }}": str(ram_usage_value),
    "{{ top_process_1 }}": format_process(top_process_1),
    "{{ top_process_2 }}": format_process(top_process_2),
    "{{ top_process_3 }}": format_process(top_process_3),
    "{{ text_files }}": str(file_counts[".txt"]),
    "{{ py_files }}": str(file_counts[".py"]),
    "{{ pdf_files }}": str(file_counts[".pdf"]),
    "{{ jpg_files }}": str(file_counts[".jpg"]),
    "{{ file_stats }}": file_stats_html,
    "{{ largest_files }}": largest_files_html,
    "{{ total_files }}": str(total_files),
    "{{ total_size }}": f"{total_size / (1024 ** 3):.2f} GB",
}

# Replace variables in HTML

for key, value in variables.items():
    html = html.replace(key, value)


# Save the final HTML

output = "index.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dashboard generated: {output}")