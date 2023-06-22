# syntax=docker/dockerfile:1

FROM python:3.9-slim
# FROM python:3.9-alpine
EXPOSE 8501
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 config set global.index-url 'https://mirrors.aliyun.com/pypi/simple/'
RUN pip3 config set install.trusted-host 'mirrors.aliyun.com'
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "-m" , "streamlit", "run","main.py"]
CMD [ "--server.port=8501"]