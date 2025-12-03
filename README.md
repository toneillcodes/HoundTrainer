# HoundTrainer
A tool for managing custom node types and cypher queries in BloodHound
## Quick Start & Prerequisites
HoundTrainer requires Python 3.x.
Pandas is optional for model creation and the script will fallback to standard libraries for CSV parsing if the import is unavailable.
1. Clone the repository
```
$ git clone https://github.com/toneillcodes/HoundTrainer.git
$ cd HoundTrainer
```

2. Install dependencies
```
$ pip install -r requirements.txt
```

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

## Operations
* [create](#create-operation)
* [list](#list-operation)
* [get](#get-operation)
* [upload](#upload-operation)
* [export](#export-operation)
* [delete](#delete-operation)
* [deleteall](#deleteall-operation)  
NOTE: For cypher operations, when no ```--scope``` argument is provided, the default scope used is 'owned'.

### Create Operation
#### Create a Custom Node Type Model
Create a model from CSV definitions
```
Kind Name,Icon Name,Color
ExampleUser,user,#4D93D9
ExampleRole,user-group,#47D359
```
Parse CSV (--csv) and generate JSON (--file)
```
$ python houndtrainer.py create --type model --csv examples\example-model.csv --file examples\example-model.json
Success: Data written to examples\example-model.json
[INFO] Successfully wrote model from 'examples\example-model.csv' to file 'examples\example-model.json'.
[INFO] Done.
$
```
References: 
* [examples\example-model.csv](examples\example-model.csv)
* [examples\example-model.json](examples\example-model.json)

### List Operation
#### List Custom Node Types
List custom node types
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
List output with cypher queries
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

### Get Operation
#### Get a Custom Node Type
Retrieve custom node type details by kind name (--name)
```
$ python houndtrainer.py get --type node --url http://127.0.0.1:8080 --name ExampleUser
[INFO] Listing custom type for kind_name 'ExampleUser'...
Enter JWT:
[INFO] ID: 280, Name: ExampleUser, type: font-awesome, Name: user, Color: #4D93D9
[INFO] Done.
$
```
#### Get a Cypher Query
Retrieve cypher query details by ID (--id)
```
$ python houndtrainer.py get --type cypher --url http://127.0.0.1:8080 --id 14
[INFO] Retrieving cypher query for ID: '14'...
Enter JWT:
[INFO] ID: 14, Name: Test Query, Created_At: 2025-11-29T15:05:37.546016Z, Updated_At: 2025-11-29T18:02:40.993889Z, User_id: 0f916532-08f7-47f4-bf1b-37b2317cce1b, Description: Testing, Query: "match(a:ExampleUser)\nwhere a.objectid = 'Bob'\nreturn a"
[INFO] Done.
$
```

### Upload Operation
#### Upload Custom Node Type Model
Upload example-model.json
```
$ python houndtrainer.py upload --type node --url http://127.0.0.1:8080 --file examples\example-model.json
[INFO] Uploading model from file: examples\example-model.json...
Enter JWT:
[INFO] Model uploaded successfully.
[INFO] Operation 'upload' for type 'node' with file examples\example-model.json was successful.
[INFO] Done.
$
```
Confirm upload success
```
$ python houndtrainer.py list --type node --url http://127.0.0.1:8080
[INFO] Listing all custom types...
Enter JWT:
[INFO] ID: 282, Kind Name: ExampleUser
[INFO] ID: 283, Kind Name: ExampleRole
[INFO] Done.
$
```
References: 
* [examples\example-model.json](examples\example-model.json)

#### Upload Single Cypher Query
Check the list of Cypher Queries
```
$ python houndtrainer.py list --type cypher --url http://127.0.0.1:8080
[INFO] Listing all cypher queries under scope: 'owned'...
Enter JWT:
[INFO] No cypher queries found.
[INFO] Done.
```
Upload the example cypher query file ```examples\example-cypher.json```
```
$ python houndtrainer.py upload --type cypher --url http://127.0.0.1:8080 --file examples\example-cypher.json
[INFO] Uploading query JSON from file: examples\example-cypher.json...
Enter JWT:
[INFO] Cypher query uploaded successfully.
[INFO] Operation 'upload' for type 'cypher' with file examples\example-cypher.json was successful.
[INFO] Done.
```
Check the list of Cypher Queries
```
$ python houndtrainer.py list --type cypher --url http://127.0.0.1:8080
[INFO] Listing all cypher queries under scope: 'owned'...
Enter JWT:
[INFO] ID: 17, Query: Test
[INFO] Done.
$
```
References: 
* [examples\example-cypher.json](examples\example-cypher.json)

#### Upload Cypher Query Pack (ZIP)
TODO

### Export Operation
#### Export a Custom Node Type
Export a Custom Node Type by kind name (--name)
```
$ python houndtrainer.py export --type node --url http://127.0.0.1:8080 --name ExampleRole --file examples\example-custom-type.json
[INFO] Listing custom type for kind_name 'ExampleRole'...
Enter JWT:
Success: Data written to examples\example-custom-type.json
[INFO] Successfully wrote 'node' data to file 'examples\example-custom-type.json'.
[INFO] Done.
$
```
References: 
* [examples\example-custom-type.json](examples\example-custom-type.json)
#### Export a Cypher Query
Export cypher query by ID (--id)
```
$ python houndtrainer.py export --type cypher --url http://127.0.0.1:8080 --id 16 --file examples\example-cypher.json
[INFO] Exporting cypher query ID '16'...
Enter JWT:
Success: Data written to examples\example-cypher.json
[INFO] Successfully wrote 'cypher' data to file 'examples\example-cypher.json'.
[INFO] Done.
$
```
References:
* [examples\example-cypher.json](examples\example-cypher.json)

### Delete Operation
#### Delete a Custom Node Type by kind name
Delete a Custom Node Type by kind name (--name)
```
$ python houndtrainer.py delete --type node --url http://127.0.0.1:8080 --name ExampleUser
[INFO] Deleting custom type: ExampleUser
Enter JWT:
[INFO] Deleted custom type: ExampleUser
[INFO] Successfully completed delete for node.
[INFO] Done.
$
```
Confirm deletion
```
$ python houndtrainer.py list --type node --url http://127.0.0.1:8080
[INFO] Listing all custom types...
Enter JWT:
[INFO] ID: 283, Kind Name: ExampleRole
[INFO] Done.
$
```
#### Delete a Cypher Query by ID
Delete Cypher Query by ID (--id)
```
$ python houndtrainer.py delete --type cypher --url http://127.0.0.1:8080 --id 14
[INFO] Deleting cypher query ID: '14'
Enter JWT:
[INFO] Deleted custom type: 14
[INFO] Successfully completed operation 'delete' for cypher.
[INFO] Done.
$
```
Confirm deletion
```
$ python houndtrainer.py list --type cypher --url http://127.0.0.1:8080
[INFO] Listing all cypher queries under scope: 'owned'...
Enter JWT:
[INFO] No cypher queries found.
[INFO] Done.
$
```

### Deleteall Operation
#### Delete all Custom Node Types
Delete all Custom Types
```
$ python houndtrainer.py list --type node --url http://127.0.0.1:8080
[INFO] Listing all custom types...
Enter JWT:
[INFO] ID: 280, Kind Name: ExampleUser
[INFO] ID: 281, Kind Name: ExampleRole
[INFO] Done.
$

$ python houndtrainer.py deleteall --type node --url http://127.0.0.1:8080
[INFO] Running operation 'deleteall' for type 'node'.
Enter JWT:
[INFO] Operation deleteall requires confirmation.
Enter 'Y' to continue and 'N' to cancel: Y
[INFO] Deleting all custom types...
[INFO] Listing all custom types...
[INFO] Deleting custom type: ExampleUser
[INFO] Deleted custom type: ExampleUser
[INFO] Deleting custom type: ExampleRole
[INFO] Deleted custom type: ExampleRole
[INFO] Successfully completed operation 'deleteall' for type 'node'.
$

$ python houndtrainer.py list --type node --url http://127.0.0.1:8080
[INFO] Listing all custom types...
Enter JWT:
[INFO] No custom kinds found.
[INFO] Done.
$
```

#### Delete all Cypher Queries
```
$ python houndtrainer.py deleteall --type cypher --url http://127.0.0.1:8080
Enter JWT: 
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

$ python houndtrainer.py list --type cypher --url http://127.0.0.1:8080
Enter JWT: 
[INFO] Listing custom types...
[INFO] No custom kinds found.
[INFO] Done.
$
```

## Authentication
* This script uses a JWT for authentication and expects the value to be provided during runtime.
* To obtain a JWT (legally) login to your BHE or CE instance and view the 'Network' tab in the 'Developer Tools' in your browser of choice.
* This approach aligns with the recommendation from SpecterOps for quick API calls  
https://bloodhound.specterops.io/integrations/bloodhound-api/working-with-api#use-a-jwt%2Fbearer-token

## API Reference
All operations utilize the following endpoints
| Operation Type | Endpoint |
| ---- | ---- |
| node| custom-nodes |
| cypher | saved-queries |

## TODO
* ~~Print all custom type details to STDOUT~~ Added 11/29/25
* ~~Output node data to a file~~ Added 11/29/25
* Support for authentication with an API key
* Ability to pass a list of IDs or Kind Names for get/export operations
* Validate operation to validate icon and OG schemas

## Shoutouts
* [cokernel](https://github.com/C0KERNEL): for help with testing, documentation updates and suggestions.