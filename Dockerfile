FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /python_app .

EXPOSE 5000

CMD ["python" , "main.py"]
