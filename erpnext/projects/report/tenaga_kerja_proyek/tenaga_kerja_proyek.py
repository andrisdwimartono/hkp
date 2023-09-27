# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_column(columns)
	data = get_data(columns, data)
	return columns, data

def get_column(columns):
	xx = frappe.db.sql("""SELECT name, project_name FROM tabProject ORDER BY name ASC""", as_dict=1)
	if xx:
		columns.append({
			"fieldname": "designation",
			"label": "Jabatan",
			"fieldtype": "Link",
			"options": "Designation"
		})
	for x in xx:
		columns.append({
			"fieldname": x.name,
			"label": x.project_name,
			"fieldtype": "Data"
		})
	return columns

def get_data(columns, data):
	dess = frappe.db.sql("""SELECT DISTINCT designation FROM `tabProject Team` pt ORDER BY designation ASC""", as_dict=1)
	for des in dess:
		dt = {
			"designation": des.designation
		}
		for col in columns:
			emp = frappe.db.sql("""SELECT employee_name FROM `tabProject Team` pt WHERE parent = '{0}' AND designation = '{1}' ORDER BY designation ASC""".format(col["fieldname"], des.designation), as_dict=1)
			if emp:
				dt[col["fieldname"]] = emp[0].employee_name
		data.append(dt)
	return data