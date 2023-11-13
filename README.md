## Python environment 
- Python 3.8.18
- All requirements are in folder `requirements.txt`
- Command to install all dependencies: `pip3.8 install -r requirements.txt`

## Start WebApp Locally
- `python3.8 ./webapp/microminer.py`
- MicroMiner will be available at `http://127.0.0.1:4000`

## Start WebApp with Docker
`docker build -t microminerv2 .`
`docker run -d -p 4001:4001 -e PORT=4001 microminerv2`
- MicroMiner will be available at `http://127.0.0.1:4001`


