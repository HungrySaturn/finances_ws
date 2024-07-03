# finances_ws

web scraping

# Projects
## PyPI
[package-link](https://pypi.org/project/finaces-ws/)
pip install finaces-ws
## Configuration
Create folders and files
```bash
pip install -r requirements-dev.txt --force
mkdir data
cd data
echo { } > dataX.json
cd ..


[config.py](app/endpointFiller/config.py)
- Change domain/port
```bash
DOMAIN = "http://127.0.0.1"
PORT = "32800"
```
