#!/bin/bash

# 根目录
APP_HOME=$(cd "$(dirname "$0")/.." && pwd)

# 日志目录
LOG_DIR="$APP_HOME/logs"
LOG_FILE="$LOG_DIR/uvicorn.log"

# Uvicorn 可执行文件
UVICORN_BIN="/usr/local/python311/bin/uvicorn"

# 创建日志目录（如果不存在）
mkdir -p "$LOG_DIR"

# 启动服务
nohup "$UVICORN_BIN" \
  --app-dir "$APP_HOME/src" \
  main:app \
  --host 0.0.0.0 \
  --port 8080 \
  > "$LOG_FILE" 2>&1 &

echo "Uvicorn started, PID: $!"