ALTER TABLE game_map ADD CONSTRAINT all_fields_unique UNIQUE (x, y, game_object_id)