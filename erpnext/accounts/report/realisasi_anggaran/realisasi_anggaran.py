# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	return frappe.db.sql(
		"""
		SELECT
			'KAS BON PROYEK' type,
			reap.form_payment_entry_project AS kas_bon,
			reap.purpose,
			COALESCE(fpear.total_budget_realization, 0) AS total_budget_realization,
			COALESCE(fpep.total_budget, 0) AS total_budget_plan,
			COALESCE(fpear.total_budget_realization, 0)-COALESCE(fpep.total_budget, 0) AS total_budget_difference
		FROM `tabRealisasi Anggaran Proyek` reap
		LEFT JOIN (
			SELECT fpear.parent, SUM(fpear.budget_realization) total_budget_realization FROM `tabForm Payment Entry Account Realisasi` fpear
			GROUP BY fpear.parent
		) fpear ON fpear.parent = reap.name
		LEFT JOIN `tabForm Payment Entry Project` fpep ON fpep.name = reap.form_payment_entry_project
		WHERE reap.posting_date BETWEEN '{0}' AND '{1}' AND reap.docstatus = 1
		UNION
		SELECT
			'KAS BON NON PROYEK' type,
			reanp.form_payment_entry AS kas_bon,
			reanp.purpose,
			COALESCE(fpear.total_budget_realization, 0) AS total_budget_realization,
			COALESCE(fpep.total_budget, 0) AS total_budget_plan,
			COALESCE(fpear.total_budget_realization, 0)-COALESCE(fpep.total_budget, 0) AS total_budget_difference
		FROM `tabRealisasi Anggaran Non Proyek` reanp
		LEFT JOIN (
			SELECT fpear.parent, SUM(fpear.budget_realization) total_budget_realization FROM `tabForm Payment Entry Non Project Realisasi` fpear
			GROUP BY fpear.parent
		) fpear ON fpear.parent = reanp.name
		LEFT JOIN `tabForm Payment Entry` fpep ON fpep.name = reanp.form_payment_entry
		WHERE reanp.posting_date BETWEEN '{0}' AND '{1}' AND reanp.docstatus = 1
		""".format(filters.date_from, filters.date_to), as_dict=1)

def get_columns(filters):
	columns = [
		{
			"label": _("Tipe"),
			"fieldname": "type",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Kas Bon"),
			"fieldname": "kas_bon",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": _("Tujuan"),
			"fieldname": "purpose",
			"fieldtype": "Data",
			"width": 320,
		},
		{
			"label": _("Rencana"),
			"fieldname": "total_budget_plan",
			"fieldtype": "Float",
			"width": 160,
		},
		{
			"label": _("Realisasi"),
			"fieldname": "total_budget_realization",
			"fieldtype": "Float",
			"width": 160,
		},
		{
			"label": _("Selisih"),
			"fieldname": "total_budget_difference",
			"fieldtype": "Float",
			"width": 140,
		},
	]

	return columns
