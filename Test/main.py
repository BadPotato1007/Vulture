import subprocess
from pathlib import Path
import os
import urllib.request


# get user
user = subprocess.run('whoami', capture_output=True, text=True)
user = user.stdout
print(user)


#get downloads files
downloads_path = str(Path.home() / "Downloads")
os.listdir(downloads_path)
urllib.request.urlretrieve("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAilBMVEUAAAArAFUHAEEFAD8EAEAFAD8EAEALAEAFAEEEAD8EAD8kAEkGAEEEAEAFAEAGAEMEAEAGAEQAt/wAuf4AoeUAuP0ArfIAqu4BaKoDC0kBaKkAs/gAq+8AsvcDBkUAr/MAtvsAouYEAD8ApuoAt/sBZ6kBdrgAr/QBh8oDI2ICOHgCOXkCMG8DCkhLPorkAAAAI3RSTlMABkeVv9nzGJbx/weC9Mcu4y3/////////////////////8ja8OkgAAADfSURBVHgBhZNFAgMhDACDQ+ru7u3u/59XLw1rzJUBovCHcSGV1koKziCPsQ49zhoIqdUbGNCo14LrTczRJI+02lhAu+Pv03NqmO//TSyh+YmjjqXU3x/4+Lu9PoY0Xp9YLBfQAjBXJTgGHKsE5CCoMBg+GY0n6BEgqfBlih4JKhBm8/mi15ujR4GmwnCJuFz11ujRoHNBbqiwBVUtKJDVggSRE3ZUELRQ+97qcDgce70TLRQp9br35UxLDTYnnC60WaTd19vt+iRJSbtjAxMdudjQRsc+vjjx1Ysvb3T9H+irJzSL0LzqAAAAAElFTkSuQmCC", "123.png")

