import sqlalchemy
import psycopg2
from pprint import pprint

engine = sqlalchemy.create_engine('postgresql://postgres:user@localhost:5432/netology2022')
pprint(engine)

connection = engine.connect()
print(connection)
pprint(engine.table_names())

#1.�������� � ��� ������ ��������, �������� � 2018 ����
select_1 = connection.execute('''SELECT  name, releasedate FROM albums
WHERE releasedate BETWEEN '2018-01-01' AND '2018-12-31';
''').fetchall()
pprint(select_1)

#2.�������� � ����������������� ������ ����������� �����
select_2 = connection.execute('''SELECT   name, tracklength FROM tracks
ORDER BY tracklength DESC;
''').fetchone()
pprint(select_2)

#3.�������� ������, ����������������� ������� �� ����� 3,5 ������
select_3 = connection.execute('''SELECT  name FROM tracks
WHERE tracklength >= 03.50;
''').fetchall()
pprint(select_3)

#4.�������� ���������, �������� � ������ � 2018 �� 2020 ��� ������������
select_4 = connection.execute('''SELECT name FROM compilation
WHERE release_year BETWEEN '2018-01-01' AND '2020-12-31';
''').fetchall()
pprint(select_4)

#5.�����������, ��� ��� ������� �� 1 �����
select_5 = connection.execute('''SELECT name FROM perfomers
WHERE name NOT LIKE '%% %%';
''').fetchall()
pprint(select_5)

#6.�������� ������, ������� �������� ����� "���"/"my"
select_6 = connection.execute('''SELECT name FROM tracks
WHERE name LIKE '%%my%%';
''').fetchall()
pprint(select_6)