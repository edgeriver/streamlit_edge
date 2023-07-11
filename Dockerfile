# syntax=docker/dockerfile:1

FROM python:3.9-buster as builder-image
# FROM python:3.9-alpine
COPY requirements.txt .
RUN pip3 config set global.index-url 'https://mirrors.aliyun.com/pypi/simple/'\
&& pip3 config set install.trusted-host 'mirrors.aliyun.com'\
# && apt-get update -y\
&& apt-get install -y git\ 
&& pip3 install -r requirements.txt

FROM python:3.9-slim-buster
COPY --from=builder-image /usr/local/bin /usr/local/bin
COPY --from=builder-image /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
EXPOSE 8501
WORKDIR /app
COPY . .
ENTRYPOINT ["python3", "-m" , "streamlit", "run","main.py"]
CMD [ "--server.port=8501"]