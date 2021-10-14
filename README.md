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

```json
db_conf = {
    "username":"",
    "password":"",
    "host":"",
    "db_name":""
}
```

## IV) Starting and using the API

At this point you should be able to start the server by executing the *api.py* file:

`python3 api.py`

Your terminal should now display this message:

`Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

This means that you can access the API with the base URI *http://localhost:5000/myAPI*. So if you want to create a user from the */user* endpoint for example you will have to type *http://localhost:5000/myAPI/user* with a POST method (Postman can be used for that).

As a large number of endpoints can be accessed through this API you will find below a summary of these endpoints:

### 1) Creating users

Method : **POST**\
URI : */user*\
Authentication : *not required*\
Parameters :

```yaml
{
	"username*": string([a-zA-Z0-9_-]),
	"pseudo": string,
	"email*": string(email),
	"password*": string // 8 characters minimum
}
```

These parameters need to be entered in the body of the request in JSON format. Mandatory parameters are signaled with a "*".

Response code : **201**\
Response data example:

```json
{
    "message": "Ok",
    "data": {
        "created_at": "2021-10-14T15:01:12",
        "id": 13,
        "pseudo": "tes12",
        "username": "test12",
        "email": "test12@gmail.com"
    }
}
```

### 2) Authenticating users

Method : **POST**\
URI : */auth*\
Authentication : *not required*\
Parameters :

```json
{
	"login*": string,
	"password*": string
}
```

These parameters need to be entered in the body of the request in JSON format. Mandatory parameters are signaled with a "*".

Response code : **201**\
Response data example:

```json
{
    "message": "Ok",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidGVzdDgiLCJleHAiOjE2MzQyMTI2NTh9.MEQi3LWowrrqWIM35Yzqu0_fyrH7eHXtfqgnrHsHj-k",
        "user": {
            "pseudo": "test8",
            "id": 7,
            "created_at": "2021-10-12T17:00:46",
            "email": "test8@gmail.com",
            "username": "test8"
        }
    }
}
```

In order to authenticate for requests that require you ti be authentified you need to enter the token you obtained from the */auth* endpoint in the 'Authorization' headers.

### 3) Deleting users

Method : **DELETE**\
URI : */user/:id*\
Authentication : *required*\
Parameters : *no parameters*

Response code : **204**\
Response data example: `{}`

### 4) Updating users

Method : **PUT**\
URI : */user/:id*\
Authentication : *required*\
Parameters :

```json
{
	"username": string([a-zA-Z0-9_-]),
	"pseudo": string,
	"email": string(email),
	"password": string
}
```

These parameters need to be entered in the body of the request in JSON format. Mandatory parameters are signaled with a "*".

Response code : **200**\
Response data example:

```json
{
    "message": "Ok",
    "data": {
        "created_at": "2021-10-07T23:54:42",
        "id": 2,
        "pseudo": "test4",
        "username": "test4",
        "email": "test4@gmail.com"
    }
}
```

### 5) User list

Method : **GET**\
URI : */users*\
Authentication : *not required*\
Parameters :

```json
{
	"pseudo": string,
	"page": int,
	"perPage": int
}
```

These parameters are all optional and need to be entered as query parameters in the URI.

Response code : **200**\
Response data example:

```json
{
    "message": "Ok",
    "data": [
        {
            "created_at": "2021-10-12T17:01:01",
            "id": 8,
            "pseudo": "test9",
            "username": "test9",
            "email": "test9@gmail.com"
        },
        {
            "created_at": "2021-10-12T17:00:46",
            "id": 7,
            "pseudo": "test8",
            "username": "test8",
            "email": "test8@gmail.com"
        },
        {
            "created_at": "2021-10-12T17:00:32",
            "id": 6,
            "pseudo": "test7",
            "username": "test7",
            "email": "test7@gmail.com"
        }
    ],
    "pager": {
        "current": 2,
        "total": 3
    }
}
```

### 6) User by id

Method : **GET**\
URI : */user/:id*\
Authentication : *not required but if you provide a token you will be able to visualize your email adress.*\
Parameters : *no parameters*

Response code : **200**\
Response data example:

```json
{
    "message": "Ok",
    "data": {
        "username": "test7",
        "pseudo": "test7",
        "created_at": "2021-10-12T17:00:32",
        "id": 6
    }
}
```

### 7) Posting a video

Method : **POST**\
URI : */user/:id/video*\
Authentication : *required*\
Parameters :

```json
{
	"name": string,
	"source": file
}
```
These parameters need to be entered as form data.

Response code : **201**\
Response data example:

```json
{
    "message": "Ok",
    "data": {
        "source": "/home/syoupheng/PythonProjects/ETNA_myAPI/public/209f57a6-surfing_with_audio.mkv",
        "id": 7,
        "user": {
            "pseudo": "test8",
            "id": 7,
            "created_at": "2021-10-12T17:00:46",
            "username": "test8"
        },
        "enabled": 1,
        "created_at": "2021-10-14T09:58:09",
        "view": 0,
        "formats": {}
    }
}
```

### 8) Video list

Method : **GET**\
URI : */videos*\
Authentication : *not required*

Parameters :
```json
{
	"name": string,
	"user": int (user id),
	"duration": int (seconds),
	"page": int,
	"perPage": int
}
```

These parameters are all optional and need to be entered as query parameters in the URI. 

Response code : **200**\
Response data example:

```json
{
    "message": "Ok",
    "data": [
        {
            "user": {
                "username": "test8",
                "pseudo": "test8",
                "created_at": "2021-10-12T17:00:46",
                "id": 7
            },
            "created_at": "2021-10-12T17:10:39",
            "id": 3,
            "view": 0,
            "enabled": 1,
            "source": "/home/syoupheng/PythonProjects/ETNA_myAPI/public/11bf99e7-surfing_with_audio.mkv",
            "formats": {}
        },
        {
            "user": {
                "username": "test8",
                "pseudo": "test8",
                "created_at": "2021-10-12T17:00:46",
                "id": 7
            },
            "created_at": "2021-10-12T17:05:56",
            "id": 1,
            "view": 0,
            "enabled": 1,
            "source": "/home/syoupheng/PythonProjects/ETNA_myAPI/public/5230614f-surfing_with_audio.mkv",
            "formats": {}
        }
    ],
    "pager": {
        "current": 2,
        "total": 2
    }
}
```

### 9) Video list by user

Method : **GET**\
URI : *user/:id/videos*\
Authentication : *not required*

Parameters :
```json
{
	"page": int,
	"perPage": int
}
```

These parameters are all optional and need to be entered as query parameters in the URI.

Response code : **200**\
Response data example:

```json
{
    "message": "Ok",
    "data": [
        {
            "user": {
                "username": "test6",
                "pseudo": "test6",
                "created_at": "2021-10-12T17:00:18",
                "id": 5
            },
            "created_at": "2021-10-12T17:11:28",
            "id": 6,
            "view": 0,
            "enabled": 1,
            "source": "/home/syoupheng/PythonProjects/ETNA_myAPI/public/f4aa521e-surfing_with_audio.mkv",
            "formats": {}
        },
        {
            "user": {
                "username": "test6",
                "pseudo": "test6",
                "created_at": "2021-10-12T17:00:18",
                "id": 5
            },
            "created_at": "2021-10-12T17:11:24",
            "id": 5,
            "view": 0,
            "enabled": 1,
            "source": "/home/syoupheng/PythonProjects/ETNA_myAPI/public/a0ec48b9-surfing_with_audio.mkv",
            "formats": {}
        }
    ],
    "pager": {
        "current": 1,
        "total": 2
    }
}
```

### 9) Encoding video by id

This endpoint was designed to create copies of videos for each resolution lower or equal to the original video. No video encoding is done by requesting this endpoint.

Method : **PATCH**\
URI : *video/:id*\
Authentication : *not required*

Parameters :
```json
{
	"format": int (1080, 720, 480...etc),
	"file": string (name of the encoded file)
}
```

These parameters are all optional and need to be entered in the body of the request.

Response code : **200**\
Response data example:

```json
{
    "message": "Ok",
    "data": {
        "Video": {
            "user": {
                "username": "test6",
                "pseudo": "test6",
                "created_at": "2021-10-12T17:00:18",
                "id": 5
            },
            "created_at": "2021-10-12T17:11:24",
            "id": 5,
            "view": 0,
            "enabled": 1,
            "source": "/home/syoupheng/PythonProjects/ETNA_myAPI/public/a0ec48b9-surfing_with_audio.mkv",
            "formats": {
                "720": "/home/syoupheng/PythonProjects/Flask-MyYoutubeAPI/public/720/55c01bd6-Untitled",
                "480": "/home/syoupheng/PythonProjects/Flask-MyYoutubeAPI/public/480/c931b4c9-Untitled",
                "360": "/home/syoupheng/PythonProjects/Flask-MyYoutubeAPI/public/360/48499da3-Untitled",
                "240": "/home/syoupheng/PythonProjects/Flask-MyYoutubeAPI/public/240/3bc35e92-Untitled",
                "144": "/home/syoupheng/PythonProjects/Flask-MyYoutubeAPI/public/144/cd3bc6ca-Untitled"
            }
        }
    }
}
```

### 11) Updating videos

Method : **PUT**\
URI : */video/:id*\
Authentication : *required*\
Parameters :

```json
{
	"name": string,
	"user": int
}
```

These parameters need to be entered in the body of the request in JSON format. Mandatory parameters are signaled with a "*".

Response code : **200**\
Response data example:

```json
{
    "message": "Ok",
    "data": {
        "Video": {
            "user": {
                "username": "test6",
                "pseudo": "test6",
                "created_at": "2021-10-12T17:00:18",
                "id": 5
            },
            "created_at": "2021-10-12T17:11:24",
            "id": 5,
            "view": 0,
            "enabled": 1,
            "source": "/home/syoupheng/PythonProjects/ETNA_myAPI/public/a0ec48b9-surfing_with_audio.mkv"
        }
    }
}
```

### 12) Deleting videos

Method : **DELETE**\
URI : */video/:id*\
Authentication : *required*\

Parameters : *no parameters*

Response code : **204**\
Response data example: `{}`

### 13) Posting comments

Method : **POST**\
URI : */video/:id/comment*\
Authentication : *required*\
Parameters :

```json
{
	"body": string
}
```
This parameter needs to be entered in the body of the request.

Response code : **201**\
Response data example:

```json
{
    "message": "Ok",
    "data": {
        "body": "Great video !",
        "user": {
            "username": "test6",
            "pseudo": "test6",
            "created_at": "2021-10-12T17:00:18",
            "id": 5
        },
        "id": 10
    }
}
```

### 14) Comment list

Method : **GET**\
URI : */video/:id/comments*\
Authentication : *required*\
Parameters :

```
{
	"page": int,
	"perPage": int
}
```
These parameters are optional and need to be entered as query parameters in the URI.

Response code : **200**\
Response data example:

```json
{
    "message": "Ok",
    "data": [
        {
            "body": "This API is awesome !",
            "user": {
                "username": "test6",
                "pseudo": "test6",
                "created_at": "2021-10-12T17:00:18",
                "id": 5
            },
            "id": 12
        },
        {
            "body": "This sucks !",
            "user": {
                "username": "test6",
                "pseudo": "test6",
                "created_at": "2021-10-12T17:00:18",
                "id": 5
            },
            "id": 11
        }
    ],
    "pager": {
        "current": 1,
        "total": 2
    }
}
```