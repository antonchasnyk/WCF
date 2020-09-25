# WCF
![Coverage](https://img.shields.io/badge/Coverage-80%25-yellowgreen) 

<!--  
    brightgreen     100%
    green           90%
    yellowgreen     80%
    yellow          70%
    orange          60%
    red             50%
 -->

## Django localizations
```shell script
python manage.py makemessages -l ru --ignore=venv/* --ignore=frontend/*
python manage.py compilemessages -l ru --ignore=venv/* --ignore=frontend/*
```

## Run test coverage script 
```shell script
  coverage run --source='.' manage.py test
  coverage report  #for console output
  coverage html    #to create report
```