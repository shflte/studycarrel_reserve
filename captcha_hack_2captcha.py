from dotenv import load_dotenv
import subprocess
import requests
import os
import time
import base64

def get_captcha_value():
    return input("captcha value: ")
    load_dotenv()

    api_key = os.getenv("2CAPTCHA_API_KEY")
    url = "https://api.2captcha.com/"
    create_task_endpoint = url + "createTask"
    get_task_result_endpoint = url + "getTaskResult"

    create_payload = {
        "clientKey": api_key,
        "task": {
            "type": "ImageToTextTask",
            "body": "",
            "phrase": False,
            "case": True,
            "numeric": 1,
            "math": False,
            "minLength": 4,
            "maxLength": 4,
        },
        "languagePool": "en"
    }
    get_payload = {
    "clientKey": api_key, 
    "taskId": 0
    }

    '''
    response example
    createTask:
    {
        "errorId": 0,
        "taskId": 72345678901
    }
    getTaskResult:
    {
        "errorId": 0,
        "status": "ready",
        "solution": {
            "text": "hello world"
        },
        "cost": "0.00025",
        "ip": "1.2.3.4",
        "createTime": 1692808229,
        "endTime": 1692808326,
        "solveCount": 1
    }
    '''

    headers = {
        "Content-Type": "application/json"
    }

    # load captcha image and encode it into base64
    captcha_path = "captcha.png"
    with open(captcha_path, "rb") as f:
        captcha_image = f.read()
        captcha_image_encoded = base64.b64encode(captcha_image).decode("utf-8")
        create_payload["task"]["body"] = captcha_image_encoded
    create_response = requests.post(create_task_endpoint, json=create_payload, headers=headers)

    # check if create task is successful
    if create_response.status_code != 200 :
        raise Exception(f"create task failed: {create_response.json()}")
    create_response_json = create_response.json()
    if create_response_json["errorId"] != 0:
        raise Exception(f"create task failed: {create_response_json}")

    # get task id
    task_id = create_response_json["taskId"]

    # get task result
    get_payload["taskId"] = task_id
    while True:
        get_response = requests.post(get_task_result_endpoint, json=get_payload, headers=headers)
        # check if get task result is successful
        if get_response.status_code != 200 :
            raise Exception(f"get task result failed: {get_response.json()}")
        get_response_json = get_response.json()
        print(get_response_json)

        # check if get task result is successful
        if get_response_json["errorId"] != 0:
            raise Exception(f"get task result failed: {get_response_json}")

        # check if task is ready
        if get_response_json["status"] == "ready":
            break
        else:
            print("task not ready, wait for 1 second")
            time.sleep(1)

    # get captcha value
    captcha_value = get_response_json["solution"]["text"]

    return captcha_value
