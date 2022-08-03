# What?

![Readme image](/readme.png)

# Requirements

Python 3, https://www.python.org/downloads/

# How to?

1. Go to https://www.avanza.se/min-ekonomi/transaktioner.html
2. Download desired transactions as .csv
3. Save to `~/data` folder.
4. Edit DESIRED_ACCOUNT and FILE values in `app.py`
5. Activate python env, https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments
6. Run `python3 app.py`

# Docker

Run `docker run -it -p 5000:5000 --rm $(docker build -q .)`

# UI

Run `npm start`

# API

1. Start server with `flask run`
2. Upload a file with `curl -L -X POST 'http://127.0.0.1:5000/upload' -F 'file=@"/Users/dennisolsson/Develop/zetas-avanza-avg-calculator/uploads/transaktioner_2022-01-01_2022-07-04.csv"'`
3. Calculate return with `curl -L -X POST 'http://127.0.0.1:5000/calculate' -F 'filename="transaktioner_2022-01-01_2022-07-04.csv"'`
