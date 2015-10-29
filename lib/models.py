import sqlalchemy as sa


DB_CREDENTIALS = {
    'user': 'postgres',
    'database': 'game_db',
    'host': '127.0.0.1',
    'password': '1111'}

GameObject = sa.Table('game_object', sa.MetaData(),
                      sa.Column('id', sa.VARCHAR(64), primary_key=True),
                      sa.Column('name', sa.VARCHAR(50)),
                      sa.Column('description', sa.TEXT)
                      )

GameMap = sa.Table('game_map', sa.MetaData(),
                   sa.Column('x', sa.INTEGER),
                   sa.Column('y', sa.INTEGER),
                   sa.Column('game_object_id', sa.VARCHAR(64),
                             sa.ForeignKey("game_object.id")),
                   sa.UniqueConstraint('x', 'y', 'game_object_id',
                                       name='all_fields_unique')
                   )


