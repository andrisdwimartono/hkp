# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_data(filters):
	data = frappe.db.sql("""
		SELECT
			tba.pos_rap,
			tba.budget_amount,
			COALESCE(realization.budget_realization, 0) AS budget_realization,
			COALESCE(tba.budget_amount, 0)-COALESCE(realization.budget_realization, 0) AS budget_deviation
		FROM `tabBudget` tb
		LEFT JOIN `tabBudget Account` tba ON tb.name = tba.parent and tba.parenttype = 'Budget'
		LEFT JOIN (
			SELECT
				tjea.budget,
				tjea.pos_rap,
				SUM(tjea.debit - tjea.credit) AS budget_realization
			FROM `tabJournal Entry Account` tjea
			INNER JOIN `tabJournal Entry` tje ON tje.name = tjea.parent
			WHERE tje.docstatus = 1
			GROUP BY tjea.budget, tjea.pos_rap
		) realization ON realization.budget = tba.parent AND realization.pos_rap = tba.pos_rap
		WHERE tb.name = '{0}'
		ORDER BY tba.pos_rap ASC
		""".format(filters.get("budget")),  as_dict=1)
	return data

def get_columns():
	columns = [
		{
			"fieldname": "pos_rap",
			"label": "Uraian",
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"fieldname": "budget_amount",
			"label": "Anggaran",
			"fieldtype": "Currency",
			"width": 225,
		},
		{
			"fieldname": "budget_realization",
			"label": "Realisasi",
			"fieldtype": "Currency",
			"width": 225,
		},
		{
			"fieldname": "budget_deviation",
			"label": "Deviasi",
			"fieldtype": "Currency",
			"width": 225,
		},
	]
	return columns