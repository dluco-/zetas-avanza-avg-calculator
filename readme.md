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

Run `docker run -it --rm $(docker build -q .)`
