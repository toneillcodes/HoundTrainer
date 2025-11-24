from typing import Optional, Dict, Any
import requests
import argparse
import logging
import getpass
import json
import sys

# Try importing pandas, handle error if missing
try:
    import pandas as pd
except ImportError:
    pd = None

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def list_custom_types(base_url: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    logging.info("Listing custom types...")
    url = f"{base_url}/api/v2/custom-nodes"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch custom types: {e}")
        return None

def upload_custom_model(base_url: str, headers: Dict[str, str], model_path: str) -> None:
    logging.info("Uploading model...")
    url = f"{base_url}/api/v2/custom-nodes"
    try:
        with open(model_path, 'r') as file:
            payload = json.load(file)
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        logging.info("Model uploaded successfully.")
    except FileNotFoundError:
        logging.error(f"File not found at path '{model_path}'")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def delete_custom_type(base_url: str, headers: Dict[str, str], kind_name: str) -> None:
    logging.info(f"Deleting custom type: {kind_name}")
    url = f"{base_url}/api/v2/custom-nodes/{kind_name}"
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        logging.info(f"Deleted custom type: {kind_name}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to delete '{kind_name}': {e}")

def delete_all_custom_types(base_url: str, headers: Dict[str, str]) -> None:
    logging.info("Deleting all custom types...")
    custom_list = list_custom_types(base_url, headers)
    data = custom_list.get("data") if custom_list else None
    if data:
        for item in data:
            kind_name = item.get("kindName")
            if kind_name:
                delete_custom_type(base_url, headers, kind_name)
            else:
                logging.warning(f"Missing 'kindName' for item: {item}, skipping.")
    else:
        logging.info("No custom types found.")

# ---------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Manage custom types in BloodHound.")
    
    # Add 'correlate' to choices
    parser.add_argument("-o", "--operation", choices=["list", "upload", "delete", "deleteall"],
                        help="Operation to complete.")
    
    parser.add_argument("-b", "--base-url", help="The base URL for the BloodHound instance.")
    parser.add_argument("-m", "--model-path", help="Path to the JSON model file to upload.")
    parser.add_argument("-k", "--kind", help="Custom kind type to delete.")

    args = parser.parse_args()
    operation = args.operation
    
    # base-url is required
    if not args.base_url:
        logging.error(f"Operation '{operation}' requires a '--base-url' parameter.")
        sys.exit(1)
        
    base_url = args.base_url

    bearer_token = getpass.getpass("Enter JWT: ").strip()
    # perform some basic input validation
    if bearer_token.count('.') != 2:
        logging.error("Invalid JWT format.")
        sys.exit(1)

    # build the request headers
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }

    # upload model (schema)
    if operation == "upload":
        if not args.model_path:
            logging.error("Model path is required for upload operation.")
            sys.exit(1)
        upload_custom_model(base_url, headers, args.model_path)

    # list
    elif operation == "list":
        custom_list = list_custom_types(base_url, headers)
        data = custom_list.get("data") if custom_list else None
        if data:
            for item in data:
                logging.info(f"ID: {item.get('id')}, Kind Name: {item.get('kindName')}")
        else:
            logging.info("No custom kinds found.")

    # delete node
    elif operation == "delete":
        if not args.kind:
            logging.error("Kind name is required for delete operation.")
            sys.exit(1)
        delete_custom_type(base_url, headers, args.kind)

    elif operation == "deleteall":
        delete_all_custom_types(base_url, headers)

    logging.info("Done.")

if __name__ == '__main__':
    main()
