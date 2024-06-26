FROM python:3.9.12 

WORKDIR /usr/src/app 

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#uvicorn app.main:app --host 0.0.0.0 --port 8000
# docker build -t <imagename> . to build docker image
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]