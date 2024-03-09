from flask import flash

def form_errors_normalize_response(form, data={}):
    for field in data["data"]["form_errors"].keys(): form[field].errors = data["data"]["form_errors"][field]
    return form

def form_data_normalize(form, data=None):
    if data:
        for field in data.keys():
            if field in form: form[field].data = data[field]
    return form

def launch_flash_response(data={}):
    if data["message"]: flash(data['message'], "success" if data["success"] else "error")