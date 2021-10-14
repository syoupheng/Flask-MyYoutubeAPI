# Flask-MyYoutubeAPI

## I) Introduction

For this project I designed an API for a video platform (like Youtube).Through different requests you will be able to handle users, authenticate them, to post videos and comments...etc

## II) Creating a virtual environnement

Once you have cloned this project on your machine you will need to create a virtual environnement (venv). A venv allows you to install dependencies only for this project without affecting other projects that might use other versions of the same dependencies. To create a venv and activate it, you will need to cd into the root of the project and type:

`python3 -m venv venv`\
`source venv/bin/activate`

You should now see "venv" written in the prompt of your terminal meaning that you have successfully activated your venv. You can now install all the required packages by using:

`python3 -m pip install -r requirements.txt`

## III) Database configuration

We have provided a dump of the database *database.sql* (located at the root of the project) that you can import by typing in your MySQL CLI:

`source database.sql`

Now that your database is ready you will have to create a file called *db_config.py* at the root of the project. In this file you will need to type this and enter your database connection informations:

`db_conf = {\
    "username":"",\
    "password":"",\
    "host":"",\
    "db_name":""\
}`

## IV) Starting and using the API

At this point you should be able to start the server by executing the *api.py* file:

`python3 api.py`

Your terminal should now display this message:

`Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

This means that you can access the API with the base URI *http://localhost:5000/myAPI*. So if you want to create a user from the */user* endpoint for example you will have to type *http://localhost:5000/myAPI/user* with a POST method (Postman can be used for that).

As a large number of endpoints can be accessed through this API you will find below a summary of these endpoints:

### 1) Creating users

Method : POST\
URI : */user*\
Authentication : not required\
Parameters :

`{
	"username*": string([a-zA-Z0-9_-]),
	"pseudo": string,
	"email*": string(email),
	"password*": string // 8 characters minimum
}`

These parameters need to be entered in the body of the request in JSON format.

Response code : 201
Response data example:

`{
    "message": "Ok",
    "data": {
        "created_at": "2021-10-14T15:01:12",
        "id": 13,
        "pseudo": "tes12",
        "username": "test12",
        "email": "test12@gmail.com"
    }
}`


