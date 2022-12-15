# BookLibrary

Simulation project of a bookstore.

## Dependencies

- Python >= 3.8.12

## Usage

- Rename `env.template` file to `.env` and edit using correct values according to environment

## Install System requires
```
pip install -r requirements/dev.txt`
```


## Run migrations and load data
```
python manage.py migrate
python manage.py loaddata users.json
python manage.py loaddata customers.json
python manage.py loaddata authors.json
python manage.py loaddata books.json
```

## Run Test
```
python manage.py test
```

## URL API
```
/api/v1/docs
```



