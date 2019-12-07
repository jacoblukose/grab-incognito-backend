# grab-incognito-backend

py backend for grabathon

## Documentation link

TODO...

## SETUP

1. create a virtualenv using python3 <ul>
   `python3 -m venv .`
   </ul>

<ul>
2. git clone the repo 
</ul>

3. Install cutom root level module<ul>
   `pip install -e .`
   </ul>

4) Install python dependencies<ul>
   `pip install -r requirements.txt`
   </ul>

## RUN THE APP

FLASK_APP=\$PWD/http/api/endpoints.py FLASK_ENV=development flask run

## MONGO Mac SETUP

1. brew tap mongodb/brew
2. brew install mongodb-community@4.2
3. brew services start mongodb-community
4. Try mongo shell: mongo
