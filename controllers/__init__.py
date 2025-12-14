# Puede quedar vacío
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔹 Cambia esta URL por tu conexión real a PostgreSQL
# Ejemplo: postgresql://usuario:contraseña@localhost:5432/tu_basedatos
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:tu_contraseña@localhost:5432/tu_base"

# 🔹 Crea el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 🔹 Crea una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Crea la clase base para los modelos
Base = declarative_base()
