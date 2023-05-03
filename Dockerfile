FROM ubuntu
RUN apt update
RUN apt install -y  python3 python3-pip
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src src
COPY tickers.txt .
WORKDIR /app/src

ENTRYPOINT ["python3", "main.py", "--sim"]