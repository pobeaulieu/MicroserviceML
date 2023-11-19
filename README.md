## Python environment 
- Python 3.8.18
- All requirements are in folder `requirements.txt`
- Command to install all dependencies: `pip3.8 install -r requirements.txt`

## Start WebApp Locally
- `cd webapp`
- `python3.8 app.py`
- MicroMiner will be available at `http://127.0.0.1:5001`

## Start WebApp with Docker
`docker build -t microminer .`
`docker run --name microminer -d -p 5002:5002 -e PORT=5002 microminer`
- MicroMiner will be available at `http://127.0.0.1:5002`


