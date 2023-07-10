# syntax=docker/dockerfile:1

FROM python:3.9-slim
# FROM python:3.9-alpine
EXPOSE 8501
WORKDIR /app

COPY . .
RUN pip3 config set global.index-url 'https://mirrors.aliyun.com/pypi/simple/'\
&& pip3 config set install.trusted-host 'mirrors.aliyun.com'\
&& apt-get update -y\
&& apt-get install -y git \
&& pip3 install -r requirements.txt

ENTRYPOINT ["python3", "-m" , "streamlit", "run","main.py"]
CMD [ "--server.port=8501"]