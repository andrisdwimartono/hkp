import frappe

def before_request():
    pass

def after_request(response):
    # pass
    # response.headers["Access-Control-Allow-Origin"] = "http://172.18.130.89:5173"
    # response.headers["Access-Control-Allow-Credentials"] = "true"
    # response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    # response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response