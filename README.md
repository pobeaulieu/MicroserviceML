
## Start WebApp Locally
1. Create Virtual environment with python 3.8 
```
virtualenv venv
```

2. Activate Virtual environment
```
source venv/bin/activate
```

3. Install requiremnts (Only once)
```
pip install -r requirements.txt
```

4. Train 
 `python -m microminer.embedding.codebert_tuning`
` TODO`
4. Run Webapp
```
python webapp/app.py
```

## Start WebApp with Docker
`docker build -t microminer .`
`docker run --name microminer -d -p 5002:5002 -e PORT=5002 microminer`


