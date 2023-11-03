# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RekapitulasiAnggaranProyek(Document):
	pass

@frappe.whitelist()
def get_rekap(project, start_date, finish_date):
	return frappe.db.sql("""
		SELECT
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
		WHERE a.project = '{0}' AND a.posting_date BETWEEN '{1}' AND '{2}';
	""".format(project, start_date, finish_date), as_dict=1)