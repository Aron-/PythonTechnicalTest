# Origin Markets Backend Test

### Spec:

We would like you to implement an api to: ingest some data representing bonds, query an external api for some additional data, store the result, and make the resulting data queryable via api.
- Fork this hello world repo leveraging Django & Django Rest Framework. (If you wish to use something else like flask that's fine too.)
- Please pick and use a form of authentication, so that each user will only see their own data. ([DRF Auth Options](https://www.django-rest-framework.org/api-guide/authentication/#api-reference))
- We are missing some data! Each bond will have a `lei` field (Legal Entity Identifier). Please use the [GLEIF API](https://www.gleif.org/en/lei-data/gleif-lei-look-up-api/access-the-api) to find the corresponding `Legal Name` of the entity which issued the bond.
- If you are using a database, SQLite is sufficient.
- Please test any additional logic you add.

#### Project Quickstart

Inside a virtual environment running Python 3:
- `pip install -r requirements.txt`
- `./manage.py runserver` to run server.
- `./manage.py test` to run tests.

#### API

We should be able to send a request to:

`POST /bonds/`

to create a "bond" with data that looks like:
~~~
{
    "isin": "FR0000131104",
    "size": 100000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}
~~~
---
We should be able to send a request to:

`GET /bonds/`

to see something like:
~~~
[
    {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "legal_name": "BNPPARIBAS"
    },
    ...
]
~~~
We would also like to be able to add a filter such as:
`GET /bonds/?legal_name=BNPPARIBAS` to reduce down the results.


# Aron Willis Test Notes

### Spec:
| Methods |	URLs                          | Actions                        |
| ------- | ----------------------------- | ------------------------------ |
| GET     |	bonds/                        | Get all Bonds                  |
| GET     | bonds/?legal_name=:legal_name | Get Bonds by legal_name lookup |
| POST    | bonds/                        | Add new Bond                   |

### Bugs fixed / Minor amendments:
- requirement.txt amended to requirements.txt in readme.
- Django bonds app was not registered in settings.py.

### Specific steps taken:
- Set up Pycharm project on new computer, check for hello world.
- Created model after initial research on fields and serializer.
- DB migrations.
- Created subsequent views and tests.
- Added Token authentication and tests.

# Usage
- Set up virtual environment running Python 3: `pip install -r requirements.txt`.
- Create a user account with the following built in function: `manage.py createsuperuser`.
- Run the server before we make any requests: `manage.py runserver`.
- Send a POST request to `/api-token-auth/` with the `username` and `password` key value fields in the form body as JSON
to request an access token.
- Use the token in subsequent header requests as authentication in the format: KEY- `Authorization` VALUE- `Token X`
where X is the 40 character token value.
