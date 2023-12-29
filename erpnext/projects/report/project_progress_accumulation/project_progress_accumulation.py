# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters, columns)
	return columns, data
	# charts = get_chart_data(columns, data)
	# return columns, data, None, charts

def get_columns(filters):
	columns = [
		# {
		# 	"fieldname": "task",
		# 	"label": _("Task"),
		# 	"fieldtype": "Link",
		# 	"options": "Task",
		# 	"width": 100,
		# },
		{
			"fieldname": "subject",
			"label": _("Subject"),
			"fieldtype": "Data",
			"width": 300,
		},
	]

	from_week = check_week(posting_date=filters.get("from_date"))
	finish_week = check_week(posting_date=filters.get("finish_date"))

	from_day = check_day(posting_date=filters.get("from_date"))
	from_last_day = datetime.strptime(filters.get("from_date"), "%Y-%m-%d") + timedelta(days=(6-from_day))

	columns.append({
		"week_periode": from_week,
		"start_week": datetime.strptime(filters.get("from_date"), "%Y-%m-%d").strftime('%d/%m/%Y'),
		"end_week": from_last_day.strftime('%d/%m/%Y'),
		"fieldname": from_week,
		"label": "{0} | {1} s/d {2}".format(from_week, datetime.strptime(filters.get("from_date"), "%Y-%m-%d").strftime('%d/%m/%Y'), from_last_day.strftime('%d/%m/%Y')),
		"fieldtype": "Percent",
		"width": 300,
	})
	for n in range((finish_week)-(from_week+1)):
		columns.append({
			"week_periode": n+from_week+1,
			"start_week": (from_last_day + timedelta(days=((n*7)+1))).strftime('%d/%m/%Y'),
			"end_week": (from_last_day + timedelta(days=((n*7)+7))).strftime('%d/%m/%Y'),
			"fieldname": n+from_week+1,
			"label": "{0} | {1} s/d {2}".format(n+from_week+1, (from_last_day + timedelta(days=((n*7)+1))).strftime('%d/%m/%Y'), (from_last_day + timedelta(days=((n*7)+7))).strftime('%d/%m/%Y')),
			"fieldtype": "Percent",
			"width": 300,
		})
	columns.append({
		"week_periode": finish_week,
		"start_week": (from_last_day + timedelta(days=((((finish_week)-(from_week+1))*7)+1))).strftime('%d/%m/%Y'),
		"end_week": datetime.strptime(filters.get("finish_date"), "%Y-%m-%d").strftime('%d/%m/%Y'),
		"fieldname": finish_week,
		"label": "{0} | {1} s/d {2}".format(finish_week, (from_last_day + timedelta(days=((((finish_week)-(from_week+1))*7)+1))).strftime('%d/%m/%Y'), datetime.strptime(filters.get("finish_date"), "%Y-%m-%d").strftime('%d/%m/%Y')),
		"fieldtype": "Percent",
		"width": 300,
	})

	return columns

def get_data(filters, columns):
	return [
		{
			"subject": "Rencana"
		},
		{
			"subject": "Realisasi"
		},
		{
			"subject": "Deviasi"
		},
		]

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

def check_week(posting_date = None):
	d1 = datetime.strptime("{0}-01-01".format(datetime.now().year), "%Y-%m-%d")
	d2 = datetime.strptime(posting_date, "%Y-%m-%d")
	monday1 = (d1 - timedelta(days=d1.weekday()))
	monday2 = (d2 - timedelta(days=d2.weekday()))
	
	week = (monday2 - monday1).days / 7
	return int(week)

def check_day(posting_date = None):
	d2 = datetime.strptime(posting_date, "%Y-%m-%d")

	return d2.weekday()