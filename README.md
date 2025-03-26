# RecipeSharing
QMUL Software Engineering Project - Recipe Sharing Website

LANGUAGE STACK:
- HTML (frontend): building web elements
- CSS (frontend): styling webpages and elements
- Python -> Django (backend): creating element functionality and webpage interactivity
- SQL -> MySQL (backend): querying databases

LAYERED SOFTWARE ARCHITECTURE:
- Presentation: user interface layer where we see and enter data into the application
- Business: responsible for handling business logic, like validation
- Application: handles moving data between the user interface and database
- Data: stores all the data

MVT DESIGN PATTERN:
- Model: defines all data and database rules
- View: processes data requests and returns responses
- Template: handles user interface

VERSION CONTROL INFO:
- Root directory: /RecipeSharing
- Main branch: origin/main

VIRTUAL ENVIRONMENT INFO:
- What is it: Needed to manage package dependencies 
- How to activate: Run command in terminal "source venv/bin/activate"
- How to deactivate: Run command in terminal "deactivate"
- Best practices: Activate venv at the start of development session, deactivate it when finished

HOW TO RUN:
- Run application: (from Root directory) Run "python guzzle/manage.py runserver"
- Run unit tests: ____

POTENTIAL ERRORS:
- Venv won't activate: activation command is different on Mac and Windows
- Updating CSS/HTML doesn't show on webpage: open webpage in incognito window (changes aren't cached)
