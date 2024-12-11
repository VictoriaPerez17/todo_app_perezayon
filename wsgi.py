from app.src.main import app
from app.src.db_create import init_db

init_db()
app.secret_key = "DeployProject?2024"
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == "__main__":
    app.run()