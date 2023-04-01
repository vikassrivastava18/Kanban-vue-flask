# Kanban-vue-flask

## Summary
- A user needs to register for the application with a username, email and password. Password is hashed using werkzeug.security. Authentication is done with JWT, which carries the payload (user id and expiration time). Once registered, they can create lists and cards for daily tasks. The token is saved in Users local storage and sent along with every request.

- A card has the information about the deadline and the completion time. Comparing the completion time and the deadline, one can tell if the card was not finished in time, is pending, or delayed.

- A card can be moved from one list to another using drag and drop. The backend saves the information on the cards movement.

- The card can be edited or deleted by the user.

- Daily/monthly reminder - User gets the reminder for the tasks not completed before the set deadline, through Google-chat webhook

- Export - the list information can be exported by the user in csv format.

## Description
A multiuser Kanban application for managing daily tasks.

# Tools
- Flask - For creating the backend
- Sqlite - For saving the data
- Vue - For creating the frontend
- Flask-Sqlalchemy - For interacting with the database
- Flask-jwt - For authentication (token based)
- Bootstrap - For the layout and styling
- Celery, Redis - For the schedulers


## DB Schema Design

### User
- userid(integer, primarykey, autoincrement)
- username(sting, unique)
- email(string, unique)
- password(string)
- active(boolean)


### List - 
	(On to Many relationship with User)
- list_id(integer, primarykey, autoincrement)
- name(string)
- user(integer, foreignkey(User))


### Card - 
	(On to Many relationship with List)
- card_id(integer, primarykey, autoincrement)
- list(integer, foreignkey(List))


###TokenLogout -
	Add the token after logout as it may not have expired yet
- token_id(integer, primarykey, autoincrement)
- token(string)
- logout_on(datetime)



### API for User - Create, Read, Update, Delete
### API for List - Create, Read
### API for Card - Create, Read, Update, Delete

### Architecture - MVC with Flask (Model + Controller)and Vue(Vue)


