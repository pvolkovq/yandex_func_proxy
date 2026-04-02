import sys
import ast
import logging
import requests
import traceback

logger = logging.getLogger("func_logger")

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

def request(event, context):
    method = event["httpMethod"]
    data = event.get("body", {})
    url = data.get("url", False)
    params = event["queryStringParameters"].get("params", {})
    headers = event["queryStringParameters"].get("headers", {})
    response_type = event["queryStringParameters"].get("response_type", "")
    
    if headers:
        headers = ast.literal_eval(headers)
    if params:
        params = ast.literal_eval(params)
    
    if url:
        data.pop("url")
        try:
            response = requests.request(method, url, headers=headers, data=data, params=params)
            if response_type == "json":
                result = response.json()
            else:
                result = response.text
        except:
            return form_error_response(400, traceback.format_exc())
    else:
        return form_error_response(400, "url parameter do not received")

    result["status_code"] = 200
    
    return {
        "body": result
        }

def form_error_response(status_code: int, message: str):
    logger.error(message)
    response = {
        "body": {
            "status_code": status_code,
            "message": message
        }
    }
    return response

