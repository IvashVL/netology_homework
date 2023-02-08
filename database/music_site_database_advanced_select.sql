-- 1. количество исполнителей в каждом жанре;
SELECT genre_name, COUNT(artist_id) FROM genre
JOIN artist_genre ON genre.genre_id = artist_genre.genre_id
GROUP BY genre_name;																																																																																																																																																																																																																																																																																																																				

-- 2. количество треков, вошедших в альбомы 2019-2020 годов;
SELECT COUNT(*) FROM track
JOIN album ON track.album_id = album.album_id
WHERE year BETWEEN 2019 AND 2020;																																																																																																																																																																																																																																																																																																																			

-- 3. средняя продолжительность треков по каждому альбому;
SELECT album_name, ROUND(AVG(duration), 2) FROM track
JOIN album ON track.album_id = album.album_id
GROUP BY album_name;

-- 4. все исполнители, которые не выпустили альбомы в 2020 году;
SELECT DISTINCT artist_name FROM artist
JOIN album_artist ON album_artist.artist_id = artist.artist_id
JOIN album ON album.album_id = album_artist.album_id
WHERE year != 2020;

-- 5. названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
SELECT collection_name FROM collection
JOIN collection_track ON collection_track.collection_id = collection.collection_id
JOIN track ON track.track_id = collection_track.track_id
JOIN album ON album.album_id = track.album_id
JOIN album_artist ON album_artist.album_id = album.album_id
JOIN artist ON artist.artist_id = album_artist.artist_id
WHERE artist_name = 'Ten Years After';

-- 6. название альбомов, в которых присутствуют исполнители более 1 жанра;
SELECT DISTINCT album_name FROM album
JOIN album_artist ON album_artist.album_id = album.album_id
JOIN (SELECT artist_id FROM artist_genre
	  GROUP BY artist_id 
	  HAVING COUNT(*) > 1) AS genre_count ON genre_count.artist_id =  album_artist.artist_id;

-- 7. наименование треков, которые не входят в сборники;
SELECT track_name FROM track
WHERE track_id NOT IN (SELECT track_id FROM collection_track);


-- 8. исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически 
-- таких треков может быть несколько);
SELECT DISTINCT artist_name FROM artist
JOIN album_artist ON album_artist.artist_id = artist.artist_id
JOIN album ON album.album_id = album_artist.album_id
JOIN track ON track.album_id = album.album_id
WHERE duration = (SELECT MIN(duration) FROM track);

-- 9. название альбомов, содержащих наименьшее количество треков.
SELECT album_name FROM album
WHERE album_id IN (SELECT album_id FROM track
				   GROUP BY album_id 
				   HAVING COUNT(*) = (SELECT MIN(q.count) FROM (SELECT album_id, COUNT(*) FROM track 
																GROUP BY album_id) AS q));
