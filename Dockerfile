FROM python:3
WORKDIR /
RUN mkdir -p /app
COPY *.py /app/
COPY .env /app/
COPY requirements.txt /app/
RUN apt-get -y install libc-dev
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt
CMD ["python3", "/app/main.py"]