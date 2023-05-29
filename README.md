# SoftDesk

The application will allow users to have a tracking process for their projects.
Using a contributor system for each project, users will be able to create "issues" to track the nature, priority and status of those while adding "comments" to collaborate.

## Environment
### Installation
- clone the repository.  
`https://github.com/TroadecJb/P10---SoftDesk.git`
- Access repository.  
`$ cd /path/to/project`

### Virtual environment
- Python  
`$ python -m -venv <environment name>`
- windows activation  
`$ ~<environment name>\Scripts\activate.bat`
- macOs/linux  
`$ ~source <environment name>/bin/activate`
- install requirements  
`$ python -m pip install -r requirements.txt`
- to run it  
```
$ cd /path/to/project/SoftDesk
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

---
## Requirements
```
Django==4.2.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2
drf-nested-routers==0.93.4
```


---
## Documentation
To see the documentation click [here](https://documenter.getpostman.com/view/27468746/2s93m8yg3M)