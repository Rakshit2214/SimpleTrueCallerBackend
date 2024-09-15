
                                                        'contact_validation_api'

unzip the project

install requirements using -> pip install -r requirements.txt

run the following commands in terminal:
	1. python manage.py makemigrations
	2. python manage.py migrate 
	3. python manage.py populate_db (to populate with test data)

test env ready.
May use {https://sqliteviewer.app/#/} to open and view sqlite3 database.

testcase endpoints and paylods:

1) post, url=http://127.0.0.1:8000/api/register/ ,payload={"name":"rakshitWalia","username":{"username":"rakshitTest","password":"000000"},"registeredUserNumber":"01031010","userEmailId":"rakshit@instahyre.com"}

2) post, url= http://127.0.0.1:8000/api/login/ , payload = {"username":"user0", "password":"pass0"}

	[get the token from response and put it into header as {"Authentication" : "Bearer <token_key>"}]


3)get, url= http://127.0.0.1:8000/api/mark_contact_spam/, payload= {"contact_number":"1000000002"}

4) get, url= http://127.0.0.1:8000/api/search_by_name/, payload= {"name":"name"}
 (value can anything eg,name or name0 or nam)

5)get, url= http://127.0.0.1:8000/api/search_by_phone/, payload= {"phone_number":"1000000003"}

6)post, url = http://127.0.0.1:8000/api/mark_contact_spam/, payload = {"phone_number":"1000000003"} (only registered user with proper auth header can fo this)

7)post, http://127.0.0.1:8000/api/logout/, payload = {} (keep the auth header)