# EXECUTAR SOMENTE NO GIT BASH OU TERMINAL DO LINUX

export FLASK_APP=app
export FLASK_ENV=development
flask db migrate
flask db upgrade
flask run