-- Удаляем все записи из таблиц и сбрасываем id.
-- Это нужно для того чтоб первичные ключи не "съезжали" после повторного запуска запросов
-- Или же id можно прописывать явно

DELETE FROM album_artist;
DELETE FROM artist_genre;
DELETE FROM collection_track;
DELETE FROM artist;
ALTER SEQUENCE artist_artist_id_seq RESTART WITH 1;
DELETE FROM genre;
ALTER SEQUENCE genre_genre_id_seq RESTART WITH 1;
DELETE FROM track;
ALTER SEQUENCE track_track_id_seq RESTART WITH 1;
DELETE FROM album;
ALTER SEQUENCE album_album_id_seq RESTART WITH 1;
DELETE FROM collection;
ALTER SEQUENCE collection_collection_id_seq RESTART WITH 1;


INSERT INTO artist (artist_name)
VALUES('Ten Years After'),
	('Imelda May'),
	('Golden Earring'),
	('Beth Hart'),
	('Heart'),
	('King Harvest'),
	('The Cat Empire'),
	('Twisted Sister'),
	('The Pretty Reckles');
	
INSERT INTO genre (genre_name)
VALUES('Classic Rock'),
	('Rock & Roll'),
	('Hard Rock'),
	('Blues Rock'),
	('Blues'),
	('Pop Rock'),
	('Ska'),
	('Alternative Rock');

INSERT INTO album (album_name, year)
VALUES('Space In Time', 1971),
	('Mayhem', 2020),
	('Paradise In Distress', 1999),
	('37 Days', 2007),
	('Dreamboat Annie', 1976),
	('Dancing in the Moonlight', 1970),
	('Two Shoes', 2005),
	('Stay Hungry', 1984),
	('Light Me Up', 2018);
	
INSERT INTO track (track_name, album_id, duration)
VALUES('I''d Love To Change The World', 1, 224),
	('All For You', 2, 171),
	('Desperately Trying To Be Different', 3, 244),
	('One Night Without You', 3, 272),
	('Bad News to Fall in Love', 3, 308),
	('Heaven Look Down', 4, 199),
	('Crazy On You', 5, 256),
	('Dancing in the Moonlight', 6, 178),
	('Two Shoes', 7, 317),
	('The Price', 8, 230),
	('Make Me Wanna Die', 9, 236),
	('Just Tonight', 9, 168),
	('My Medicine', 9, 194),
	('Zombie', 9, 190),
	('Far From Never', 9, 217);

INSERT INTO collection (collection_name, year)
VALUES('Retro Songs', 2010),
	('Modern Songs', 2020),
	('Songs From Movie', 2012),
	('Best Collection Vol.1', 2018),
	('Female Voice', 2019),
	('Male Voice', 2015),
	('Best Collection Vol.2', 2016),
	('Best Collection Vol.3', 2021);

INSERT INTO collection_track (collection_id, track_id)
VALUES(1, 1),
	(1, 7),
	(1, 8),
	(1, 10),
	(2, 2),
	(2, 3),
	(2, 4),
	(2, 5),
	(2, 6),
	(2, 9),
	(2, 11),
	(2, 12),
	(2, 13),
	(2, 15),
	(3, 1),
	(3, 7),
	(3, 8),
	(4, 1),
	(4, 2),
	(4, 3),
	(4, 15),
	(5, 2),
	(5, 6),
	(5, 7),
	(5, 11),
	(5, 12),
	(5, 13),
	(5, 15),
	(6, 1),
	(6, 3),
	(6, 4),
	(6, 5),
	(6, 8),
	(6, 9),
	(6, 10),
	(7, 4),
	(7, 5),
	(7, 6),
	(7, 7),
	(7, 8),
	(8, 9),
	(8, 10),
	(8, 11),
	(8, 12),
	(8, 13);

INSERT INTO album_artist (album_id, artist_id)
VALUES(1, 1),
	(2, 2),
	(3, 3),
	(4, 4),
	(5, 5),
	(6, 6),
	(7, 7),
	(8, 8),
	(9, 9);
	
INSERT INTO artist_genre (artist_id, genre_id)
VALUES(1, 1),
	(2, 2),
	(3, 1),
	(4, 4),
	(5, 5),
	(6, 6),
	(7, 7),
	(8, 1),
	(9, 3),
	(9, 8);