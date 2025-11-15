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
			COALESCE(acceptance.budget_acceptance, 0) AS budget_acceptance,
			0 AS budget_realization,
			COALESCE(acceptance.budget_acceptance, 0)-0 AS budget_deviation
		FROM `tabBudget` tb
		LEFT JOIN `tabBudget Account` tba ON tb.name = tba.parent and tba.parenttype = 'Budget'
		LEFT JOIN (
			SELECT
				acceptance_data.budget,
				acceptance_data.pos_rap,
				SUM(acceptance_data.budget_acceptance) AS budget_acceptance
			FROM (
				SELECT
					sps.budget,
					fpea.pos_rap,
					SUM(fpea.budget_amount) AS budget_acceptance,
					'Slip Pembayaran Subkon' AS acceptance_type
				FROM `tabForm Payment Entry Account` fpea
				INNER JOIN `tabSlip Pembayaran Subkon` sps ON sps.name = fpea.parent
				WHERE fpea.docstatus = 1 AND fpea.parenttype = 'Slip Pembayaran Subkon'
				GROUP BY sps.budget, fpea.pos_rap
				UNION
				SELECT
					fpes.budget,
					fpea.pos_rap,
					SUM(fpea.budget_amount) AS budget_acceptance,
					'Form Payment Entry Supplier' AS acceptance_type
				FROM `tabForm Payment Entry Account` fpea
				INNER JOIN `tabForm Payment Entry Supplier` fpes ON fpes.name = fpea.parent
				WHERE fpea.docstatus = 1 AND fpea.parenttype = 'Form Payment Entry Supplier'
				GROUP BY fpes.budget, fpea.pos_rap
				UNION
				SELECT
					fpep.budget,
					fpea.pos_rap,
					SUM(fpea.budget_amount) AS budget_acceptance,
					'Form Payment Entry Project' AS acceptance_type
				FROM `tabForm Payment Entry Account` fpea
				INNER JOIN `tabForm Payment Entry Project` fpep ON fpep.name = fpea.parent
				WHERE fpea.docstatus = 1 AND fpea.parenttype = 'Form Payment Entry Project'
				GROUP BY fpep.budget, fpea.pos_rap
				) AS acceptance_data
			GROUP BY acceptance_data.budget, acceptance_data.pos_rap
		) acceptance ON acceptance.pos_rap = tba.pos_rap AND acceptance.budget = tb.name
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
			"fieldname": "budget_acceptance",
			"label": "Disetujui",
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