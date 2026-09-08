#!/usr/bin/env bash
python3 src/main.py "/" "preview"
cd preview && python3 -m http.server 8888
