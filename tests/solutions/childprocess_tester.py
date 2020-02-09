import subprocess

while True:
    subprocess.Popen("python3 || python", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
