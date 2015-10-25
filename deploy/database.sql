-- Database scheme

CREATE TABLE game_object(
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(50),
  description TEXT
);


CREATE TABLE game_map(
 x INTEGER,
 y INTEGER,
 game_object_id VARCHAR(64) REFERENCES game_object(id),
 UNIQUE (x, y, game_object_id)
)