import os

def setup_database(app):
    host = os.environ.get("DB_HOST", "localhost")  #os.environment.get(<NOME_VAR>, <VALOR_DEFAULT_SE_VAR_NAO_EXISTE>)
    port = os.environ.get("DB_PORT", "5432")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "root")
    db_name = os.environ.get("DB_NAME", "agenda")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
