# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters, columns)
	#return columns, data
	charts = get_chart_data(columns, data)
	return columns, data, None, charts

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

	from datetime import date, timedelta

	start_date = datetime.strptime(filters.get("from_date"), "%Y-%m-%d")
	end_date = datetime.strptime(filters.get("finish_date"), "%Y-%m-%d")
	delta = timedelta(days=1)
	weeknum = 0
	dt = []
	while start_date <= end_date:
		if weeknum != check_week(posting_date=start_date.strftime("%Y-%m-%d")):
			weeknum = check_week(posting_date=start_date.strftime("%Y-%m-%d"))
			if len(dt) > 0:
				dt[len(dt)-1]["end_week"] = (start_date + timedelta(days=-1)).strftime('%Y-%m-%d')
				dt[len(dt)-1]["label"] = "{0} | {1} s/d {2}".format(dt[len(dt)-1].get("week_periode"), datetime.strptime(dt[len(dt)-1].get("start_week"), "%Y-%m-%d").strftime('%d/%m/%Y'), (start_date + timedelta(days=-1)).strftime('%d/%m/%Y'))
			dt.append({
				"week_periode": weeknum,
				"start_week": start_date.strftime('%Y-%m-%d'),
				#"end_week": last_date.strftime('%Y-%m-%d'),
				"fieldname": weeknum,
				#"label": "{0} | {1} s/d {2}".format(weeknum, start_date.strftime('%d/%m/%Y'), last_date.strftime('%d/%m/%Y')),
				"fieldtype": "Percent",
				"width": 300,
			})
		start_date += delta
		if start_date == end_date:
			dt[len(dt)-1]["end_week"] = (start_date + timedelta(days=-1)).strftime('%Y-%m-%d')
			dt[len(dt)-1]["label"] = "{0} | {1} s/d {2}".format(dt[len(dt)-1].get("week_periode"), datetime.strptime(dt[len(dt)-1].get("start_week"), "%Y-%m-%d").strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
	columns = columns+dt
	return columns

def get_data(filters, columns):
	data = [
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
	for d in columns:
		x = frappe.db.sql("""
			SELECT 
				SUM(COALESCE(`tabTask Progress`.rencana*`tabTask`.task_weight/100, 0)) rencana,
				SUM(COALESCE(`tabTask Progress`.realisasi*`tabTask`.task_weight/100, 0)) realisasi,
				SUM(COALESCE(`tabTask Progress`.deviasi*`tabTask`.task_weight/100, 0)) deviasi 
			FROM `tabTask`
			INNER JOIN `tabTask Progress` ON `tabTask Progress`.tanggal BETWEEN '{1}' AND '{2}' AND `tabTask Progress`.parent = `tabTask`.name
			WHERE `tabTask`.project = '{0}'
		""".format(filters.get("project"), d.get("start_week"), d.get("end_week")), as_dict=1)
		if x:
			data[0][d.get("fieldname")] = x[0].rencana
			data[1][d.get("fieldname")] = x[0].realisasi
			data[2][d.get("fieldname")] = x[0].deviasi
		else:
			data[0][d.get("fieldname")] = 0
			data[1][d.get("fieldname")] = 0
			data[2][d.get("fieldname")] = 0
	data[0]["subject"] = "Rencana"
	data[1]["subject"] = "Realisasi"
	data[2]["subject"] = "Deviasi"
	return data

def get_chart_data(columns, data):
	labels = []
	datasets = []
	rencana = []
	realisasi = []
	deviasi = []
	for d in columns[1:]:
		labels.append(d.get("week_periode"))
		rencana.append(data[0][d.get("week_periode")])
		realisasi.append(data[1][d.get("week_periode")])
		deviasi.append(data[2][d.get("week_periode")])
	# datasets = [
	# 	{
	# 		"name": account.get("account").replace("'", ""),
	# 		"values": [account.get(d.get("fieldname")) for d in columns[2:]],
	# 	}
	# 	for account in data
	# 	if account.get("parent_account") == None and account.get("currency")
	# ]
	# datasets = datasets[:-1]
	
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

	chart = {"data": {"labels": labels, "datasets": datasets}, "type": "line", "colors":["#449CF0", "#29CD42", "#CB2929"],}

	return chart

def check_week(posting_date = None):
	d1 = datetime.strptime("{0}-01-01".format(datetime.strptime(posting_date, "%Y-%m-%d").year), "%Y-%m-%d")
	d2 = datetime.strptime(posting_date, "%Y-%m-%d")
	monday1 = (d1 - timedelta(days=d1.weekday()))
	monday2 = (d2 - timedelta(days=d2.weekday()))
	
	week = (monday2 - monday1).days / 7
	return int(week)

def check_day(posting_date = None):
	d2 = datetime.strptime(posting_date, "%Y-%m-%d")

	return d2.weekday()