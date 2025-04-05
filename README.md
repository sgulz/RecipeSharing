# Recipe Sharing || Guzzle

QMUL Software Engineering Project - Recipe Sharing Website

## Language Stack
- HTML (frontend): building web elements
- CSS (frontend): styling webpages and elements
- Python -> Django (backend): creating element functionality and webpage interactivity
- SQL -> PostgreSQL (backend): querying databases

## Layered Software Architecture
- Presentation: user interface layer where we see and enter data into the application
- Business: responsible for handling business logic, like validation
- Application: handles moving data between the user interface and database
- Data: stores all the data

## MVT Design Pattern
- Model: defines all data and database rules
- View: processes data requests and returns responses
- Template: handles user interface

## Django Apps
- What is it: apps are directories which handle a single responsibility each
- What should they contain: models (define data), views (process data requests), services (business logic), 
- Guzzle app: default app in Django which handles the base settings and URL configuration
- Example apps: recipes (handling all the recipe-related functions), social (handles all the social aspects)
- Creating new apps: (from RecipeSharing) run 'python guzzle/manage.py startapp your_app_name'. Add the app name to INSTALLED_APPS in RecipeSharing/guzzle/guzzle/settings.py

## Django Admin
- Access: http://127.0.0.1:8000/admin/
- Username: guzzle
- Password: Guzzle123!
- Why: View all database details

## Kanban Agile Methodology
- Kanban board: https://miro.com/welcomeonboard/NnRBL0Z5b3l6S1AyWjZWTzUyOHl1SXhPdklMMnBmZVhRSkhXUzZuVHZnQ25QWEY2K0JXcnpOSjlreStQRjNnR0txaDJjTmxzS3piRnVzM3pvbVZVZlM0Y0Fra3kyNnc3allJVlRxcCs0OG9UdnlUcUZZNDVWNDJxN1RFNGs5VXZzVXVvMm53MW9OWFg5bkJoVXZxdFhRPT0hdjE=?share_link_id=802428780943

## Version Control Info
- Root directory: /RecipeSharing
- Main branch: origin/main

## Virtual Environment Info
- What is it: Needed to manage package dependencies 
- How to activate: Run command in terminal "source venv/bin/activate"
- How to deactivate: Run command in terminal "deactivate"
- Best practices: Activate venv at the start of development session, deactivate it when finished

## How to Run
- Run application: (from Root directory) Run "python guzzle/manage.py runserver"
- Run unit tests: TODO

## Potential Errors
- Venv won't activate: activation command is different on Mac and Windows
- Imports can't be found: change interpreter to RecipeSharing/venv/bin/python
- Updating CSS/HTML doesn't show on webpage: open webpage in incognito window (changes aren't cached)

## Database Tables

[User]  
id (PK)  
username  
passwordHash  

[Recipe]  
id (PK)  
authorID (FK -> User.id)  
title  
description  
instructions  
duration
servings  
calories  
createdAt  

[Ingredient]  
id (PK)  
name  

[Tag]  
id (PK)  
name  

[RecipeIngredient]  
id (PK)  
recipeID (FK -> Recipe.id)  
ingredientID (FK -> Ingredient.id)  
quantity  
unit  

[RecipeTag]  
id (PK)  
recipe_id (FK -> Recipe.id)  
tag_id (FK -> Tag.id)  

[Friend]  
id (PK)  
userID (FK -> User.id)  
friendID (FK -> User.id)  
status  

[Post]  
id (PK)  
userID (FK -> User.id)  
recipeID (FK -> Recipe.id)  
createdAt  

[FavouriteRecipe]  
id (PK)  
userID (FK -> User.id)  
recipeID (FK -> Recipe.id)  
