#!/bin/bash
# startup.sh — Azure App Service runs this to start the app.
# You set this as the "Startup Command" in the Azure Portal.
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
