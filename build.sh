# @todo #/DEV During building process there is an error: 'grep: pyproject.toml: No such file or directory'
set -e
make install
make lint
make test
docker-compose up --build