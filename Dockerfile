FROM python:3.12-slim

WORKDIR /app

RUN apt update && apt upgrade -y 

RUN apt install -y python3-pip python3-venv && \
    apt clean

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"] 
