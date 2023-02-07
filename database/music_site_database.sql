DROP TABLE IF EXISTS collection_track;
DROP TABLE IF EXISTS album_artist;
DROP TABLE IF EXISTS artist_genre;
DROP TABLE IF EXISTS track;
DROP TABLE IF EXISTS collection;
DROP TABLE IF EXISTS album;
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS genre;

CREATE TABLE IF NOT EXISTS collection (
	collection_id SERIAL PRIMARY KEY,
	collection_name TEXT NOT NULL,
	year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS album (
	album_id SERIAL PRIMARY KEY,
	album_name TEXT NOT NULL,
	year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS artist (
	artist_id SERIAL PRIMARY KEY,
	artist_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS genre (
	genre_id SERIAL PRIMARY KEY,
	genre_name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS track (
	track_id SERIAL PRIMARY KEY,
	track_name TEXT NOT NULL,
	album_id INT REFERENCES album,
	duration INT NOT NULL
);

CREATE TABLE IF NOT EXISTS collection_track (
	collection_id INT REFERENCES collection,
	track_id INT REFERENCES track,
	PRIMARY KEY (collection_id, track_id)
);

CREATE TABLE IF NOT EXISTS album_artist (
	album_id INT REFERENCES album,
	artist_id INT REFERENCES artist,
	PRIMARY KEY (album_id, artist_id)
);

CREATE TABLE IF NOT EXISTS artist_genre (
	artist_id INT REFERENCES artist,
	genre_id INT REFERENCES genre,
	PRIMARY KEY (artist_id, genre_id)
);

