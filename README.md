# HoundTrainer
A tool for managing custom node types and cypher queries in BloodHound  
## Usage
```
$ python houndtrainer.py -h
usage: houndtrainer.py [-h] {create,get,list,upload,export,delete,deleteall} ...

Manage custom types and cypher queries in BloodHound.

positional arguments:
  {create,get,list,upload,export,delete,deleteall}
    create              Create a schema model from CSV definitions.
    get                 Retrieve a specific resource
    list                List custom node or cypher resources
    upload              Upload custom node or cypher resources
    export              Export custom node or cypher resources
    delete              Delete a custom node or cypher resource
    deleteall           Delete all custom node or cypher resources

options:
  -h, --help            show this help message and exit
$
```
## Authentication
* This script uses a JWT for authentication and expects the value to be provided during runtime.
* To obtain a JWT (legally) login to your BHE or CE instance and view the 'Network' tab in the 'Developer Tools' in your browser of choice.
* This approach aligns with the recommendation from SpecterOps for quick API calls  
https://bloodhound.specterops.io/integrations/bloodhound-api/working-with-api#use-a-jwt%2Fbearer-token

### Operations List
* [create](#create-operation)
* [get](#get-operation)
* [list](#list-operation)
* [upload](#upload-operation)
* [export](#export-operation)
* [delete](#delete-operation)
* [deleteall](#deleteall-operation)

### Operations References

### Create Operations
#### Create a Model
Create a model from CSV definitions

### Get Operations
#### Get a Custom Node Type
Get output with custom node type

### List Operations
#### List Custom Nodes
List output with custom node types
```
$ python houndtrainer.py list --type node --url http://127.0.0.1:8080
[INFO] Listing all custom types...
Enter JWT:
[INFO] ID: 280, Kind Name: ExampleUser
[INFO] ID: 281, Kind Name: ExampleRole
[INFO] Done.
$
```
List output when no custom node types nodes are found
```
$ python houndtrainer.py list --type node --url http://127.0.0.1:8080
[INFO] Listing all custom types...
Enter JWT:
[INFO] No custom kinds found.
[INFO] Done.
$
```
#### List Cypher Queries
List output with cypher queries under the 'owned' scope
```
$ python houndtrainer.py list --type cypher --url http://127.0.0.1:8080
[INFO] Listing all cypher queries under scope: 'owned'...
Enter JWT:
[INFO] ID: 14, Query: Test Query
[INFO] Done.
```
List output when no cypher queries are found
```
$ python houndtrainer.py list --type cypher --url http://127.0.0.1:8080
[INFO] Listing all cypher queries under scope: 'owned'...
Enter JWT:
[INFO] No cypher queries found.
[INFO] Done.
$
```
### Upload Operations
#### Upload Custom Type Model
Upload example-model.json
```
$ python houndtrainer.py upload --type node --url http://127.0.0.1:8080 --file example-model.json
[INFO] Uploading model from file: example-model.json...
Enter JWT:
[INFO] Model uploaded successfully.
[INFO] Operation 'upload' for type 'node' with file example-model.json was successful.
[INFO] Done.
$
```
Validate custom types were loaded
```
$ python houndtrainer.py list --type node --url http://127.0.0.1:8080
[INFO] Listing all custom types...
Enter JWT:
[INFO] ID: 280, Kind Name: ExampleUser
[INFO] ID: 281, Kind Name: ExampleRole
[INFO] Done.
$
```
#### Upload Single Cypher Query
Notes
#### Upload Cypher Query Pack (ZIP)
Notes

### Delete Operations
#### Delete a node by kind name
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

#### Delete all Nodes
```
$ python houndtrainer.py deleteall --type node http://127.0.0.1:8080
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

$ python houndtrainer.py list  --type node http://127.0.0.1:8080
Enter JWT: <redacted.redacted.redacted>
[INFO] Listing custom types...
[INFO] No custom kinds found.
[INFO] Done.
$
```

#### Delete all Cypher Queries
```
$ python houndtrainer.py deleteall --type cypher http://127.0.0.1:8080
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

$ python houndtrainer.py list  --type cypher http://127.0.0.1:8080
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
