# HoundTrainer
A tool for managing custom node types in BloodHound  
## Usage
```
$ python houndtrainer-v4.py -h
usage: houndtrainer-v4.py [-h] [-o {list,upload,delete,deleteall}] [-b BASE_URL] [-m MODEL_PATH] [-k KIND]

Manage custom types in BloodHound.

options:
  -h, --help            show this help message and exit
  -o, --operation {list,upload,delete,deleteall}
                        Operation to complete.
  -b, --base-url BASE_URL
                        The base URL for the BloodHound instance.
  -m, --model-path MODEL_PATH
                        Path to the JSON model file to upload.
  -k, --kind KIND       Custom kind type to delete.
$
```
## Authentication
* This script uses a JWT for authentication and expects the value to be provided during runtime.
* To obtain a JWT (legally) login to your BHE or CE instance and view the 'Network' tab in the 'Developer Tools' in your browser of choice.
* This approach aligns with the recommendation from SpecterOps for quick API calls  
https://bloodhound.specterops.io/integrations/bloodhound-api/working-with-api#use-a-jwt%2Fbearer-token

### Operations
* [list](#list-custom-nodes)
* [upload](#upload-model)
* [delete](#delete-a-node-by-kind-name)
* [deleteall](#delete-all-nodes)

## Examples
### List custom nodes
```
$ python houndtrainer.py list http://127.0.0.1:8080
Enter JWT: <redacted.redacted.redacted>
[INFO] Listing custom types...
[INFO] ID: 1, Kind Name: ExampleUser
[INFO] ID: 2, Kind Name: ExampleSecurityUser
[INFO] ID: 3, Kind Name: ExampleGroup
[INFO] ID: 4, Kind Name: ExampleClass
[INFO] ID: 5, Kind Name: ExampleObject
[INFO] Done.
$
```

### Upload model
```
$ python houndtrainer.py upload http://127.0.0.1:8080 -m example-model-v3.json
Enter JWT: <redacted.redacted.redacted>
[INFO] Uploading model...
[INFO] Model uploaded successfully.
[INFO] Done.
$

$ python houndtrainer.py list http://127.0.0.1:8080
Enter JWT: <redacted.redacted.redacted>
[INFO] Listing custom types...
[INFO] ID: 1, Kind Name: ExampleUser
[INFO] ID: 2, Kind Name: ExampleSecurityUser
[INFO] ID: 3, Kind Name: ExampleGroup
[INFO] ID: 4, Kind Name: ExampleClass
[INFO] ID: 5, Kind Name: ExampleObject
[INFO] Done.
$
```

### Delete a node by kind name
```
$ python houndtrainer.py delete http://127.0.0.1:8080 -k ExampleObject
Enter JWT: <redacted.redacted.redacted>
[INFO] Deleting custom type: ExampleObject
[INFO] Deleted custom type: ExampleObject
[INFO] Done.
$

$ python houndtrainer.py list http://127.0.0.1:8080
Enter JWT: <redacted.redacted.redacted>
[INFO] Listing custom types...
[INFO] ID: 1, Kind Name: ExampleUser
[INFO] ID: 2, Kind Name: ExampleSecurityUser
[INFO] ID: 3, Kind Name: ExampleGroup
[INFO] ID: 4, Kind Name: ExampleClass
[INFO] Done.
$
```

### Delete all nodes
```
$ python houndtrainer.py deleteall http://127.0.0.1:8080
Enter JWT: <redacted.redacted.redacted>
[INFO] Deleting all custom types...
[INFO] Listing custom types...
[INFO] Deleting custom type: ExampleUser
[INFO] Deleted custom type: ExampleUser
[INFO] Deleting custom type: ExampleSecurityUser
[INFO] Deleted custom type: ExampleSecurityUser
[INFO] Deleting custom type: ExampleGroup
[INFO] Deleted custom type: ExampleGroup
[INFO] Deleting custom type: ExampleClass
[INFO] Deleted custom type: ExampleClass
[INFO] Done.
$

$ python houndtrainer.py list http://127.0.0.1:8080
Enter JWT: <redacted.redacted.redacted>
[INFO] Listing custom types...
[INFO] No custom kinds found.
[INFO] Done.
$
```
## TODO
* Print all custom type details to STDOUT
* Output node data to a file
* Support for authentication with an API key
