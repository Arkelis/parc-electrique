echo "Building frontend app"

cd app
env $(grep -v '^#' .env.production | xargs) npx vite build

echo
echo "Preparing static files for web server"

cd ../web
rm -r static
poetry run python manage.py collectstatic

echo "Done!"