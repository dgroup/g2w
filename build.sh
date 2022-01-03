# @todo #/DEV During building process there is an error: 'grep: pyproject.toml: No such file or directory'
make install
make lint
make test
docker build -t dgroup/g2w:latest . -f Containerfile