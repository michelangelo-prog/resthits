## Getting Started

Update the environment variables, and then build the images and spin up the containers:

```sh
docker-compose up -d --build
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

## Commands description

### Run tests

```sh
docker-compose run resthits python manage.py test-pytest
```

### Run tests with black, isort and flakes

```sh
docker-compose run resthits python manage.py test-pytest-with-plugins
```

### Create sample data

```sh
docker-compose run resthits python manage.py create-sample-data
```