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

Здесь создаем и запускаем докер-контейнер.
```
$ docker run -d -p 8180:8180 -p 8181:8181 -v dimonoy/ml-api
```


### Проверить работоспособность можно через Postman

Создаем POST запрос с url http://127.0.0.1:8180/predict.  
Во вкладке Authorization выбираем Type: No Auth.  
Во вкладке Body выбираем raw с типом JSON и вставляем следующее:
```
{
    "description": "As a Web Engineer at Runscope you'll be responsible for building a world-class, high-performance web application used by our customers every day. We win or lose customers based on their interaction with the web app so it's your responsibility to make sure it's a delightful and reliable experience.We're building tools we use ourselves every day, and we have high standards. You should too. We're a small team so everyone is a product manager. You will need to be able to prioritize what's important to build and understand our customers' needs at a very deep level. The tools you build will directly impact other developers so having a strong product vision is important for this role.This is a role for an experienced engineer looking to have significant influence over the direction of a product.",
    "company_profile": "Runscope is building tools for developers working on API-driven mobile and web applications. We have a clear vision for the future of service-powered companies and the tools that will be required to build the next generation of applications. We're an experienced team backed by top-tier investors looking for people who share our passion for building great tools and want to help shape not just our products, but the company as well. Proven Work/Life BalanceA lot of companies talk about work/life balance, but we've to the data to prove how important to us it is. We've posted a breakdown of over 10,000 commits over the first year of the company showing when we work. See the stats.",
    "benefits": "Be a part of an experienced team who have worked on some of the most popular web sites and developer tools.Competitive salary and meaningful equity. Medical, dental and vision insurance. Flexible working schedule and real work/life balance. Unlimited vacation and personal time. Casual work environment.Spec your own equipment — tell us what you need and it will be ready to go when you walk in on your first day. Spacious office space in the heart of San Francisco's SOMA neighborhood a short walk from BART or Caltrain. Relocation assistance. We laugh, a lot."
}
```
