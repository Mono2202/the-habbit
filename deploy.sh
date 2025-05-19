#!/bin/bash

fuser -k 5002/tcp
fuser -k 5003/tcp

cd backend
nohup gunicorn app:app --bind 0.0.0.0:5003 > output.log 2>&1 &

cd ../frontend
nohup npm start > output.log 2>&1 &

cd ..
