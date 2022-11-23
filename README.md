
# Bot-assistant-Python

### Tech

* [Telepot](https://github.com/nickoala/telepot) - Python framework for Telegram Bot API


### Installation

Install the dependencies:
```sh
sudo apt-get install python-dev python-pip libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev
pip install telepot psycopg2 configparser matplotlib pip psycopg2-binary opencv-python numpy
```


Clone the aplication:
```sh
git clone https://github.com/ViniciusEMonteiro/Bot-assistant-Python.git
cd Bot-assistant-Python/
```

Start aplication:
```sh
python main.py
```

Or start in background:
```sh
nohup python main.py &
```

Or create a service to run:
```sh
nano /lib/systemd/system/meu-script.service
```

```sh
Unit]
Description=Script para inciar o Bot
Wants=network-online.target
After=network.target

[Service]
Type=simple
User=labra
WorkingDirectory=/seu/diretorio
ExecStart=/seu/diretorio/Bot-assistant-Python/main.py
Restart=on-failure
RestartSec=1

[Install]
WantedBy=multi-user.target
```

```sh
sudo systemctl daemon-reload
sudo systemctl start meu-script
sudo systemctl status meu-script
sudo systemctl enable meu-script
```

And create config file:

```sh
Bot_Name = Teste
Bot_hash = Teste
BD_IP = 127.0.0.1
BD_Port = 5432
BD_Name = teste_bd
BD_User = teste
BD_Pass = Secret

```

### LICENSE
----

* [GNU GENERAL PUBLIC LICENSE](https://github.com/ViniciusEMonteiro/Bot-assistant-Python/blob/master/LICENSE)
----
