FROM python:3.11
WORKDIR /app
COPY requirements.txt /
RUN pip install -r /requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . /app
CMD ["python","main.py"]
