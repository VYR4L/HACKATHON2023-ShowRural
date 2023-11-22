import sqlalchemy as sa
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


ROOT_DIR = Path(__file__).parent
Base = declarative_base()
DB_NAME = "database.db"
DB_FILE = ROOT_DIR / DB_NAME

app = sa.create_engine(f'sqlite:///{DB_NAME}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=app)

db = SessionLocal()
if not DB_FILE.exists():
    with app.app_context():
        sa.create_all()
        print('#################')
        print('Created Database!')
        print('#################')
        Base.metadata.create_all(app)


class Employee(Base):
    __tablename__ = 'employees'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    rg = sa.Column(sa.String(255), unique=True, nullable=False)
    image_name = sa.Column(sa.String(255), nullable=False)
    
    def __init__(self, image_path):
        self.image_name = image_path


class Visitor(Base):
    __tablename__ = 'visitors'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    rg = sa.Column(sa.String(255), unique=True, nullable=False)
    image_name = sa.Column(sa.String(255), nullable=False)

    def __init__(self, image_path):
        self.image_name = image_path


class Clock_in(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.String(8), nullable=False)
    name = sa.Column(sa.String(255), nullable=False)
    rg = sa.Column(sa.String(255), unique=True, nullable=False)
    date =  sa.Column(sa.String(255), nullable=False)
    