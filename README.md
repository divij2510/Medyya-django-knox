
# Medyya Social Media Backend

Backend RESTful API for a social media app


## Requirements

To run this project, you will need to install the following python packages in your machine.

`asgiref` `--` `3.7.2`

`cffi` `--` `1.16.0`

`cryptography` `--` `42.0.5`

`Django` `--` `5.0.3`

`django-rest-knox` `--` `4.2.0`

`djangorestframework` `--` `3.14.0`

`pillow` `--` `10.2.0`

`pycparser` `--` `2.21`

`pytz` `--` `2024.1`

`sqlparse` `--` `0.4.4`

`tzdata` `--` `2024.1`


## Install and Run

Make sure to have python installed in your system, If required you can make a virtual environment for dependencies.

```bash
  git clone https://github.com/divij2510/Medyya-django-knox.git
```  
  After cloning, move into the directory having the project files using the change directory command
```bash
  cd Medyya-django-knox
```
  Create a virtual environment where all the required python packages will be installed
```
python -m venv env
```
  Activate the virtual environment
```
.\env\Scripts\activate
```
  Install all the project Requirements
```
pip install -r requirements.txt
```
  Apply migrations and create your superuser (follow the prompts)
```
python manage.py migrate
python manage.py createsuperuser
```
Run the development server!
```
python manage.py runserver
```
  
