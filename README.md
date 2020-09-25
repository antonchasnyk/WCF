# WCF
![Coverage](https://img.shields.io/badge/Coverage-68%25-yellow) 

## Django localizations
```shell script
python manage.py makemessages -l ru --ignore=venv/* --ignore=frontend/*
python manage.py compilemessages -l ru
```

## Run test coverage script 
```shell script
  coverage run --source='.' manage.py test
  coverage report  #for console output
  coverage html    #to create report
```