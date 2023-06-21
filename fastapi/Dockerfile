FROM python:3.9
RUN mkdir /fastapi
WORKDIR /fastapi
RUN apt-get update && \
    apt-get install -y libmariadb-dev
RUN pip install --no-build-isolation mysql-connector-python
COPY requirements.txt /fastapi/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python3", "main.py"]