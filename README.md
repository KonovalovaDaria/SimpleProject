requirements:
python 3.8
req.txt

dev requirements:
dev-req.txt

start projects:
python manage.py runserver 


# примеры запросов

1. созание автора
```commandline
curl -X PUT "127.0.0.1:8000/author/" -d '{"first_name": "first_name", "last_name": "last_name", "birthday": "2022-01-01"}'
```

2. обновление данных автора
```commandline
curl -X POST "127.0.0.1:8000/author/1/" -d '{"first_name": "first_name1", "last_name": "last_name4", "birthday": "2022-01-01"}'
```

3. получение данных автора
```commandline
curl -X GET "127.0.0.1:8000/author/1/"
```

4. удаление автора
```commandline
curl -X DELETE "127.0.0.1:8000/author/1/"
```
