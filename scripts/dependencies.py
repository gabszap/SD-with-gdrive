import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


packages = [
    "google-auth",
    "google-auth-oauthlib",
    "google-auth-httplib2",
    "google-api-python-client",
    "gradio"
]

for package in packages:
    install(package)
