=========================API COMMANDS=========================
(GET) /catalog/
Returns list of images


(GET) /updatecatalog/
Sync image list for API with images that exist on the cloud
Return: nothing


(POST) /register/
Register a new user, new user gets 1 VM per image (from the catalog) 
Usage: Send JSON object with username,email,preferred_pass, and external_id.
		preferred_pass will be the password to log into each lab environment via ssh
		external_id is a unique identifier that will be used to reference this user in other calls
		This call requires login credentials
Example JSON:
	{
		"api_uname":"webportal", 
		"api_pass":"greg123",
		"username":"superhooks", 
		"email":"superhooks@greg.com", 
		"preferred_pass":"password123", 
		"external_id":"3"
	}
Example POST:
	curl -X POST http://127.0.0.1:8000/register/ -d '{"api_uname":"webportal", "api_pass":"greg123","username":"superhooks", "email":"superhooks@greg.com", "preferred_pass":"password123", "external_id":"3"}' -H "Content-Type: application/json"

(POST) /lablist/
Get list of labs (and ip addresses) associated with a specific user
Usage: Send JSON object with 'userid'. This is the same external_id provided on registration
EXAMPLE JSON:
	{"api_uname":"webportal", "api_pass":"greg123", "userid":"3"}
EXAMPLE POST:
	curl -X POST http://127.0.0.1:8000/lablist/ -d '{"api_uname":"webportal", "api_pass":"greg123", "userid":"3"}' -H "Content-Type: application/json"
EXAMPLE RESPONSE:
	{
    	"superhooks-15": "192.168.0.20 - ",
    	"superhooks-16": "192.168.0.11 - ",
    	"superhooks-17": "192.168.0.19 - "
	}


(POST) /rebuildlab/
Reset lab back to its starting image
Usage: Send JSON object with 'ipaddress'
EXAMPLE JSON:
	{"ipaddress":"10.0.0.1"}
EXAMPLE POST:
	curl -X POST http://127.0.0.1:8000/rebuildlab/ -d '{"ipaddress":"10.0.0.40"}' -H "Content-Type: application/json"
Return: HTTP Code 200

(POST) /enroll/
Enroll a user into a class. Builds a lab environment (Virtual Machine) based on the image name. Image name's uniquely identify classes.
Usage: Send JSON object with 'external_id', 'image_name', and 'cloud'
EXAMPLE JSON:
	{
		"api_uname":"webportal", 
		"api_pass":"greg123",
		"external_id":"3",
		"image_name":"cirros",
		"cloud":"chameleon"
	}
EXAMPLE POST:
	curl -X POST http://127.0.0.1:8000/enroll/ -d '{"api_uname":"webportal", "api_pass":"greg123","external_id":"5","image_name":"cirros", "cloud":"chameleon"}' -H "Content-Type: application/json"

(POST) /unenroll/
Unenroll a user from a class. Removes a lab environment (Virtual Machine) based on the image name. Image name's uniquely identify classes.
Usage: Send JSON object with 'external_id', and 'image_name'
EXAMPLE JSON:
	{
		"api_uname":"webportal", 
		"api_pass":"greg123",
		"external_id":"3",
		"image_name":"cirros"
	}
EXAMPLE POST:
	curl -X POST http://127.0.0.1:8000/unenroll/ -d '{"api_uname":"webportal", "api_pass":"greg123","external_id":"5","image_name":"cirros"}' -H "Content-Type: application/json"
