import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "cx_freeze"])
from cx_Freeze import setup, Executable

options_stickerscraper = {
    "includes": ["requests", "apnggif"],
    "packages": ["sys", "subprocess", "os", "time"],
    "excludes": [],
    "include_files": []
}

options_emojiscraper = {
    "includes": ["requests"],
    "packages": ["sys", "subprocess", "os", "time"],
    "excludes": [],
    "include_files": []
}

setup(
    name = "",
    description = "",
    options = {},
    executables = [Executable(script="stickerscraper.py")]
)