from typing import Optional, Dict, Any
import requests
import argparse
import logging
import getpass
import json
import sys
import csv

_HAS_PANDAS_SUPPORT = False
# Try importing pandas, handle error if missing
try:
    import pandas as pd
    _HAS_PANDAS_SUPPORT = True
except ImportError:
    pd = None

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# set the api version
api_version = "v2"
# node endpoint
custom_nodes_path = f"/api/{api_version}/custom-nodes"
# cypher endpoint
saved_queries_path = f"/api/{api_version}/saved-queries"

# module-level variable to store the JWT token, might refactor this
_JWT_TOKEN: Optional[str] = None

# Create a session for persistent connections
session = requests.Session()

# maybe this whole thing should just be in a class
def prompt_for_jwt(self): # Inside the API Client class
    while True:
        bearer_token = getpass.getpass("Enter JWT: ").strip()
        if bearer_token.count('.') == 2 and bearer_token:
            # Check JWT structure (two dots) and non-emptiness
            self._jwt_token = bearer_token
            return bearer_token
        logging.error("Invalid or empty JWT format. Please try again.")

def prompt_for_jwt():
    global _JWT_TOKEN
    # Return the token if it's already been set
    if _JWT_TOKEN is not None:
        return _JWT_TOKEN

    # Prompt only if the token is not set
    bearer_token = getpass.getpass("Enter JWT: ").strip()
    
    # perform some basic input validation, maybe make this a loop instead of exiting?
    if bearer_token.count('.') != 2 or not bearer_token:
        logging.error("Invalid or empty JWT format. Exiting.")
        sys.exit(1)
        
    # Store the token for subsequent calls
    _JWT_TOKEN = bearer_token
    return _JWT_TOKEN

# maybe this whole thing should just be in a class
def handle_request(method: str, url: str, **kwargs):
    bearer_token = prompt_for_jwt()
    # build the request headers
    req_headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }    
    try:
        # merge any headers that might have been passed in arguments, for flexibility
        if 'headers' in kwargs:
            req_headers.update(kwargs['headers'])
            del kwargs['headers']
            
        response = session.request(method, url, headers=req_headers, **kwargs)
        response.raise_for_status()
        
        # check for presence of content before attempting to decode JSON
        if response.content:
            # if content exists, attempt to decode it as JSON
            # todo: make this more flexible
            return response.json()
        else:
            # returning True for successful status codes like 204 or 200 with no body.
            return True
    except requests.exceptions.HTTPError as e:
        logging.error(f"No entry found: {e}")            
        return False
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return False

def write_json_to_file(data: Dict[str, Any], file_path: str, indent: int = 4) -> None:
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        print(f"Success: Data written to {file_path}")
        return True    
    except TypeError as e:
        print(f"Error: Failed to serialize data. Check if all elements are JSON-serializable (e.g., not sets, objects without __dict__): {e}")
        return False
    except IOError as e:
        print(f"Error: An IOError occurred (e.g., permission denied or path is invalid): {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# model methods
def pd_transform_csv_to_custom_types_json(csv_file_path: str) -> Dict[str, Any]:
    try:
        df = pd.read_csv(csv_file_path)
        # validate the CSV header
        required_cols = ['Kind Name', 'Icon Name', 'Color']
        if not all(col in df.columns for col in required_cols):
            logging.error("CSV missing required columns.")
            return {}
        # drop incomplete data from the dataframe
        df.dropna(subset=required_cols, inplace=True)
        # iterate through remaining data and build the model
        custom_types = {
            row['Kind Name'].strip(): {
                "icon": {
                    "type": "font-awesome",
                    "name": row['Icon Name'].strip(),
                    "color": row['Color'].strip()
                }
            }
            for _, row in df.iterrows()
        }
        return {"custom_types": custom_types}
    except FileNotFoundError:
        logging.error(f"CSV file not found: {csv_file_path}")
        return {}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {}

def transform_csv_to_custom_types_json(csv_file_path: str) -> Dict[str, Any]:
    custom_types = {}
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            # read rows as dictionaries with column headers as keys
            reader = csv.DictReader(csvfile)
            fieldnames = [name.strip() for name in reader.fieldnames]
            reader.fieldnames = fieldnames
            for row in reader:
                # confirm that the required columns exist and are not empty
                kind_name = row.get('Kind Name', '').strip()
                icon_name = row.get('Icon Name', '').strip()
                color = row.get('Color', '').strip()
                if not (kind_name and icon_name and color):
                    print(f"Skipping row due to missing data: {row}")
                    continue
                # build the nested dictionary structure for the current custom type
                custom_types[kind_name] = {
                    "icon": {
                        "type": "font-awesome",
                        "name": icon_name,
                        "color": color
                    }
                }
        # return the final structure
        return {"custom_types": custom_types}
    except FileNotFoundError:
        print(f"Error: CSV file not found at path '{csv_file_path}'")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}
    
# node management methods
def get_custom_type(base_url: str, kind_name: str) -> Optional[Dict[str, Any]]:
    logging.info(f"Listing custom type for kind_name '{kind_name}'...")
    url = f"{base_url}{custom_nodes_path}/{kind_name}"
    try:
        response = handle_request('GET', url)     
        return response 
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch custom type for kind_name '{kind_name}': {e}")
        return None

def list_custom_types(base_url: str) -> Optional[Dict[str, Any]]:
    logging.info("Listing all custom types...")
    url = f"{base_url}{custom_nodes_path}"
    try:
        response = handle_request('GET', url)
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch all custom types: {e}")
        return None

def upload_custom_model(base_url: str, file_path: str) -> None:
    logging.info(f"Uploading model from file: {file_path}...")
    url = f"{base_url}{custom_nodes_path}"
    try:
        with open(file_path, 'r') as file:
            payload = json.load(file)
        response = handle_request('POST', url, json=payload)
        if response:
            logging.info("Model uploaded successfully.")
            return True
    except FileNotFoundError:
        logging.error(f"File not found at path '{file_path}'")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def delete_custom_type(base_url: str, kind_name: str) -> None:
    logging.info(f"Deleting custom type: {kind_name}")
    url = f"{base_url}{custom_nodes_path}/{kind_name}"
    try:
        response = handle_request('DELETE', url)
        if response is not False:
            logging.info(f"Deleted custom type: {kind_name}")
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to delete '{kind_name}': {e}")
        return False

def delete_all_custom_types(base_url: str) -> None:
    logging.info("Deleting all custom types...")
    custom_list = list_custom_types(base_url)
    data = custom_list.get("data") if custom_list else None
    if data:
        for item in data:
            kind_name = item.get("kindName")
            if kind_name:
                delete_custom_type(base_url, kind_name)
            else:
                logging.warning(f"Missing 'kindName' for item: {item}, unable to process, skipping deletion.")
        return True
    else:
        logging.info("No custom types found.")
        return False

# cypher methods
def get_cypher_query(base_url: str, id: int) -> Optional[Dict[str, Any]]:
    logging.info(f"Retrieving cypher query for ID: '{id}'...")
    url = f"{base_url}{saved_queries_path}/{id}"
    try:
        response = handle_request('GET', url)
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch cypher query for ID '{id}' with message: {e}")
        return None

def list_cypher_queries(base_url: str, scope: str = "owned") -> Optional[Dict[str, Any]]:
    logging.info(f"Listing all cypher queries under scope: '{scope}'...")
    url = f"{base_url}{saved_queries_path}?scope={scope}"
    try:
        response = handle_request('GET', url)
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch cypher queries: {e}")
        return None

def export_cypher_query(base_url: str, id: int, output_file: str) -> Optional[Dict[str, Any]]:
    logging.info(f"Exporting cypher query ID '{id}'...")
    url = f"{base_url}{saved_queries_path}/{id}/export"
    try:
        response = handle_request('GET', url)
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch cypher queries for ID '{id}': {e}")
        return None

def export_cypher_queries(base_url: str, scope: str, output_file: str) -> Optional[Dict[str, Any]]:
    logging.info(f"Exporting cypher queries for scope '{scope}'...")
    url = f"{base_url}{saved_queries_path}/export?scope={scope}"
    try:
        response = handle_request('GET', url)
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch cypher queries for ID '{id}': {e}")
        return None

def upload_cypher_query(base_url: str, file_path: str) -> None:
    logging.info(f"Uploading query JSON from file: {file_path}...")
    url = f"{base_url}{saved_queries_path}/import"
    try:
        with open(file_path, 'r') as file:
            payload = json.load(file)
        response = handle_request('POST', url, json=payload)
        logging.info("Cypher query uploaded successfully.")
        return True
    except FileNotFoundError:
        logging.error(f"File not found at path '{file_path}'")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def upload_cypher_queries(base_url: str, file_path: str) -> None:
    if not file_path.lower().endswith(".zip"):
        logging.info(f"File '{file_path}' does not appear to be a ZIP. Multiple cypher queries must be uploaded as JSON files within a ZIP.")
        raise ValueError("File is not a ZIP archive.")
    logging.info("Uploading query zip from archive: {file_path}...")
    url = f"{base_url}{saved_queries_path}/import"
    try:
        with open(file_path, 'rb') as file:
            files = {'upload_file': (file.name, file)}
        response = handle_request('POST', url, files=files)        
        logging.info("Query ZIP uploaded successfully.")
        return True
    except FileNotFoundError:
        logging.error(f"File not found at path '{file_path}'")
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def delete_cypher_query(base_url: str, id: int) -> None:
    logging.info(f"Deleting cypher query ID: '{id}'")
    url = f"{base_url}{saved_queries_path}/{id}"
    try:
        response = handle_request('DELETE', url)
        if response is not False:
            logging.info(f"Deleted custom type: {id}")
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to delete '{id}': {e}")
        return False

def delete_all_cypher_queries(base_url: str, scope: str) -> None:
    ## get the list within scope and cycle through the delete by ID method
    logging.info(f"Retrieving cypher queries with scope {scope}")
    custom_list = list_cypher_queries(base_url)
    data = custom_list.get("data") if custom_list else None
    if data:
        for item in data:
            cypher_id = item.get("id")
            if cypher_id:
                delete_cypher_query(base_url, cypher_id)            
            else:
                logging.warning(f"Missing 'kindName' for item: {item}, skipping.")
        return True
    else:
        logging.info("No custom types found.")
        return False

# ---------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------
def main() -> None:    
    # Refactored CLI using subcommands, simplifying argument processing
    parser = argparse.ArgumentParser(description="Manage custom types and cypher queries in BloodHound.")
    subparsers = parser.add_subparsers(dest="operation", required=True)

    # Subcommand: create
    get_parser = subparsers.add_parser("create", help="Create a schema model from CSV definitions.")
    get_parser.add_argument("--type", choices=["model"], help="Type of resource to create.", required=True)
    get_parser.add_argument("--csv", help="CSV file that contains model definitions.", required=True)
    get_parser.add_argument("--file", help="Output file to write the model to.", required=True)

    # Subcommand: get
    get_parser = subparsers.add_parser("get", help="Retrieve a specific resource")
    get_parser.add_argument("--url", required=True)
    get_parser.add_argument("--type", choices=["node", "cypher"], required=True)
    get_parser.add_argument("--id", help="ID of the resource")
    get_parser.add_argument("--name", help="Name of the resource")

    # Subcommand: list
    list_parser = subparsers.add_parser("list", help="List custom node or cypher resources")
    list_parser.add_argument("--url", required=True)
    list_parser.add_argument("--type", choices=["node", "cypher"], required=True)
    list_parser.add_argument("--scope", choices=["all", "public", "shared", "owned"], default="owned", help="Scope for cypher queries")

    # Subcommand: upload
    upload_parser = subparsers.add_parser("upload", help="Upload custom node or cypher resources")
    upload_parser.add_argument("--url", required=True)
    upload_parser.add_argument("--type", choices=["node", "cypher"], required=True)
    upload_parser.add_argument("--file", required=True)

    # Subcommand: export
    export_parser = subparsers.add_parser("export", help="Export custom node or cypher resources")
    export_parser.add_argument("--url", required=True)
    export_parser.add_argument("--type", choices=["node", "cypher"], required=True)
    export_parser.add_argument("--id", help="ID of the resource (required for cypher query export)")
    export_parser.add_argument("--name", help="Kind name of the resource (required for custom type export)")
    export_parser.add_argument("--scope", choices=["all", "public", "shared", "owned"], default="owned", help="Scope for cypher queries")
    export_parser.add_argument("--file", required=True)

    # Subcommand: delete
    delete_parser = subparsers.add_parser("delete", help="Delete a custom node or cypher resource")
    delete_parser.add_argument("--url", required=True)
    delete_parser.add_argument("--type", choices=["node", "cypher"], required=True)
    delete_parser.add_argument("--id", help="ID of the resource")
    delete_parser.add_argument("--name", help="Name of the resource")

    # Subcommand: deleteall
    deleteall_parser = subparsers.add_parser("deleteall", help="Delete all custom node or cypher resources")
    deleteall_parser.add_argument("--url", required=True)
    deleteall_parser.add_argument("--type", choices=["node", "cypher"], required=True)
    deleteall_parser.add_argument("--scope", choices=["all", "public", "shared", "owned"], help="Scope for cypher queries")
    
    args = parser.parse_args()
    operation = args.operation
    type = args.type

    # create methods
    if operation == "create":
        if type == "model":
            if _HAS_PANDAS_SUPPORT:
                results = pd_transform_csv_to_custom_types_json(args.csv)
            else:
                results = transform_csv_to_custom_types_json(args.csv)
            if results:
                output_result = write_json_to_file(results, args.file, 4)
                if not output_result:
                    logging.error(f"Failed to write model from '{args.csv}' to file '{args.file}'.")
                    sys.exit(1)
                logging.info(f"Successfully wrote model from '{args.csv}' to file '{args.file}'.")
            else:
                logging.error(f"Failed to read model defintion from CSV file '{args.csv}'")                
        else:
            logging.error(f"No methods defined for operation '{operation}' and type {type}")

    # get methods
    if operation == "get":
        base_url = args.url
        if type == "node":
            # name argument is required for the cypher type
            if args.name:                
                results = get_custom_type(base_url, args.name)
                if results and 'data' in results:        
                    parsed_results = results
                    if isinstance(parsed_results['data'], dict):
                        item = parsed_results['data']
                        logging.info(f"ID: {item.get('id')}, Name: {item.get('kindName')}")
                    else:
                        logging.warning(f"Unexpected data type in response: {type(parsed_results['data'])}")
                else:
                    logging.info(f"No custom node types found with kind_name: {args.name}.")
            else:
                logging.error(f"A kind_name '--name' is required for the operation '{operation}' with type '{type}' .")
        elif type == "cypher":
            # id argument is required for the cypher type
            if args.id:
                bearer_token = prompt_for_jwt()
                # build the request headers
                headers = {
                    "Authorization": f"Bearer {bearer_token}",
                    "Accept": "application/json"
                }
                results = get_cypher_query(base_url, args.id)
                if results and 'data' in results:
                    # Use 'results' directly, no need for json.loads()
                    parsed_results = results 
                    
                    if isinstance(parsed_results['data'], dict):
                        item = parsed_results['data']
                        logging.info(f"ID: {item.get('id')}, Name: {item.get('name')}")
                else:
                    logging.info(f"No cypher queries found with id: {args.id}.")
            else:
                logging.error(f"A cypher '--id' is required for the operation '{operation}' with type '{type}' .")                       
          
    # list methods
    elif operation == "list":
        base_url = args.url
        if type == "node":
            custom_list = list_custom_types(base_url)
            data = custom_list.get("data") if custom_list else None
            if data:
                for item in data:
                    logging.info(f"ID: {item.get('id')}, Kind Name: {item.get('kindName')}")
            else:
                logging.info("No custom kinds found.")
        elif type == "cypher":            
            if args.scope is None:
                logging.info("No '--scope' provided for cypher operation, using the default value of 'owned'")
            cypher_list = list_cypher_queries(base_url, args.scope)
            data = cypher_list.get("data") if cypher_list else None
            if data:
                for item in data:
                    logging.info(f"ID: {item.get('id')}, Query: {item.get('name')}")
            else:
                logging.info("No cypher queries found.")

    # upload methods
    elif operation == "upload":
        base_url = args.url
        if type == "node":
            if not args.file:
                logging.error(f"Operation '{operation}' requires a '--file' parameter.")
                sys.exit(1)
            upload_status = upload_custom_model(base_url, args.file)
        elif type == "cypher":
            if not args.file:
                logging.error(f"Operation '{operation}' requires a '--file' parameter.")
                sys.exit(1)                
            upload_status = upload_cypher_query(base_url, args.file)
        if upload_status:
            logging.info(f"Operation '{operation}' for type '{type}' with file {args.file} was successful.")
        else:
            logging.error(f"Operation '{operation}' for type '{type}' with file {args.file} failed.")

    # export methods
    elif operation == "export":
        base_url = args.url
        if type == "node":        
            if not args.name:
                logging.error(f"Operation '{operation}' for type '{type}' requires the '--name' parameter.")
                sys.exit(1)
            data = get_custom_type(base_url, args.name)
            if data and 'data' in data:
                # extract the data object containing the custom type definition
                custom_type_data = data['data']                
                # extract the kindName for the top-level key
                kind_name = custom_type_data.get('kindName')
                if not kind_name:
                    logging.error("Retrieved data is missing 'kindName'. Cannot format for export.")
                    sys.exit(1)
                config = custom_type_data.get("config")
                if not config:
                    logging.error("Retrieved data is missing 'config' element. Cannot format for export.")
                    sys.exit(1)        
                if not 'icon' in config:                
                    logging.error("Retrieved data is missing 'icon' element. Cannot format for export.")
                    sys.exit(1)
                final_payload = {
                    "custom_types": {
                        kind_name: { 
                            "icon": config.get("icon")
                        }
                    }
                }
                output_result = write_json_to_file(final_payload, args.file, 4)
                if not output_result:
                    logging.error(f"Failed to write '{type}' data to file '{args.file}'.")
                    sys.exit(1)
                logging.info(f"Successfully wrote '{type}' data to file '{args.file}'.")
            else:
                logging.error(f"Failed to fetch custom node type for kind_name '{args.name}' with message: {e}")   
        elif type == "cypher":
            if not args.id:
                logging.error(f"Operation '{operation}' for type '{type}' requires the '--id' parameter.")
                sys.exit(1)
            data = export_cypher_query(base_url, args.id, args.file)
            if data:
                output_result = write_json_to_file(data, args.file, 4)
                if not output_result:
                    logging.error(f"Failed to write '{type}' data to file '{args.file}'.")
                    sys.exit(1)
                logging.info(f"Successfully wrote '{type}' data to file '{args.file}'.")     
            else:
                logging.error(f"Failed to fetch cypher query for ID '{id}' with message: {e}")          

    # delete methods
    elif operation == "delete":
        base_url = args.url
        if type == "node":
            # if the type is node we need to pass the kind_name (--name)
            if not args.name:
                logging.error(f"The '--name' parameter is required for {operation} operation with type {type}.")
                sys.exit(1)
            result = delete_custom_type(base_url, args.name)
            if result is False:
                logging.error(f"The {operation} operation with type {type} for kind_name {args.name} failed.")
                sys.exit(1)
            else:
                logging.info(f"Successfully completed {operation} for {type}.")            
        elif type == "cypher":
            # if the type is node we need to pass the id
            if not args.id:
                logging.error(f"The '--id' parameter is required for operation '{operation}' with type '{type}'.")
                sys.exit(1)
            result = delete_cypher_query(base_url, args.id)
            if result is False:
                logging.error(f"The operation '{operation}' with type '{type}' for id '{args.id}' failed.")
                sys.exit(1)
            else:
                logging.info(f"Successfully completed peration '{operation}' for {type}.")

    # deleteall methods
    elif operation == "deleteall":
        base_url = args.url
        logging.info(f"Running operation '{operation}' for type '{type}'.")
        bearer_token = prompt_for_jwt()
        # build the request headers
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Accept": "application/json"
        }
        logging.info(f"Operation {operation} requires confirmation.")
        while True:            
            continue_prompt = input("Enter 'Y' to continue and 'N' to cancel: ").strip().lower()
            if continue_prompt == "y":
                if args.type == "node":
                    delete_all_custom_types(base_url)
                elif args.type == "cypher":
                    delete_all_cypher_queries(base_url, args.scope)
                logging.info(f"Successfully completed operation '{operation}' for type '{type}'.")                    
                sys.exit()
            elif continue_prompt == "n":
                logging.info(f"User cancelled operation '{operation}'.")
                break
    logging.info("Done.")

if __name__ == '__main__':
    main()