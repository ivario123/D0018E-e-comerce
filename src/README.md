# The main app folder

Source Layout

```bash
|--- app.py              # The main app file, contains default routes and configuration
|--- auth.py             # The auth routes and configuration
|--- admin.py            # The admin routes and configuration
|--- sql                 # Src for all database facing code
|   |--- __init__.py     # The database connection
|   |--- auth.py         # The auth database code
|   |--- inventory.py    # The inventory database code
|--- models              # Src for all models
|   |--- __init__.py     # The models
|   |--- user.py         # The user model
|   |--- item.py         # The item model
```

## Running the app

To run the app, you simply run:

```bash
python app.py
```

from this folder.

## Dependencies

- [Flask](https://flask.palletsprojects.com/en/2.2.x/) - The web framework used
- [result](https://github.com/ivario123/pyresult) - A simple result monad for python
- [ssql](https://vesuvio-git.neteq.ltu.se/ivajns-9/ssql) - A simple SQL wrapper that uses sshtunnel to connect to a remote database
- [require](https://github.com/ivario123/require) - A simple way of automatically checking that all required fields are present in a posted JSON object
- [flask-login](https://flask-login.readthedocs.io/en/latest/) - A simple way of handling user sessions
