# Итоговый проект курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy
API: flask
Данные: https://www.kaggle.com/shivamb/real-or-fake-fake-jobposting-prediction

Задача: предсказать по описанию вакансии является ли она фейком или нет.

Используемые признаки:

- description (string)
- company_profile (string)
- benefits (string)

Преобразования признаков: TF-IDF

Модель: LogisticRegression

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/dimonoy/ml-api.git
$ cd ml-api
$ docker build -t dimonoy/ml-api .
```

### Запускаем контейнер

Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)
```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/models dimonoy/ml-api
```

### Переходим на localhost:8181
