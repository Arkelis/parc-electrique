cd web
env $(grep -v '^#' ../.env | xargs) poetry run python manage.py shell