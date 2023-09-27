import json
import requests
import frappe

def get_token():
    url = "http://192.168.18.250:8091/jwt-api-token-auth/"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "username": "hasta.subag",
        "password": "hast@hkp123321"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response:
        resp = response.json()
        if resp:
            return resp
    return response.json()

def get_all_department(token):
    try:
        url = "http://192.168.18.250:8091/personnel/api/departments/?page_size=20"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {0}".format(token["token"])
        }

        response = requests.get(url, headers=headers)
        if response:
            resp = response.json()
            if resp:
                return resp
    except AttributeError:
        frappe.throw("""Token error""")

def get_transaction(start_date=None, end_date=None):
    if start_date == None or end_date == None:
        frappe.throw("Waktu Mulai dan Selesai harus diisi")
    token = get_token()
    try:
        departments = get_all_department(token)
        alldata = []
        for dept in departments["data"]:
            url = "http://192.168.18.250:8091/att/api/transactionReport/?start_date="+start_date+"&end_date="+end_date+"&departments="+str(dept["id"])
            headers = {
                "Content-Type": "application/json",
                "Authorization": "JWT {0}".format(token["token"])
            }
            response = requests.get(url, headers=headers)
            if response:
                resp = response.json()
                if resp:
                    alldata = alldata+resp["data"]
        return alldata
    except AttributeError:
        frappe.throw("""Token error""")