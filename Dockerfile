FROM python:3.9.13

#Where to install Python - roject directory
WORKDIR /usr/src/app

#Where the requirements.txt is
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install itsdangerous==2.0.1

EXPOSE 5000

COPY . .

CMD ["python", "run.py", "--host=0.0.0.0"]
