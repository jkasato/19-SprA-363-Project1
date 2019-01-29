# running the app -- prereqs
- run `create.sql` to initialize the database
- change contents in `password` file to match mysql password

# run httpserver.py
`python3 httpserver.py`

# run without httpserver.py
`python3 -m http.server --bind localhost --cgi 8000`

# visit page from server
http://localhost:8000/app.html

# tips
## run .py standalone in interpreter
`python3 -i cgi-bin/simple.py`

