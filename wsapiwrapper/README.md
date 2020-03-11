This library communicates with wsbackend APIs. It is intended to be used by a 
frontend web application. 

wsapiwrapper uses the 
[requests library](https://requests.readthedocs.io/en/master/) for HTTP transactions. Its
 [json decoder](https://2.python-requests.org/en/master/user/quickstart/#json-response-content) 
 converts API responses (in JSON) to Python lists and dictionaries.