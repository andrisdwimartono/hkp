# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters, columns)
	charts = get_chart_data(columns, data)
	return columns, data, None, charts

def get_columns(filters):
	# start_week = 1
	# if filters and filters.get("start_date") and filters.get("finish_date"):

	columns = [
		{
			"fieldname": "task",
			"label": _("Task"),
			"fieldtype": "Link",
			"options": "Task",
			"width": 100,
		},
		{
			"fieldname": "subject",
			"label": _("Subject"),
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"fieldname": "rencana",
			"label": _("Rencana"),
			"fieldtype": "Percent",
			"width": 100,
		},
		{
			"fieldname": "realisasi",
			"label": _("Realisasi"),
			"fieldtype": "Percent",
			"width": 100,
		},
		{
			"fieldname": "deviasi",
			"label": _("Deviasi"),
			"fieldtype": "Percent",
			"width": 100,
		},
	]

	return columns

def get_data(filters, columns):
	return frappe.db.sql("""
				SELECT 
					`tabTask`.name task,
					`tabTask`.subject,
					`tabTask Progress`.rencana,
					`tabTask Progress`.realisasi,
					`tabTask Progress`.deviasi
			    FROM `tabTask`
				INNER JOIN (
					  SELECT
					  	`tabTask Progress`.parent,
						max(`tabTask Progress`.tanggal) tanggal
					  FROM `tabTask Progress`
					  WHERE `tabTask Progress`.tanggal <= '{1}'
					  GROUP BY `tabTask Progress`.parent
					  ORDER BY `tabTask Progress`.tanggal DESC
					  ) as `tp1` ON `tp1`.parent = `tabTask`.name
				INNER JOIN `tabTask Progress` ON `tabTask Progress`.tanggal = tp1.tanggal AND `tabTask Progress`.parent = tp1.parent
					  WHERE `tabTask`.project = '{0}'""".format(filters.get("project"), filters.get("finish_date")), as_dict=1)

def get_chart_data(columns, data):
	labels = [d.subject for d in data]
	# datasets = [
	# 	{
	# 		"name": account.get("account").replace("'", ""),
	# 		"values": [account.get(d.get("fieldname")) for d in columns[2:]],
	# 	}
	# 	for account in data
	# 	if account.get("parent_account") == None and account.get("currency")
	# ]
	# datasets = datasets[:-1]
	datasets = []
	rencana = []
	realisasi = []
	deviasi = []
	for d in data:
		rencana.append(d.rencana)
		realisasi.append(d.realisasi)
		deviasi.append(d.deviasi)
	datasets.append({
		"name": "Rencana",
		"values": rencana
	})
	datasets.append({
		"name": "Realisasi",
		"values": realisasi
	})
	datasets.append({
		"name": "Deviasi",
		"values": deviasi
	})

	chart = {"data": {"labels": labels, "datasets": datasets}, "type": "bar", "colors":["#449CF0", "#29CD42", "#CB2929"],}

	return chart