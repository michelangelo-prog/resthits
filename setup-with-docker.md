## Getting Started

Update the environment variables, and then build the images and spin up the containers:

```sh
docker-compose up -d --build
```

## Commands description

### Run tests

```sh
docker-compose run resthits python manage.py test-pytest-with-plugins
```