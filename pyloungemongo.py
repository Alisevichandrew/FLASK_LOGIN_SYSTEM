import pymongo

# устанавливаем соединение с MongoDB
# MongoDB должна быть запущена на компьютере, 27017 - стандартный порт
db_client = pymongo.MongoClient("mongodb://localhost:27017/")  # MongoClient('localhost', 27017)

# подключаемся к БД pyloungedb, если её нет, то будет создана
current_db = db_client["pyloungedb"]  # dictionary style
# current_db = db_client.pyloungedb - attribute style

# получаем колекцию из нашей БД, если её нет, то будет создана
# Коллекция - это группа документов, которая хранится в БД MongoDB (эквалент таблицы в ркляционных базах)
collection = current_db["youtubers"]  # current_db.youtubers

# Коллекции и базы данных в MongoDB created lazily - фактически создаются при вставке в них первого документа
# Данные в MongoDB представляются с помощью JSON-style документов
# можно явно указать желаемый айди, добавив ключ - '_id': n
pylounge = {
  'title': 'PyLounge',
  'url': 'https://www.youtube.com/channel/UCru5FZQN_Xa0tKfrBqUIcng',
  'subscribers': 2100,
  'views': 90000
}

ins_result = collection.insert_one(pylounge)  # добавляет одну запись в коллекцию collection
print(ins_result.inserted_id)  # id вставленного объекта

it_youtubers = [
    {'title': 'АйТиБорода','url': 'www.youtube.com/c/ITBEARD/', 'subscribers': 227000, 'views': 1200024},
    {'title': 'Диджитализируй!', 'url': 'www.youtube.com/channel/UC9MK8SybZcrHR3CUV4NMy2g/', 'subscribers': 62700, 'views': 960245},
    {'title': 'Senior Software Vlogger', 'url': 'www.youtube.com/user/rojkovdima', 'subscribers': 90700, 'views': 2000000}
]

ins_result = collection.insert_many(it_youtubers)  # добавляет несколько записей в коллекцию collection
print(ins_result.inserted_ids)

# Запрос найти первый документ у которого количество подписчиков = subs
subs = 2100
print(collection.find_one({'subscribers': subs}))  # {} - критерии запроса
print(collection.count_documents({'subscribers': subs}))  # количество документов в коллекции у которых subs подписчиков

# вывести все документы в коллекции
for channel in collection.find():
    print(channel)

# Сложные запросы
# https://docs.mongodb.com/manual/reference/operator/
print('Количество документов у которых подписчиков > 10 000')
print(collection.count_documents({"subscribers": {"$gt": 10000}})) #где '$gt' - это оператор больше, т.е. подписчиков больше '10000'
print('Количество документов у которых подписчиков < 10 000')
print(collection.count_documents({"subscribers": {"$lt": 10000}})) # где "$lt" - это оператор, который указывает меньше, т.е. по ключу "subscribers" выдает к-во подписчиков меньше 10000

# https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline/
print('Все ютуберы к которых > 10 000 подписчиков, отсортированные по полю title')
for channel in collection.find({'subscribers': {'$gt': 10000}}).sort('title'):  # sort('title', -1) # где '-1' указывает, что сортировка будет в обратном порядке, т.е. по убыванию
    print(channel)

# { <operator>: [ <argument1>, <argument2> ... ] }, <argument1> - {'':''}
print('Все имена ютуберов у которых > 10 000 подписчиков И просмотров больше 1 000 000')
for channel in collection.find({'$and': [{'subscribers': {'$gt': 10000}}, {'views': {'$gt': 1000000}}]}): # где '$and' - объединяет запросы 'Логическим' и возвращает все документы, которвые соответствуют обоим условиям 
    print(channel['title'])

print('каналы, название которых соответствует регулярному выражению ^Py(.*?)')
for channel in collection.find({'title': {'$regex': '^Py(.*?)'}}).limit(2):  # groupby (группировать), orderby (упорядочивать записи), skip ("скипать" пропускать записи) и т.д. '$regex' - это регулярное выражение, а 'limit', лимитирует к-во документов, которые будут выведены (в данном случае, мы выведем только две записи)
    print(channel['title'], ' ', channel['subscribers'])

# переменная с запросом: просмотров от 0 до 100 000
query = {'views': {'$in': list(range(0, 100000))}}  # '$in' -выбирает, где значения поля находятся в массиве (в данном случае от '0' до '100000')
for channel in collection.find(query): # обращаемся к коллекции и отправляем переменную с нашим запросом
    print(channel['title'], ' ', channel['subscribers'], channel['views'])

# обновление документов
collection.update_one({'title': 'PyLounge'}, {'$set': {'subscribers': 1000024}}) # в данном случае мы ,берем документы, в названии которых есть 'PyLounge' и устанавливаем командой '$set' полю 'subscribers': значение 1000024
print(collection.find_one({'title': 'PyLounge'}))
# есть ещё find_one_and_delete, find_one_and_replace и т.д. (для этого нужно смотреть документацию к проекту на mongoDB)
print('Find and update')
print(collection.find_one_and_update({'title': 'PyLounge'}, {'$set': {'subscribers': 1000024}}))

collection.update_many({'subscribers': {'$gt': 100000}}, {'$set': {'views': 3000000}})
print('После всех обновлений. Каналы с более 100 000 подписчиков')
for channel in collection.find({'subscribers': {'$gt': 100000}}):
    print(channel)

# удаление
collection.delete_one({'title': {'$regex': '^Senior'}}) # delete_many, find_one_and_delete. Хотим удалить одного пользователя, у которого 'title', ипользуя регулярное выражение '$regex': есть '^Senior'
print('После удаления:')
for channel in collection.find():
    print(channel)

# создание индексов (индекся нужны для ускорения работы базы, в частности, для ускорения поиска)
collection.create_index('title')  # , unique=True (делает индекс уникальным). В данном случае index стоит на 'title', поскольку довольно часто мы отбираем по названию
 
# удаление коллекции
collection.drop()
# удаление бд
db_client.drop_database('pyloungedb')