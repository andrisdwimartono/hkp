# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns =[
		# {
		# 	"fieldname": "name",
		# 	"label": "Budget",
		# 	"fieldtype": "Link",
		# 	"options": "Budget",
		# 	"width": 140
		# },
		# {
		# 	"fieldname": "project",
		# 	"label": "Project",
		# 	"fieldtype": "Link",
		# 	"options": "Project",
		# 	"width": 140
		# },
		# {
		# 	"fieldname": "group",
		# 	"label": "Group",
		# 	"fieldtype": "Data",
		# 	# "hidden": 1,
		# 	"width": 140
		# },
		# {
		# 	"fieldname": "parent_budget_account",
		# 	"label": "Parent Budget Account",
		# 	"fieldtype": "Link",
		# 	"options": "Budget Account",
		# 	"width": 140
		# },
		{
			"fieldname": "nomor",
			"label": "Nomor",
			"fieldtype": "Data",
			"width": 140
		},
		{
			"fieldname": "pos_rap",
			"label": "POS RAP",
			"fieldtype": "Link",
			"options": "POS RAP",
			"width": 140
		},
		{
			"fieldname": "budget_amount",
			"label": "Rencana",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "total_paid_amount",
			"label": "Tanda Terima",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "total_amount",
			"label": "Jurnal",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "total_realisasi",
			"label": "Realisasi",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"fieldname": "sisa",
			"label": "Sisa",
			"fieldtype": "Currency",
			"width": 140
		}
	]
	data = get_data(filters)
	return columns, data


def get_data(filters=None):
	date_to_pe = ""
	date_to_je = ""
	if filters.get('date_to'):
		date_to_pe = "AND pe.posting_date <= '{0}'".format(filters.get('date_to'))
		date_to_je = "AND je.posting_date <= '{0}'".format(filters.get('date_to'))
	rawData = frappe.db.sql("""
		SELECT
			b.name,
			b.project,
			ba.group,
			ba.parent_budget_account,
			ba.nomor,
			ba.pos_rap,
			ba.budget_amount,
			COALESCE(pe.total_paid_amount, 0) AS total_paid_amount,
			COALESCE(je.total_amount, 0) AS total_amount,
			COALESCE(pe.total_paid_amount, 0) + COALESCE(je.total_amount, 0) AS total_realisasi,
			ba.budget_amount - (COALESCE(pe.total_paid_amount, 0) + COALESCE(je.total_amount, 0)) sisa
		FROM `tabBudget` b
		INNER JOIN `tabBudget Account` ba ON ba.parent = b.name
		LEFT JOIN (
			SELECT
				pe.budget,
				pe.pos_rap,
				SUM(pe.paid_amount) AS total_paid_amount
			FROM `tabPayment Entry` pe
			WHERE pe.docstatus = 1 AND pe.budget IS NOT NULL AND pe.pos_rap IS NOT NULL {1}
			GROUP BY pe.budget, pe.pos_rap
		) pe ON pe.budget = b.name AND ba.pos_rap = pe.pos_rap
		LEFT JOIN (
			SELECT
				jea.budget,
				jea.pos_rap,
				SUM(COALESCE(jea.debit, 0) - COALESCE(jea.credit, 0)) total_amount
			FROM `tabJournal Entry` je
			INNER JOIN `tabJournal Entry Account` jea ON jea.parent = je.name AND jea.parenttype = 'Journal Entry'
			WHERE je.docstatus = 1 AND jea.budget IS NOT NULL AND jea.pos_rap IS NOT NULL {2}
			GROUP BY jea.budget, jea.pos_rap
		) je ON je.budget = b.name AND ba.pos_rap = je.pos_rap
		WHERE b.name = '{0}'
		ORDER BY b.name, ba.idx, ba.nomor""".format(filters.get('budget'), date_to_pe, date_to_je), as_dict=True)
	
	return rawData