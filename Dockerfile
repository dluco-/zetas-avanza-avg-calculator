FROM amancevice/pandas:alpine

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . /app

CMD ["python", "app.py"]