#!/bin/sh

# Build emojiscraper executable
#pyinstaller --console --collect-all requests emojiscraper.py

# Build stickerscraper executable
#pyinstaller --console --collect-all requests --collect-all apnggif stickerscraper.py

make clean
make build