import os
hostname = "google.com"
response = os.system("ping -n 1 " + hostname)
print(response)
if response == 0:
    pingstatus = "Network Active"
else:
    pingstatus = "Network Error"

print(pingstatus)