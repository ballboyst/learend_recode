from sqlalchemy import crate_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql + pymysql"://mysql:mysql@todo_db:3306/todo_db
engine = crate_engine(SQLALCHEMY_DATABASE_URL)
db_session = sessionmaker(autocommit=False, autoflash=False, bind=engine)


def get_db()
    db = db.session()
    try:
        yield db
    finally:
        db.close()
