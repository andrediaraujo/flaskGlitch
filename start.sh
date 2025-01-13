#!/bin/bash
# Activate virtual environment
source venv/bin/activate

# Run the Flask app with a production-ready WSGI server like Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:8000 hello:app