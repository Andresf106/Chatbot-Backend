# app.py
from flask import Flask
from database.database import init_db, db
from controllers.usuario_controller import usuario_bp
from controllers.cita_controller import cita_bp
from controllers.medicamento_controller import medicamento_bp

app = Flask(__name__)

# Inicializar base de datos
init_db(app)

# Registrar los blueprints
app.register_blueprint(usuario_bp, url_prefix="/usuarios")
app.register_blueprint(cita_bp, url_prefix="/citas")
app.register_blueprint(medicamento_bp, url_prefix="/medicamentos")

if __name__ == "__main__":
    app.run(debug=True)
