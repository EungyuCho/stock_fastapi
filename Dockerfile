FROM python:3
WORKDIR /usr/src/app

COPY requirement.txt ./
RUN pip install -r requirement.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "index:app", "--host", "0.0.0.0"]