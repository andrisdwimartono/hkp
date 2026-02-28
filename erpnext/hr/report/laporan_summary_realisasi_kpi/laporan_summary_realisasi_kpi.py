# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = [
		{
			"fieldname": "name",
			"label": "Realisasi KPI",
			"fieldtype": "Link",
			"options": "Realisasi KPI"
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Data"
		},
		{
			"fieldname": "date",
			"label": "Date",
			"fieldtype": "Date"
		},
		{
			"fieldname": "employee_name",
			"label": "Employee Name",
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "designation",
			"label": "Designation",
			"fieldtype": "Link",
			"options": "Designation"
		},
		{
			"fieldname": "total_final_score",
			"label": "Total Final Score",
			"fieldtype": "Float"
		},
		{
			"fieldname": "predicate",
			"label": "Predicate",
			"fieldtype": "Data"
		},
		{
			"fieldname": "predicate_label",
			"label": "Predicate Label",
			"fieldtype": "Data"
		}
	]
	data = get_data(filters)
	return columns, data

def get_data(filters=None):
	filter_query = "WHERE 1=1"
	if filters.get("employee"):
		filter_query += " AND rk.employee = '{0}'".format(filters.get('employee'))
	if filters.get("from_date") and filters.get("to_date"):
		filter_query += " AND rk.date BETWEEN '{0}' AND '{1}'".format(filters.get('from_date'), filters.get('to_date'))
	if filters.get("status"):
		filter_query += " AND rk.docstatus = {0}".format(1 if filters.get('status') == 'Submitted' else 0)
	data = frappe.db.sql("""
		SELECT
			rk.name,
			CASE WHEN rk.docstatus = 1 THEN 'Submitted' ELSE 'Draft' END AS status,
			rk.date,
			rk.employee_name,
			rk.designation,
			SUM(rkd.final_score) AS total_final_score
		FROM `tabRealisasi KPI Detail` rkd
		INNER JOIN `tabRealisasi KPI` rk ON rk.name = rkd.parent
		{0}
		GROUP BY rk.name, rk.date, rk.employee_name, rk.designation
	""".format(filter_query), as_dict=1)
	for d in data:
		if d.total_final_score > 92:
			d.predicate = "A"
			d.predicate_label = "ISTIMEWA"
		elif d.total_final_score > 84:
			d.predicate = "B"
			d.predicate_label = "BAIK"
		elif d.total_final_score > 76:
			d.predicate = "C"
			d.predicate_label = "CUKUP"
		elif d.total_final_score > 68:
			d.predicate = "D"
			d.predicate_label = "KURANG"
		else:
			d.predicate = "E"
			d.predicate_label = "MENGECEWAKAN"
	return data