 ## Register 

> - This endpoint is to create a new user in the database, also automatically creates a blank profile.

```python

POST <base hosting url>/api/users/signup/

```

Supported attributes:

| Attribute                | Type     | Required | Description           |
|--------------------------|----------|----------|-----------------------|
| `username`              | str | Yes      | Username of the new user. |
| `password`              | str | Yes       | password of the new user. |


If successful, returns [`201`](rest/index.md#status-codes) and the following
response attributes:

| Attribute                | Type     | Description           |
|--------------------------|----------|-----------------------|
| `password`              | str | Username of the new user. |
| `is_active`              | bool | The activity of the user's account |
| `username`              | str |  password of the new user. |

Example request:

```shell
 url-    "<base hosting url>/api/users/signup/"
 METHOD- "POST"
 BODY-   {"username":"divij",
         "password":"sample_pass"}
```

Example response:

```json
{
    "password": "sample_pass",
    "is_active": true,
    "username": "divij"
}
```

## Login 

> - This endpoint is to login an existing user in the database.

```python

POST <base hosting url>/api/users/login/

```

Supported attributes:

| Attribute                | Type     | Required | Description           |
|--------------------------|----------|----------|-----------------------|
| `username`              | str | Yes      | Username of the user. |
| `password`              | str | Yes       | password of the user. |


If successful, returns [`200`](rest/index.md#status-codes) and the following
response attributes:

| Attribute                | Type     | Description           |
|--------------------------|----------|-----------------------|
| `expiry`              | datetime | Expiry time of login session. |
| `token`              | str | The token to include in auth header for future authentication |

Example request:

```shell
 url-    "<base hosting url>/api/users/login/"
 METHOD- "POST"
 BODY-   {"username":"divij",
         "password":"sample_pass"}
```

Example response:

```json
{
    "expiry": "2024-03-12T06:44:58.876783+05:30",
    "token": "5fefe7314d5f99abf22c7b9c7bd691a2b23c3061cd7af4bcf6b8ffb74feb112d"
}
```

## Logout

> - This endpoint is to logout a logged in user.

```python

POST <base hosting url>/api/users/logout/

```

Headers:

| Header                | Type     | Required | Description           |
|--------------------------|----------|----------|-----------------------|
| `Authorization`              | str | Yes      | The auth token of logged in user. |

If successful, returns [`204`](rest/index.md#status-codes) and no response attributes:

Example request:

```shell
 url-    "<base hosting url>/api/users/logout/"
 METHOD- "POST"
 HEADER- "Authorizattion":"Token <your_access_token>"
```


## Update/Create Profile 

> - This endpoint is to update profile of an existing user in the database.

```python

PUT <base hosting url>/api/users/profile/update/

```

Headers:

| Header                | Type     | Required | Description           |
|--------------------------|----------|----------|-----------------------|
| `Authorization`              | str | Yes      | The auth token of logged in user. |

Supported attributes:

| Attribute                | Type     | Required | Description           |
|--------------------------|----------|----------|-----------------------|
| `profile_picture`              | image file | No      | display picture of user. |
| `bio`              | str | No      | description of user or bio. |
| `slug`              | str | No       | slug username/ nickname. |


If successful, returns [`200`](rest/index.md#status-codes) and the following
response attributes:

| Attribute                | Type     | Description           |
|--------------------------|----------|-----------------------|
| `profile_picture`              | image file | display picture of user. |
| `bio`              | str | description of user or bio. |
| `slug`              | str | slug username/ nickname. |

Example request:

```shell
 url-    "<base hosting url>/api/users/profile/delete/"
 METHOD- "PUT"
 HEADER- "Authorizattion":"Token <your_access_token>"
 BODY-   {"bio":"Hello i am new at Medyya",
         "slug":"divu123",
         "profile-picture":<image_file>}
```

Example response:

```json
{
    "profile_picture": "/media/profile_pictures/default_pic.png",
    "bio": "Hello i am new at Medyya",
    "slug": "divuu123"
}
```

## Delete Profile and User

> - This endpoint is to update profile of an existing user in the database.

```python

DELETE <base hosting url>/api/users/profile/delete/

```

Supports NO ATTRIBUTES

If successful, returns [`200`](rest/index.md#status-codes) and NO ATTRIBUTES.

Example request:

```shell
 url-    "<base hosting url>/api/users/profile/delete/"
 METHOD- "DELETE"
 HEADER- "Authorizattion":"Token <your_access_token>"
```

## View all profiles

> - This endpoint is to get profiles of all existing users.

```python

GET <base hosting url>/api/users/profile/view-all/

```

Headers:

| Header                | Type     | Required | Description           |
|--------------------------|----------|----------|-----------------------|
| `Authorization`              | str | Yes      | The auth token of logged in user. |

Supports NO ATTRIBUTES

If successful, returns [`200`](rest/index.md#status-codes) and returns the following:

| Attribute                | Type     | Description           |
|--------------------------|----------|-----------------------|
| `profile_picture`              | image file | display picture of user. |
| `bio`              | str | description of user or bio. |
| `slug`              | str | slug username/ nickname. |
| `user`              | str | username of the profile's user. |
| `user_full_name`              | str | Full name of user. |

Example request:

```shell
 url-    "<base hosting url>/api/users/profile/view-all/"
 METHOD- "GET"
 HEADER- "Authorizattion":"Token <your_access_token>"
```

Example response:

```json
[
    {
        "user": "divij",
        "user_full_name": "Divij Mehta",
        "connections": 1,
        "profile_picture": "/media/profile_pictures/aphoto_Y0aYKXG.jpg",
        "bio": "Django Developer",
        "slug": "divij2510"
    },
    {
        "user": "haarsheel",
        "user_full_name": " ",
        "connections": 1,
        "profile_picture": "/media/profile_pictures/default_pic.png",
        "bio": "Hey there, I just joined Medyya",
        "slug": "haarsheel"
    },
    {
        "user": "ashar.devansh@outlook.com",
        "user_full_name": " ",
        "connections": 0,
        "profile_picture": "/media/profile_pictures/default_pic.png",
        "bio": "Hey there, I just joined Medyya",
        "slug": "ashardevanshoutlookcom"
    },
    {
        "user": "testuser",
        "user_full_name": " ",
        "connections": 0,
        "profile_picture": "/media/profile_pictures/default_pic.png",
        "bio": "Hey there, I just joined Medyya",
        "slug": "testuser"
    }
]
```

## View a profile

> - This endpoint is to get profile of a specifific user.

```python

GET <base hosting url>/api/users/profile/view/<str:username>

```

Headers:

| Header                | Type     | Required | Description           |
|--------------------------|----------|----------|-----------------------|
| `Authorization`              | str | Yes      | The auth token of logged in user. |

Requires a string in url <username>:

| Attribute                | Type     | Description           |
|--------------------------|----------|-----------------------|
| `username`              | str | username of profile's user. |

If successful, returns [`200`](rest/index.md#status-codes) and returns the following:

| Attribute                | Type     | Description           |
|--------------------------|----------|-----------------------|
| `profile_picture`              | image file | display picture of user. |
| `bio`              | str | description of user or bio. |
| `slug`              | str | slug username/ nickname. |
| `user`              | str | username of the profile's user. |
| `user_full_name`              | str | Full name of user. |

Example request:

```shell
 url-    "<base hosting url>/api/users/profile/view/divij"
 METHOD- "GET"
 HEADER- "Authorizattion":"Token <your_access_token>"
```

Example response:

```json
{
    "user": "divij",
    "user_full_name": "Divij Mehta",
    "connections": 1,
    "profile_picture": "/media/profile_pictures/aphoto_Y0aYKXG.jpg",
    "bio": "Django Developer",
    "slug": "divij2510"
}
```

## View mutual connections

> - This endpoint is to get profiles of all recommended users.

```python

GET <base hosting url>/api/users/profile/view-recommended/

```

Headers:

| Header                | Type     | Required | Description           |
|--------------------------|----------|----------|-----------------------|
| `Authorization`              | str | Yes      | The auth token of logged in user. |

Supports NO ATTRIBUTES

If successful, returns [`200`](rest/index.md#status-codes) and returns the following:

| Attribute                | Type     | Description           |
|--------------------------|----------|-----------------------|
| `profile_picture`              | image file | display picture of user. |
| `bio`              | str | description of user or bio. |
| `slug`              | str | slug username/ nickname. |
| `user`              | str | username of the profile's user. |
| `user_full_name`              | str | Full name of user. |

Example request:

```shell
 url-    "<base hosting url>/api/users/profile/view-recommended/"
 METHOD- "GET"
 HEADER- "Authorizattion":"Token <your_access_token>"
```

Example response:

```json
[
    {
        "user": "divij",
        "user_full_name": "Divij Mehta",
        "connections": 1,
        "profile_picture": "/media/profile_pictures/aphoto_Y0aYKXG.jpg",
        "bio": "Django Developer",
        "slug": "divij2510"
    },
    {
        "user": "haarsheel",
        "user_full_name": " ",
        "connections": 1,
        "profile_picture": "/media/profile_pictures/default_pic.png",
        "bio": "Hey there, I just joined Medyya",
        "slug": "haarshu"
    }
]
```
