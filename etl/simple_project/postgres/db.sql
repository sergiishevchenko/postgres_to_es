CREATE SCHEMA IF NOT EXISTS public;

CREATE SCHEMA IF NOT EXISTS content;

ALTER ROLE app SET search_path TO content,public;

CREATE TYPE film_type AS ENUM ('movie', 'tv_show');

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    file_path TEXT,
    rating FLOAT,
    type film_type,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    genre_id uuid NOT NULL REFERENCES genre(id) ON DELETE CASCADE,
    created_at timestamp with time zone
);

CREATE TYPE role_type AS ENUM ('actor', 'writer', 'director');

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    person_id uuid NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    role role_type,
    created_at timestamp with time zone
);

CREATE UNIQUE INDEX film_work_person_role ON content.person_film_work (film_work_id, person_id, role);

CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work(film_work_id, genre_id);