from app.src.main import app
from app.src.db_create import init_db

if __name__ == "__main__":
    init_db()
    app.secret_key = "DeployProject?2024"
    app.run()