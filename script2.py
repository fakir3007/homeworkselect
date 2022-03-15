from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://postgres:user@localhost:5432/homework5')

connection = engine.connect()

# количество исполнителей в каждом жанре;
count_performers = connection.execute('''
    SELECT T.title, count(GP.performer_id)
    FROM Genres T
    JOIN  Genre_performer GP ON T.id = GP.genre_id
    GROUP BY T.title
    ''').fetchall()

print(f'Количество исполнителей в каждом жанре: {count_performers}')

# количество треков, вошедших в альбомы 2019-2020 годов;
count_treck_19_20 = connection.execute('''
    SELECT a.title, a.year, count(s.id)
    FROM Albums a
    JOIN Songs s ON a.id = s.album_id
    WHERE a.year >= 2019 AND a.year <= 2020
    GROUP BY a.title, a.year
    ''').fetchall()

print(f'Количество треков, вошедших в альбомы 2019-2020 годов;: {count_treck_19_20}')

# средняя продолжительность треков по каждому альбому;
duration_track_average = connection.execute('''
    SELECT  a.title, round(AVG(s.duration), 2)
    FROM Albums a
    JOIN Songs s ON a.id = s.album_id
    GROUP BY a.title
    ''').fetchall()

print(f'Cредняя продолжительность треков по каждому альбому: {duration_track_average}')

# все исполнители, которые не выпустили альбомы в 2020 году;
performers_album_not_in_20 = connection.execute('''
    SELECT p.name, a.year
    FROM Performers p
    JOIN Album_performers ap ON p.id = ap.performer_id
    JOIN Albums a ON ap.album_id = a.id
    WHERE a.year != 2020
    ''').fetchall()

print(f'Все исполнители, которые не выпустили альбомы в 2020 году: {performers_album_not_in_20}')

# названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
Name_in_collection = connection.execute('''
    SELECT DISTINCT c.title
    FROM Collections c
    JOIN Song_collection sc ON c.id = sc.collection_id
    JOIN Songs s ON sc.song_id = s.id
    JOIN Albums a ON s.album_id = a.id
    JOIN Album_performers ap ON a.id = ap.album_id
    JOIN Performers p ON ap.performer_id = p.id
    WHERE p.name LIKE 'Nirvana'
    ''').fetchall()

print(f'Названия сборников, в которых присутствует конкретный исполнитель ("artist_5"): {Name_in_collection}')

# название альбомов, в которых присутствуют исполнители более 1 жанра;
album_many_styles = connection.execute('''
     SELECT a.title
     FROM Albums a
     JOIN Album_performers ap ON a.id = ap.album_id
     JOIN Performers p ON ap.performer_id = p.id
     JOIN Genre_performer gp ON p.id = gp.performer_id
     GROUP BY p.name, a.title
     HAVING count(gp.genre_id) > 1
    ''').fetchall()

print(f'Название альбомов, в которых присутствуют исполнители более 1 жанра: {album_many_styles}')

# наименование треков, которые не входят в сборники;
lonely_track = connection.execute('''
    SELECT s.title
    FROM Songs s
    LEFT JOIN Song_collection sc ON s.id = sc.song_id
    where sc.song_id IS NULL
    ''').fetchall()

print(f'Наименование треков, которые не входят в сборники: {lonely_track}')

# исполнителя(-ей), написавшего самый короткий по продолжительности трек
# (теоретически таких треков может быть несколько);
the_shortest_track = connection.execute('''
    SELECT p.name, s.duration
    FROM Performers p
    JOIN Album_performers ap ON p.id = ap.performer_id
    JOIN Albums a ON ap.album_id = a.id
    JOIN Songs s ON a.id = s.album_id
    WHERE s.duration IN (SELECT MIN(duration) FROM Songs)
    ''').fetchall()

print(f'Исполнителя(-ей), написавшего самый короткий по продолжительности трек : {the_shortest_track}')

# название альбомов, содержащих наименьшее количество треков.
the_shortest_album = connection.execute('''
    SELECT a.title, count(s.id)
    FROM Albums a
    JOIN Songs s  ON a.id = s.album_id
    GROUP BY a.title 
    HAVING count(s.id) in (
        SELECT count(s.id)
        FROM Albums a
        JOIN Songs s  ON a.id = s.album_id
        GROUP BY a.title
        ORDER BY count(s.id)\
        LIMIT 1)
    ''').fetchall()

print(f'Название альбомов, содержащих наименьшее количество треков : {the_shortest_album}')