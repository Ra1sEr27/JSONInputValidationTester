The purpose of this script is to generate multiple requests with a given payload, then send to the server

Required libraries: urllib3, requests

Usage:
1. the HTTP request in txt file must be in the following format:
POST                                                            <-- the HTTP method must be in the first line
https://echo.free.beeceptor.com/sample-request?author=beeceptor <-- the URL must be in the second line
Host: echo.free.beeceptor.com
Content-Type: application/json
Content-Length: 66

{"name": {"name1": "Someone Else","name2": "Someone Else1"}, "age": 123, "city": "Bangkok"}

2. Example input:
Input the response JSON attribute - targeted request attribute to be replaced (a.b.c-a.b.d, a.d-a.c): parsedBody.name-name.name2,parsedBody.age-city
input payload (use , for multiple payloads | use 1024 for testing 1024 string length): !@#,null,123,1.23,1024,""

3. Don't forget to modify the proxy address and port (default: 127.0.0.1:8080)

4. The CSV output file must be closed before running the script

5. Have fun testing million fields
