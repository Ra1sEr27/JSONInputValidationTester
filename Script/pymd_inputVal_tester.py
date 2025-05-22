import requests
import json
import copy
import random
import csv
import urllib3

def generate_random_number_string(length):
    # First digit should not be zero to avoid leading zeros (optional)
    first_digit = str(random.randint(1, 9))
    # Generate the rest of the digits (1099)
    other_digits = ''.join(str(random.randint(0, 9)) for _ in range(length - 1))
    return first_digit + other_digits

def update_headers(headers: dict, target_header: str, new_value: str) -> dict:
    updated_headers = headers.copy()
    updated_headers[target_header] = new_value
    return updated_headers

def set_nested_value(data, dotted_key, new_value):
    keys = dotted_key.split(".")
    d = data

    # Handle special string values
    if new_value == '""':
        new_value = ""
    elif new_value == "1024":
        new_value = generate_random_number_string(1200)
    elif new_value == "null":
        new_value = None
    elif new_value == "__REMOVE__":
        pass  # Special keyword to indicate removal
    elif isinstance(new_value, str):
        try:
            new_value = float(new_value) if '.' in new_value else int(new_value)
        except ValueError:
            pass  # Keep as string if not a number

    # Traverse the nested structure
    for key in keys[:-1]:
        if key not in d or not isinstance(d[key], dict):
            return "None2"
        d = d[key]

    last_key = keys[-1]

    if isinstance(d, dict):
        if new_value == "__REMOVE__":
            if last_key in d:
                del d[last_key]
                return data
            else:
                return f'Key "{last_key}" not found to remove'
        else:
            if last_key in d:
                d[last_key] = new_value
                return data
            else:
                return f'Key "{last_key}" not found to set value'
    return "None3"



def get_nested_value(data, dotted_key, default=None):
    keys = dotted_key.split(".")
    d = data
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

def get_dot_paths(data, parent_key=""):
    paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                paths.extend(get_dot_paths(value, full_key))
            else:
                paths.append(full_key)
    return paths

def parse_mapping_input(input_string):
    pairs = []
    for part in input_string.split(","):
        # Remove extra spaces around the part first
        part = part.strip()
        # Split on dash, ignoring spaces around it
        items = [p.strip() for p in part.split("-", 1)]
        if len(items) == 2:
            pairs.append(items)
    return pairs

# Disable only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Set up proxy
proxies = {'http': 'http://127.0.0.1:8080',
           'https': 'http://127.0.0.1:8080'}
#Get value from user input
print("=" * 80)
print("PYMD Input Validation Tester".center(80))
print("=" * 80)
print("Author: Ra1sEr27")
print()  # Blank line
print("Tired of testing the same thing a million times by hand? Let me suffer for you. 🤖🔥")
print()  # Blank line
print("There is a thing called \"README.md\", go check it out")
print("""
===============================================================================
Enter the response JSON attribute and targeted request attribute to be replaced
===============================================================================

Example input: user1.name1-user2.name2,user1.age1 - user2.age2
      
Response body of the first request  |  Request body of the second request
-------------------------------------------------------------
{                                   |  {
  "user1": {                        |    "user2": {
    "name1": "Alice", -----------------> "name2": "Alice",
    "age1": 30,       -----------------> "age2": 30        
    "email1": "alice@mail.com"      |    }
  }                                 |  }
}                                   |
""")
targetAttributes = input("Input the source - targeted attribute: ")
print("""
==================================================================
Enter a value to modify the JSON attribute. Supported input types:
==================================================================
      
- Normal string      → e.g., hello
- Empty string       → input: ""
- Null value         → input: null
- Integer or float   → e.g. 42, 3.14
- Long number string → input: 1024 (generates a random 1024-character number string)
- Remove attribute   → input: __REMOVE__ (deletes different JSON attribute in each iteration)
""")
payloads = input("Input payload (use , for multiple payloads: ")
targetAttributes_array = parse_mapping_input(targetAttributes)
payloads_array = payloads.split(",")

#Initiate first request
with open("firstRequest.txt", "r", encoding="utf-8") as f:
    firstRequest_lines = f.read().splitlines()

firstRequest_method = firstRequest_lines[0].strip()
firstRequest_url = firstRequest_lines[1].strip()

# Headers end at the first blank line
blank_line_index = firstRequest_lines.index("")
firstRequest_headers = dict(line.split(": ", 1) for line in firstRequest_lines[2:blank_line_index])
firstRequest_body = "\n".join(firstRequest_lines[blank_line_index + 1:])
firstRequest_body_json = json.loads(firstRequest_body)

#Generate random number for header
firstRequest_headers_edited = update_headers(firstRequest_headers,"Accept","pymd1"+generate_random_number_string(3))

# Send request
response = requests.request(firstRequest_method, firstRequest_url, headers=firstRequest_headers_edited, json=firstRequest_body_json, proxies=proxies, verify=False)
response_body_json = response.json()

# Initiate second request
with open("secondRequest.txt", "r", encoding="utf-8") as f:
    secondRequest_lines = f.read().splitlines()

secondRequest_method = secondRequest_lines[0].strip()
secondRequest_url = secondRequest_lines[1].strip()
# Headers end at the first blank line
blank_line_index = secondRequest_lines.index("")
secondRequest_headers = dict(line.split(": ", 1) for line in secondRequest_lines[2:blank_line_index])
secondRequest_body = "\n".join(secondRequest_lines[blank_line_index + 1:])
#print(body)
secondRequest_body_json = json.loads(secondRequest_body)
print("Original Second Request {}".format(json.dumps(secondRequest_body_json, indent=2)))

#Replace value in the second request using value from the response
for targetAttr in targetAttributes_array:
    firstReq_targetAttr_value = get_nested_value(response_body_json,targetAttr[0])
    if firstReq_targetAttr_value != None:
        modified_secondReq_body = set_nested_value(secondRequest_body_json,targetAttr[1],firstReq_targetAttr_value)

print("Modified Second Request: {}".format(json.dumps(modified_secondReq_body, indent=2)))

#Get all dot notations from the second request
paths = get_dot_paths(secondRequest_body_json)
#Open CSV file for saving output
with open("PYMD_InputVal_Output.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["No.", "Attribute", "Payload", "Request Body", "Status Code", "Response Body"])

    counter = 1  # auto-incrementing number

#set up payload in each iteration
    for payload in payloads_array:
        for active_path in paths:
            #print("Paths: {}".format(paths))
            modified_body = copy.deepcopy(secondRequest_body_json)
            for path in paths:
                if path == active_path:
                    set_nested_value(modified_body, path, payload)
            
            secondReq_header_edited = update_headers(secondRequest_headers,"Accept","pymd2"+generate_random_number_string(3))
            response = requests.request(secondRequest_method, secondRequest_url, headers=secondReq_header_edited, json=modified_body, proxies=proxies, verify=False)
            print(f"\n▶ Active path: {active_path}, Payload: {payload}, Status Code: {response.status_code}")
            writer.writerow([
                    counter,
                    active_path,
                    payload,
                    json.dumps(modified_body),
                    response.status_code,
                    response.text# Save JSON as a single-line string
                ])
            counter += 1