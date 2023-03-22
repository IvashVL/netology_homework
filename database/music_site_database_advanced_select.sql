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

--Только обращаю внимание, что ваша реализация 4 запроса отвечает 
--на вопрос “кто выпустил хоть что-то, кроме того, что выпустил в 2020”, 
--а не на вопрос: “кто не выпустил альбомы в 2020 году”. Чтобы решить 
--поставленную задачу нужно сначала найти тех исполнителей, кто выпустил 
--альбом в 2020 (вложенным запросом), а потом их исключить из общего списка 
--исполнителей. Тут оптимальнее было вот так (названия полей и таблиц мои, 
--но суть не меняется):
--SELECT DISTINCT a.name FROM artist a 
--	WHERE a.name NOT IN (
--		SELECT DISTINCT a.name FROM artist a 
--		LEFT JOIN artist_album aa ON a.artist_id = aa.artist_id
--		LEFT JOIN album al ON al.album_id = aa.album_id 
--		WHERE al.year_of_issue = 2020
--		)
--	ORDER BY a.name;

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

--А в 6 запросе вложенная часть совсем не нужна, т.к. вы после всех объединений можете 
--сгруппировать результат по альбомам и сделать отбор при помощи HAVING:	 
--SELECT Album.Title FROM GenreArtist
--JOIN Genre ON GenreArtist.GenreId = Genre.Id
--JOIN Artist ON GenreArtist.ArtistId = Artist.Id
--JOIN ArtistAlbum ON ArtistAlbum.ArtistId = Artist.Id
--JOIN Album ON ArtistAlbum.AlbumId = Album.Id
--GROUP BY Album.Title
--HAVING COUNT(DISTINCT Genre.Name) > 1;

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

--И в последнем запросе можно было обойтись одним уровнем вложенности:															
--SELECT album.title, COUNT(track.title) track_count FROM album 
--JOIN track ON album.album_id = track.album_id
--GROUP BY album.album_id
--HAVING COUNT(track.title) = (  
--	SELECT COUNT(track.title) FROM album
--	JOIN track ON album.album_id = track.album_id
--	GROUP BY album.album_id
--	ORDER BY COUNT(track.title)
--	LIMIT 1);
