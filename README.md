### Пример создания сервиса классификации изображений

В данном репозитории реализован код и инструкции для создания и запуска сервиса классификации изображений: от этапа обучения модели до деплоя в виде API сервиса в Docker-контейнере.

### Обучение модели

Перед запуском процесса обучения необходимо установить зависимости:
```bash
pip install -r dependencies/train.requirements.txt
```

Код для загрузки датасета, создания и обучения модели и её конвертации в ONNX приведён в jupyter-ноутбуке <i>notebooks/train.ipynb</i>.

В результате выполнения всех ячеек в ноутбуке в папке с проектом должны появиться директории <i>dataset</i> и <i>model</i>.
В директории <i>dataset</i> будут располагаться подпапки с датасетами для обучения, валидации и тестирования модели.
В директории <i>model</i> будут располагаться файлы <i>model_state_dict.pth</i> (файл с весами обученной модели) и <i>model.onnx</i> (модель в формате ONNX).

### Настройка DVC

Перед настройкой DVC необходимо создать внешнее хранилище данных и убедиться, что в вашем проекте инициализирован git. Для данного примера воспользуемся Google Drive.
Для настройки DVC с хранилищем в Google Drive необходимо выполнить следующее:
1. Выполнить команду инициализации DVC:
```bash
dvc init
```
2. Создать папку в Google Drive.
3. Зайти в созданную папку и скопирать идентификатор папки из URL (в адресной строке браузера).
> Например, для URL https://drive.google.com/drive/folders/0AIac4JZqHhKmUk9PDA идентификатором будет являться <i>0AIac4JZqHhKmUk9PDA</i>.
4. Добавить папку в Google Drive в качестве удалённого хранилища для DVC:
```bash
dvc remote add --default origin gdrive://0AIac4JZqHhKmUk9PDA
dvc remote modify origin gdrive_acknowledge_abuse true
```

### Загрузка модели в удалённое хранилище через DVC

Для того, чтобы загрузить модель в Google Drive через DVC, воспользуйтесь следующими командами:
```bash
dvc add model
dvc push
```

Во время выполнения команды <i>dvc push</i> будет необходимо пройти аутентификации в Google (автоматически откроется вкладка в браузере).
В папке с проектом должен появиться файл <i>model.dvc</i> и в файл <i>.gitignore</i> должна записаться строчка /model.

В созданной в Google Drive папке должна появиться директория <i>files/md5</i>.

### Скачивание модели из удалённого хранилища через DVC

Для загрузки модели при наличии в репозитории папки с расширением <i>.dvc</i> и файла <i>model.dvc</i> можно воспользоваться следующей командой:
```bash
dvc pull
```
### Сборка Docker-образа

Можно собрать два варианта Docker-образов: для инференса модели на CPU или на GPU.

Команда для сборки образа под запуск на CPU:
```bash
docker build -f cpu.Dockerfile -t cat-dog-classification-service:cpu .
```

Команда для сборки образа под запуск на GPU:
```bash
docker build -f gpu.Dockerfile -t cat-dog-classification-service:gpu .
```

### Запуск Docker-контейнера с сервисом

Запуск Docker-контейнера может быть из двух вариантов Docker-образа: для инференса модели на CPU или на GPU.

Команда для запуска на CPU:
```bash
docker run -d --name cat-dog-classification-service \
-e SERVICE_NAME="Cat-Dog classification service" \
-p 8080:8000 \
cat-dog-classification-service:cpu
```

Команда для запуска на GPU:
```bash
docker run -d --name cat-dog-classification-service \
--runtime=nvidia \
--gpus all \
-e SERVICE_NAME="Cat-Dog classification service" \
-p 8080:8000 \
cat-dog-classification-service:gpu
```

Переменную окружения <b>SERVICE_NAME</b> можно передать опционально.
После запуска контейнера можно перейти по ссылке http://SERVER_IP_OR_HOSTNAME:8080/docs и поизучать OpenAPI-документацию.

<b>P.S.</b> SERVER_IP_OR_HOSTNAME - ip-адрес или имя вашего сервера (для запуска локально - locahost).

### Остановка Docker-контейнера с сервисом
Тут одна команда для любого типа инференса:
```bash
docker stop cat-dog-classification-service
```

### Удаление Docker-контейнера с сервисом
Тут одна команда для любого типа инференса:
```bash
docker rm cat-dog-classification-service
```
