import sqlite3

db = sqlite3.connect('test.db')

c = db.cursor()

#Создание таблицы
#c.execute("""CREATE TABLE articles (
#    title text,
#    full_text text,
#    views integer,
#    avtor text
#)

#Добавление данных
#c.execute("INSERT INTO articles VALUES ('sad', 'Faceddsabook pizdasadto', 330, 'pidodsar')")


#получение данных
c.execute("SELECT rowid, * FROM articles")

#удаление данных
#c.execute("DELETE FROM articles WHERE rowid = 1")

#изменение данных
#c.execute("UPDATE articles SET avtor = 'admin' WHERE title = 'Facebook'")
items = c.fetchall()
print(items)
db.commit()
db.close()