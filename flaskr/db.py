# import sqlite3
# import click
# from flask import current_app, g

# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(current_app.config['DATABASE'],detect_types=sqlite3.PARSE_DECLTYPES)
#         g.db.row_factory = sqlite3.Row

#         return g.db

# def close_db(e=None):
#     db = g.pop('db',None)

#     if db is not None:
#         db.close()

# def init_db():
#     db = get_db()

#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))


# @click.command('init-db')
# def init_db_command():
#    #limpa os dados existentes cria novas tabelas no banco
#     init_db()
#     click.echo('Initialized the database.')

# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///instance/fraskr.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db(app):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from . import models
    # Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(engine)