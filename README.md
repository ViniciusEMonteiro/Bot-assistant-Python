
# Bot-assistant-Python

### Tech

* [Telepot](https://github.com/nickoala/telepot) - Python framework for Telegram Bot API


### Installation

Install the dependencies:
```sh
sudo apt-get install python-dev python-pip
pip install telepot psycopg2 configparser matplotlib pip psycopg2-binary
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

```

### Aplication

```mermaid
graph LR
Message_NEW(New Message)--> Valid_User{Is a User?}
Valid_User -- No --> Action_Create((Create User)) 
Action_Create --> Tab_User[Table User]
Valid_User -- Yes --> Tab_User
Action_Create -- Welcome --> Message_Response(Message to user)
Tab_User -- ID --> Tab_Language[Table Language]
Message_NEW -- Message --> Tab_Language
Tab_Language -- I don't undertand --> Message_Response
Tab_Language -- Undertand --> Tab_Alias[Table Alias]
Tab_Alias -- Values --> Tab_Request[Table Request]
Tab_Alias --> Tab_Service[Table Service]
Tab_Service --> Tab_Request
Tab_Request --> Action_HTTP((Send HTTP)) 
Action_HTTP -- Response --> Message_Response
```

License
----

* [GNU GENERAL PUBLIC LICENSE](https://github.com/ViniciusEMonteiro/Bot-assistant-Python/blob/master/LICENSE)
----