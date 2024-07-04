function launch_map {
    cd map && tegola serve --config tegola.toml
}

function launch_node {
    cd app && npm run dev
}

function launch_django {
    cd web && poetry run python manage.py runserver
}



(trap 'kill 0' SIGINT; launch_map & launch_node & launch_django)