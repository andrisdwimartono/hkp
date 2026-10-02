# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "name",
			"label": "Name",
			"fieldtype": "Link",
			"options": "Daily K3",
			"width": 100,
		},
		{
			"fieldname": "date",
			"label": "Date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"fieldname": "payout_date",
			"label": "Payout Date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"fieldname": "customer",
			"label": "Customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 100,
		},
		{
			"fieldname": "project",
			"label": "Project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 100,
		},
		{
			"fieldname": "project_name",
			"label": "Project Name",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "project_address",
			"label": "Project Address",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "weather",
			"label": "Weather",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "man_power",
			"label": "Man Power",
			"fieldtype": "Integer",
			"width": 100,
		},
		{
			"fieldname": "executor",
			"label": "Executor",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "activities",
			"label": "Activities",
			"fieldtype": "Text",
			"width": 400,
		},
		{
			"fieldname": "result",
			"label": "Result",
			"fieldtype": "Text",
			"width": 400,
		},
		{
			"fieldname": "checklist_k3",
			"label": "Checklist K3 (%)",
			"fieldtype": "Percent",
			"width": 100,
		},
    ]
		
def get_data(filters):
	return frappe.db.sql("""
		SELECT
			`tabDaily K3`.*,
			`tabProject`.customer,
			`tabProject`.project_address,
			`tabCustomer`.image,
			(
				CASE WHEN `tabDaily K3`.body_harness THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.pelindung_mata THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.masker THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.respirator THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.kedok_las THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.helm_safety THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.earmuff_earplug THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.sarung_tangan THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.sepatu_safety THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.sabuk_pengaman THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.pelampung THEN 1 ELSE 0 END +
				CASE WHEN `tabDaily K3`.wearpack THEN 1 ELSE 0 END ) * 100.0 / 12 AS checklist_k3
		FROM `tabDaily K3`
		LEFT JOIN `tabProject` ON `tabDaily K3`.project = `tabProject`.name
		LEFT JOIN `tabCustomer` ON `tabProject`.customer = `tabCustomer`.name
		WHERE `tabDaily K3`.project = %s
		AND `tabDaily K3`.date BETWEEN %s AND %s
		ORDER BY `tabDaily K3`.date ASC
	""", (filters.get("project"), filters.get("from_date"), filters.get("to_date")), as_dict=1)


	
    