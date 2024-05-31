CREATE SCHEMA IF NOT EXISTS "content" AUTHORIZATION app;

GRANT USAGE ON SCHEMA content TO app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA content TO app;

ALTER DEFAULT PRIVILEGES IN SCHEMA content
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app;

ALTER ROLE app SET search_path TO content, public;

CREATE TABLE IF NOT EXISTS "content".film_work (
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	id uuid NOT NULL,
	title varchar(255) NOT NULL,
	description text NULL,
	creation_date date NULL,
	rating float8 NULL,
	"type" varchar(255) NOT NULL,
	file_path varchar(100) NULL,
	CONSTRAINT film_work_pk PRIMARY KEY (id)
);
CREATE INDEX idx_film_work_updated_at ON content.film_work USING btree (updated_at);

CREATE TABLE IF NOT EXISTS "content".genre (
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	id uuid NOT NULL,
	"name" varchar(255) NOT NULL,
	description text NULL,
	CONSTRAINT genre_pk PRIMARY KEY (id)
);
CREATE INDEX idx_genre_updated_at ON content.genre USING btree (updated_at);

CREATE TABLE IF NOT EXISTS "content".person (
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	id uuid NOT NULL,
	full_name varchar(255) NOT NULL,
	CONSTRAINT person_pk PRIMARY KEY (id)
);
CREATE INDEX idx_person_updated_at ON content.person USING btree (updated_at);


CREATE TABLE IF NOT EXISTS "content".genre_film_work (
	id uuid NOT NULL,
	created_at timestamptz NOT NULL,
	film_work_id uuid NOT NULL,
	genre_id uuid NOT NULL,
	CONSTRAINT fk_content_film_work_to_content_genre_film_work FOREIGN KEY (film_work_id) REFERENCES "content".film_work(id),
	CONSTRAINT fk_content_genre_to_content_genre_film_work FOREIGN KEY (genre_id) REFERENCES "content".genre(id)
);
CREATE INDEX idx_genre_film_work_film_work_id ON content.genre_film_work USING btree (film_work_id);
CREATE INDEX idx_genre_film_work_genre_id ON content.genre_film_work USING btree (genre_id);


CREATE TABLE IF NOT EXISTS "content".person_film_work (
	id uuid NOT NULL,
	"role" text NULL,
	created_at timestamptz NOT NULL,
	film_work_id uuid NOT NULL,
	person_id uuid NOT NULL,
	CONSTRAINT fk_content_film_work_to_content_person_film_work FOREIGN KEY (film_work_id) REFERENCES "content".film_work(id),
	CONSTRAINT fk_content_person_to_content_person_film_work FOREIGN KEY (person_id) REFERENCES "content".person(id)
);
CREATE INDEX idx_person_film_work_film_work_id ON content.person_film_work USING btree (film_work_id);
CREATE INDEX idx_person_film_work_person_id ON content.person_film_work USING btree (person_id);
