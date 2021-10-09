FROM python:3.8-slim-buster
COPY . /code
WORKDIR /code
RUN cp -r sources.list /etc/apt/sources.list
RUN apt update -y && apt install libreoffice -y
RUN cp simsun.ttc /usr/share/fonts && cd /usr/share/fonts && chmod 644 simsun.ttc && fc-cache -fv
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5000
CMD python3 main.py