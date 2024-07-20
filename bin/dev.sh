function launch_map {
    cd map
    env $(grep -v '^#' ../.env | xargs) tegola serve --config tegola.toml
}

function launch_node {
    cd app
    env $(grep -v '^#' .env.local | xargs) npm run dev
}

function launch_django {
    cd web
    env $(grep -v '^#' ../.env | xargs) poetry run python manage.py runserver
}



(trap 'kill 0' SIGINT; launch_map & launch_node & launch_django)