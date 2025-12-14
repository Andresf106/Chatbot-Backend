from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0903@localhost:5432/Database_Proyect_SI"

# Crear motor de SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependencia para rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
