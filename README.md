## Python environment 
- Python 3.8.18
- All requirements are in folder `requirements.txt`
- Command to install all dependencies: `pip3.8 install -r requirements.txt`

## Start WebApp Locally
- `cd webapp`
- `python3.8 microminer.py`
- MicroMiner will be available at `http://127.0.0.1:5000`

## Start WebApp with Docker
`docker build -t microminer .`
`docker run -d -p 5001:5001 -e PORT=5001 microminer`
- MicroMiner will be available at `http://127.0.0.1:5001`


