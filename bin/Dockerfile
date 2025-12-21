FROM python:3.11-slim

# 设置工作目录
WORKDIR /app
# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 复制源码
COPY src ./src

# 暴露端口
EXPOSE 8080
# 启动命令
CMD ["uvicorn", "main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8080"]
