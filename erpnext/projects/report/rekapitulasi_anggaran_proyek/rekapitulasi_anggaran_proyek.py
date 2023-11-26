# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "project",
			"label": _("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 100,
		},
		{
			"fieldname": "project_name",
			"label": _("Project Name"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "purpose",
			"label": _("Uraian"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "posting_date",
			"label": _("Tanggal Pengajuan"),
			"fieldtype": "Date",
			"width": 80,
		},
		{
			"fieldname": "total_budget_first",
			"label": _("Pengajuan (Rp)"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "submitted_date",
			"label": _("Tanggal Disetujui"),
			"fieldtype": "Date",
			"width": 80,
		},
		{
			"fieldname": "total_budget",
			"label": _("Disetujui (Rp)"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "tanggal_realisasi",
			"label": _("Tanggal Realisasi"),
			"fieldtype": "Date",
			"width": 80,
		},
		{
			"fieldname": "paid_amount",
			"label": _("Realisasi (Rp)"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "keterangan",
			"label": _("Keterangan"),
			"fieldtype": "Data",
			"width": 150,
		}
	]

def get_data(filters=None):
	where = ""
	if filters:
		if filters.project and filters.purpose:
			where = """WHERE a.project = '{0}' AND a.purpose LIKE '%{1}%'""".format(filters.project, filters.purpose)
		if filters.project and not filters.purpose:
			where = """WHERE a.project = '{0}'""".format(filters.project)
		if not filters.project and filters.purpose:
			where = """WHERE a.purpose LIKE '%{0}%'""".format(filters.purpose)
	return frappe.db.sql(
		"""SELECT
			a.project,
			a.project_name,
			a.purpose,
			a.posting_date,
			a.total_budget_first,
			a.submitted_date,
			a.total_budget,
			b.posting_date tanggal_realisasi,
			b.paid_amount,
			a.keterangan 
			FROM `tabForm Payment Entry Project` a
		LEFT JOIN `tabPayment Entry` b ON b.type = 'Form Payment Entry Project' AND a.name = b.form_payment_entry_project
		{0}""".format(where),
		as_dict=1,
	)