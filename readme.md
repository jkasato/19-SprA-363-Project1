# run httpserver.py
python3 httpserver.py

# run without httpserver.py
python3 -m http.server --bind localhost --cgi 8000


# run .py standalone in interpreter
python3 -i cgi-bin/simple.py


# visit page from server
http://localhost:8000/login.html