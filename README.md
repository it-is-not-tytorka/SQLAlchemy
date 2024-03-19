# Flask + SQLAlchemy
This project is my first experience when I worked with a database. 
I realized backend of a service which allows to create a card of your friend and add notes about this friend.
For example, you can create a friend card which has name "Bob" and description "My friend from a job". 
Now you can add notes after you meet him to remember something. Just create a note with description 
"He helped me with a task and saved my life" and add score "5". Here we are. Create more friends and notes to manage 
your relationships.   
# First of all   
To run this application clone this repository, install `requirements.txt`, set your database URL in
a python module `.app/db.py` and run `run.py` module. You can check how this application works by 
using Postman. For this you can find a file `FlaskSQL.postman_collection.json` in this repo and import 
to your own postman workspace and not write urls by yourself.   
# Database
This is a diagram of tables in a database. 
At this moment database run on a local machine. **Don't forget to set your database URL in** `.app/db.py`.
For details how models work see python module `.app/models.py`
![db_relationships.png](static%2Fdb_relationships.png)
## Let's start
### USERS
For details see `.app/views/users.py`
### User create
First of all we need to create a user. You can choose any username and password you want.
But email must be unique. If some user already has email you want to use then will be an error.
### `POST (http method) http://127.0.0.1:5000/user/create (url)`  
Request example:
```json
{
    "username": "yourname",
    "email": "testemail@gmail.com",
    "password": "qwerty123456"
}
```
Response example:
```json
{
    "message": "User created successfully",
    "user_id": 1
}
```
---
### User get
Then if you want to check user's information run this. In url provide user id you want to get.
### `GET http://127.0.0.1:5000/user/1`
Response example:
```json
{
    "user_id": 1,
    "username": "yourname",
    "email": "testemail@gmail.com",
    "password": "qwerty123456"
}
```
---
### User edit
If you want to edit some information run this. But remember that you can change username and 
password as you wish. Email will change only if a new email is unique in a database. Otherwise, 
will be error `CONFLICT` and nothing will change. In the url provide user id you want to edit.
### `PATCH http://127.0.0.1:5000/user/1/edit`
Request example:
```json
{
    "username": "mynewname",
    "password": "newsmartpassword",
    "email": "uniqueemail@gmail.com"
}
```
Response example:
```json
{
    "user_id": 1,
    "username": "mynewname",
    "email": "uniqueemail@gmail.com",
    "password": "newsmartpassword"
}
```
### FRIENDS
For details see `.app/views/friends.py`
### Friend create
Now it's time to create our friend Bob! Notice that there are keys `rating` and `notes` in the response.
`rating` shows an average scores of notes and `notes` is a list which contains all notes you'll create about this friend.
In the url provide user id who creates a new friend.
### `POST http://127.0.0.1:5000/user/1/friend/create`  
Request example:
```json
{
    "name": "Bob",
    "description": "Friend from a job"
}
```
Response example:
```json
{
    "user_id": 1,
    "friend_id": 1,
    "friend_name": "Bob",
    "description": "Friend from a job",
    "rating": "Not enough data",
    "notes": []
}
```
---
### Friend get
If you want to get all information about one friend. In url provide friend id you want to get.
### `GET http://127.0.0.1:5000/friend/1`  
Response example:
```json
{
    "user_id": 1,
    "friend_id": 1,
    "friend_name": "Bob",
    "description": "Friend from a job",
    "rating": "Not enough data",
    "notes": []
}
```
---
### Friend get all
To get all friends you've created. You can order them by `name` in ascending order
or `count_of_notes` in descending order. 
Everything else will be equaled order by `rating` in descending order. 
In the url provide user id whose friends you want to get.
### `GET http://127.0.0.1:5000/user/1/friend/all`
Request example:
```json
{
    "order_by": "name"
}
```
Response example:
```json
[
    {
        "user_id": 1,
        "friend_id": 1,
        "friend_name": "Bob",
        "description": "Friend from a job",
        "rating": "Not enough data",
        "notes": []
    }
]
```
---
### Friend edit
If some mistake has been made during creating a friend you always can solve it by running this. 
But as `User edit` you can't change `user_id` and `friend_id`. You can edit only friend's name and his description.
In the url provide friend id you want to edit.
### `PATCH http://127.0.0.1:5000/friend/1/edit`  
Request example:
```json
{
    "name": "Boooob",
    "description": "A super friend from my job"
}
```
Response example:
```json
{
    "user_id": 1,
    "friend_id": 1,
    "friend_name": "Boooob",
    "description": "A super friend from my job",
    "rating": "Not enough data",
    "notes": []
}
```
---
### Friend delete
To delete some friend run this. Deleted friends won't be visible running `Friend get` or `Friend get all`.
In the url provide friend id you want to delete.
### `DELETE http://127.0.0.1:5000/friend/1/delete`
Response example:
```json
{
    "message": "Friend has been deleted successfully"
}
```
---
### Friend restore
To restore a deleted friend use this. All notes a friend had will remain with him.
In the url provide friend id you want to restore.
### `PUT http://127.0.0.1:5000/friend/1/restore`
Response example:
```json
{
    "user_id": 1,
    "friend_id": 1,
    "friend_name": "Boooob",
    "description": "A super friend from my job",
    "rating": "Not enough data",
    "notes": []
}
```
---
### NOTES 
For more details see `.app/views/notes.py`.
### Note create
Creating a note. Notice that `score` is an integer and must be only 1, 2, 3, 4 or 5. 
Also, `score` influences a friend's rating.
`friend_id` is an id of a friend you want to describe. 
Only user who created a friend with this `friend_id` can create a note about him. 
`description` contains everything you want. 
It's ok to create an empty `description`. 
Notice that after this request responses of `friend get` and `friend get all` will change 
because a new note will be added there.
In the url provide user id who creates a new note.
### `POST http://127.0.0.1:5000/user/1/note/create`  
Request example:
```json
{
    "friend_id": 1,
    "description": "he helped me with a task and saved my life",
    "score": 5
}
```
Response example:
```json
{
    "user_id": 1,
    "friend_id": 1,
    "note_id": 1,
    "description": "he helped me with a task and saved my life",
    "score": 5
}
```
---
### Note get
To get a note run this. In the url provide a note id you want to get.
### `GET http://127.0.0.1:5000/note/1`
Response example:
```json
{
    "user_id": 1,
    "friend_id": 1,
    "note_id": 1,
    "description": "he helped me with a task and saved my life",
    "score": 5
}
```
---
### Note edit
To edit a `desription` or a `score` of a note. If you change `score` of a note then a friend's rating also will be changed.
In the url provide note id you want to edit.
### `PATCH http://127.0.0.1:5000/note/1/edit`  
Request example:
```json
{
    "description": "he helped me with a job",
    "score": 4
}
```
Response example:
```json
{
    "user_id": 1,
    "friend_id": 1,
    "note_id": 1,
    "description": "he helped me with a job",
    "score": 4
}
```
---
### Note delete
If you want to delete a note. Deleted notes won't be visible running `friend get`, `friend get all`. 
Also, a friend's rating will be calculated without deleted notes. In the url provide note id you want to delete.
### `DELETE http://127.0.0.1:5000/note/1/delete`
Response example:
```json
{
    "message": "Note has been deleted successfully"
}
```
---
### Note restore
If you want to restore a deleted note. A friend's rating will be calculated with the restored note.
In the url provide note id you want to restore.
### `PUT http://127.0.0.1:5000/note/1/restore`
Response example:
```json
{
    "user_id": 1,
    "friend_id": 1,
    "note_id": 1,
    "description": "he helped me with a job",
    "score": 4
}
```
