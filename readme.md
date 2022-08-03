# What?

![Readme image](/readme.png)

# Requirements

Python 3, https://www.python.org/downloads/

# How to?

1. Go to https://www.avanza.se/min-ekonomi/transaktioner.html
2. Download desired transactions as .csv
3. Save to `~/data` folder.
4. Run `python3 app.py`

# Installation

## Backend

(Activate python env, https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)

```bash
cd /zetas-api
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

### During development

```bash
python3 app.py
```

### Testing API

```bash
export FLASK_APP=api.py
export FLASK_DEBUG=true
python3 -m flask run
```

Making API requests:

1. Upload a file with `curl -L -X POST 'http://127.0.0.1:5000' -F 'file=@"/Users/dennisolsson/Develop/zetas-avanza-avg-calculator/zetas-api/uploads/transaktioner_2022-01-01_2022-05-05.csv"'`
2. Calculate return of an already uploaded file with `curl -L -X GET 'http://127.0.0.1:5000/?fileName=transaktioner_2022-01-01_2022-05-05.csv'`

### Docker

```bash
cd /zetas-api
docker run -it -p 5000:5000 --rm $(docker build -q .)
```

## Frontend

```bash
cd /zetas-ui
npm install
npm run dev
```
