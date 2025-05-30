FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app

# 安装依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 暴露端口（如有需要可改为其它端口）
EXPOSE 5050

# 启动命令
CMD ["python", "app/__init__.py"]