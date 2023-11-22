FROM python:3.9

WORKDIR /project_ds

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "final_ds.main:app", "--host", "127.0.0.1", "--port", "8000"]