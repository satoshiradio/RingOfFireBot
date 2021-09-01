Instructions below are for Ubuntu 20.04.2 LTS (Focal).

# Install python

```shell
sudo apt install python3.9 python3.9-venv python3-dev
```

# Download and install the mariadb connector

Go to https://downloads.mariadb.com/Connectors/c/connector-c-3.2.4/ and download the right archive for your system

Set the MARIADB_CONFIG environment variable
```shell
export MARIADB_CONFIG=~/Downloads/mariadb-connector-c-3.2.4-ubuntu-focal-amd64/bin/mariadb_config
```

# Create a virtual env and install requirements

```shell
python3 -m venv rofbot-env
source rofbot-env/bin/activate
(rofbot-env) python -m pip install wheel
(rofbot-env) python -m pip install -r requirements.txt 
```

# Setup your config.py 

```shell
mv config.py.example config.py
``` 
and edit file
