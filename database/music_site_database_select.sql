-- 1. название и год выхода альбомов, вышедших в 2018 году; 
SELECT album_name, year FROM album
WHERE year = 2018;

-- 2. название и продолжительность самого длительного трека; 
-- Первый вариант
SELECT track_name, duration FROM track
ORDER BY duration desc
LIMIT 1;
-- Второй вариант
SELECT track_name, duration FROM track
WHERE duration = (SELECT MAX(duration) FROM track);

-- 3. название треков, продолжительность которых не менее 3,5 минуты;
SELECT track_name, duration FROM track
WHERE duration >= 3.5 *60
ORDER BY duration;

-- 4. названия сборников, вышедших в период с 2018 по 2020 год включительно;
SELECT collection_name, year FROM collection
WHERE year BETWEEN 2018 AND 2020
ORDER BY year;

-- 5. исполнители, чье имя состоит из 1 слова;
SELECT artist_name FROM artist
WHERE artist_name NOT LIKE '% %'
ORDER BY artist_name;

-- 6. название треков, которые содержат слово "мой"/"my".
SELECT track_name FROM track
WHERE track_name ~* '\m(my|мой)\M'
ORDER BY track_name;
