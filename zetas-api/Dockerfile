FROM amancevice/pandas:alpine

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . /app

ENV FLASK_APP=api.py
ENV FLASK_DEBUG=True

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]