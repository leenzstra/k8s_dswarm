#!/bin/bash

echo "Installing ultralytics"
pip install ultralytics==8.2.14

echo "Starting server"
python server_hub.py --host "${host}" --port_hub "${port_hub}" --port_web "${port_web}"