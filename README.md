# amitad_test

# Установка
1. Установить python 3.6 или более https://www.python.org/downloads/release/python-360/
1. Установить pip
```sudo apt install python3-pip```
1. Скачать исходник 
```git clone https://github.com/drda3x/amitad_test.git ~/amitad_test```
1. Запустить установку
```cd ~/amitad_test && python3 setup.py install```

# Запуск
`python3 ~/amitad_test/winner_app/main.py -H _<app_host_ip>_ -P _<app_port_num>_`

# Использование
После запуска программы поднимется web-сервер на который надо передать исходный JSON-список на
url-адрес `__"http//:_<app_host_ip>_:_<app_port_num>_/"__`
