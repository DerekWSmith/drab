Migrate in this order:
python manage.py makemigrations core
python manage.py makemigrations accounts
python manage.py migrate core
python manage.py migrate accounts
