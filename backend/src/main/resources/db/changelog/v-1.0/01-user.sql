CREATE TABLE IF NOT EXISTS users (
     user_id BIGSERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     allergies TEXT NOT NULL DEFAULT '',
     restrictions TEXT NOT NULL DEFAULT '',
     cousines TEXT NOT NULL DEFAULT ''
);