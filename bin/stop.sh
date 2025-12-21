#!/bin/bash

PID=$(ps aux | grep uvicorn | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
  echo "Uvicorn is not running"
else
  kill -9 $PID
  echo "Stopping Uvicorn PID: $PID"
fi