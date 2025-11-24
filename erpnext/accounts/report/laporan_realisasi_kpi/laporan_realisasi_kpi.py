# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_data(filters):
	conditions = ""
	if filters.get("employee"):
		conditions += f" AND kpi.employee = '{filters.get('employee')}'"
	if filters.get("from_date"):
		conditions += f" AND kpi.date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" AND kpi.date <= '{filters.get('to_date')}'"
	if filters.get("status"):
		if filters.get("status") == "Draft":
			conditions += " AND kpi.docstatus = 0"
		elif filters.get("status") == "Submitted":
			conditions += " AND kpi.docstatus = 1"
		elif filters.get("status") == "Cancelled":
			conditions += " AND kpi.docstatus = 2"

	query = f"""
		SELECT
			kpi.employee,
			emp.employee_name,
			kpi.date,
			emp.department,
			emp.designation,
			CASE WHEN kpi.docstatus = '0' THEN 'Draft'
				 WHEN kpi.docstatus = '1' THEN 'Submitted'
				 WHEN kpi.docstatus = '2' THEN 'Cancelled'
			END AS status,
			kpi_detail.kpi,
			kpi_detail.description,
			kpi_detail.aktivitas_pekerjaan,
			kpi_detail.weight,
			kpi_detail.target,
			kpi_detail.actual,
			kpi_detail.achievement,
			kpi_detail.score,
			kpi_detail.final_score
		FROM
			`tabRealisasi KPI` kpi
		INNER JOIN
			`tabEmployee` emp ON kpi.employee = emp.name
		INNER JOIN
			`tabRealisasi KPI Detail` kpi_detail ON kpi.name = kpi_detail.parent
		WHERE
			kpi.docstatus IN (0, 1)
			{conditions}
		ORDER BY
			kpi.date DESC, kpi.employee ASC, kpi_detail.idx ASC
	"""

	return frappe.db.sql(query, as_dict=1)

def get_columns():
	columns = [
		{
			"fieldname": "employee",
			"label": "Employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 250
		},
		{
			"fieldname": "employee_name",
			"label": "Employee Name",
			"fieldtype": "Data",
			"width": 250
		},
		# {
		# 	"fieldname": "employee_name",
		# 	"label": "Employee Name",
		# 	"fieldtype": "Data",
		# 	"width": 150
		# },
		{
			"fieldname": "date",
			"label": "Date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "department",
			"label": "Department",
			"fieldtype": "Link",
			"options": "Department",
			"width": 150
		},
		{
			"fieldname": "designation",
			"label": "Designation",
			"fieldtype": "Link",
			"options": "Designation",
			"width": 150
		},
		{
			"fieldname": "aktivitas_pekerjaan",
			"label": "Aktivitas Pekerjaan",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "kpi",
			"label": "KPI",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "description",
			"label": "Result",
			"fieldtype": "Data",
			"width": 250
		},
		{
			"fieldname": "target",
			"label": "Target",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "weight",
			"label": "Weight",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "actual",
			"label": "Actual",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "achievement",
			"label": "Achievement",
			"fieldtype": "Percent",
			"width": 80
		},
		{
			"fieldname": "score",
			"label": "Score",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "final_score",
			"label": "Final Score",
			"fieldtype": "Float",
			"width": 120
		}
	]
	return columns
