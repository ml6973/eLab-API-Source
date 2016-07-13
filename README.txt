=========================API COMMANDS=========================
(GET) /catalog/
Returns list of images


(GET) /updatecatalog/
Sync image list for API with images that exist on the cloud
Return: nothing


(POST) /register/
Register a new user, new user gets 1 VM per image (from the catalog) 
Usage: Send JSON object with 'username' and 'email'
Example JSON:
	{"username":"ryan", "email":"ryan@ryan.com"}
Example POST:
	curl -X POST http://127.0.0.1:8000/register/ -d '{"username":"ryan", "email":"ryan@ryan.com"}' -H "Content-Type: application/json"


(POST) /lablist/
Get list of labs (and ip addresses) associated with a specific user
Usage: Send JSON object with 'userid'
EXAMPLE JSON:
	{"userid":"7"}
EXAMPLE POST:
	curl -X POST http://127.0.0.1:8000/lablist/ -d '{"userid":"7"}' -H "Content-Type: application/json"
EXAMPLE RESPONSE:
	{
    	"brandon-12": "10.0.0.41",
    	"brandon-13": "10.0.0.42",
    	"brandon-14": "10.0.0.43"
	}