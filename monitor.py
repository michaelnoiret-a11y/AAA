#import psutil
import socket
import platform
import os
from datetime import datetime, timedelta
import html

html = open("template.html").read()
"""print(html)
{{ TIME_STAMP }} = ""
{{ HOST_NAME }} = ""
{{ OS }} = ""
name = {{HOST_NAME}}.replace("{{ HOST_NAME }}", "hostname")
print(name)
"""
current_date = datetime.now().strftime(" %Y %B %d %H:%M:%S")
#html = html.replace("{{TIME_STAMP}}", current_date)

# Informations sur le processeur:
"""cpu-count = psutil.cpu_count()
cpu-freq = psutil.cpu_freq()
cpu-percent = psutil.cpu_percent()
#print(cpu-count)
# Informations sur la mémoire:
psutil.virtual_memory() # conversion bytes en GB nécessaire
                        # conversion bytes en GB nécessaire
                        # pourçentage utilisation de la RAM"""
# Informations Système générales:
"""hostname = platform.node()
{{ HOST_NAME }} = hostname
os = platform.platform()
{{ OS }} = os
print
#boot-time = psutil.boot_time()
#uptime = psutil.
#users = psutil.users()

#Informations sur les réseaux:
ip = psutil.net_if_addrs()

# Informations sur les processus:
psutil.process_iter() #  liste des processus en cours consommation CPU en pouçentage 
#psutil.               #  liste des processus en cours consommation RAM en pourçentage
#psutil.           #  Top 3 des processus les plus gourmands
# Analyse de fichiers

{{HOST_NAME}} = hostname"""





with open("index.html" , "w") as fp:
    fp.write(html)