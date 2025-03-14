#!/bin/bash

# Start Flet server in the background
flet run --web --port=8080 &

# Start HTTP server for static files
python -m http.server 8081 --directory static
