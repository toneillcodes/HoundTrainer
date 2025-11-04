# HoundTrainer
A tool for managing custom node types in BloodHound  
## Usage
```
$ python houndtrainer.py
usage: houndtrainer.py [-h] [-m MODEL_PATH] [-k KIND] {list,upload,delete,deleteall} base_url
houndtrainer.py: error: the following arguments are required: operation, base_url
$
```

### Operations
* list
* upload
* delete
* deleteall

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
