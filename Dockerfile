# 使用此基础镜像，不需要改动
FROM python:3.7

MAINTAINER yuki

## 创建 code 文件夹并将其设置为工作目录
WORKDIR /workspace

## 更新 apt-get
RUN apt-get update && apt-get install -y vim

## 更新 pip
RUN pip install pip -U

## 将 requirements.txt 复制到容器的 workspace 目录
ADD requirements.txt /workspace/

## 安装库
RUN pip install -r requirements.txt

## 将当前目录复制到容器的 workspace 目录
ADD . /workspace/

# 设置启动命令
CMD [ "/bin/bash", "-ce", "python /workspace/start.py" ]
#EXPOSE 8008