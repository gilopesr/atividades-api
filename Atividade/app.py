from config import create_app
from controllers.atividade_controller import atividade_bp

app = create_app()
app.register_blueprint(atividade_bp, url_prefix='/atividades')

if __name__ == '__main__':
    app.run(host='localhost', port=5003)