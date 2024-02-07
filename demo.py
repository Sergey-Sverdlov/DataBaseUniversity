import psycopg2
import random
import string
connection = psycopg2.connect(user="admin",
                              password="12345",
                              host="localhost",
                              port="5432",
                              database="postgres")
cursor = connection.cursor()

import time
# start_time = time.time()

# for i in range(10000):
#     cursor.execute("Select * from university where year_construction = 1820")
#
# print("--- %s seconds ---" % (time.time() - start_time))
# connection.commit()
# cursor.close()
# connection.close()
# print("Подключение выполнено успешно")
start_time = time.time()
id = 30004
for i in range(20000):
    id += 1
    name = "Ivan"
    age = random.randint(15, 25)
    school = random.randint(1515,2910)
    cursor.execute("INSERT INTO test_index VALUES(%s, %s, %s, %s)", (id, name, age, school))
    connection.commit()
cursor.close()
print("--- %s seconds ---" % (time.time() - start_time))
# id_university = 29
# letters = string.ascii_lowercase
# for i in range(1000):
#     name_university = ''.join(random.choice(letters) for i in range(15))
#     year_construction = random.randint(1830, 1870)
#     year_repair = random.randint(1940, 2018)
#     count_student = random.randint(15000, 17000)
#     min_cost = random.randint(100000, 500000)
#     intro_university = ''.join(random.choice(letters) for i in range(20))
#     about_university = ''.join(random.choice(letters) for i in range(200))
#
#     count_male = random.randint(8000, 11000)
#     count_female = count_student - count_male
#
#     position_raex = random.randint(100, 1000)
#     position_qs = position_raex + 50
#     position_the = position_raex - 80
#
#     cursor.execute("INSERT INTO university VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (id_university, name_university, year_construction, year_repair, count_student, min_cost, intro_university, about_university))
#     cursor.execute("INSERT INTO male_female VALUES(%s, %s, %s)", (id_university, count_male, count_female))
#     cursor.execute("INSERT INTO rank_university  VALUES(%s, %s, %s, %s)", (id_university, position_raex, position_qs, position_the))
#     id_university += 1
# start_time = time.time()

