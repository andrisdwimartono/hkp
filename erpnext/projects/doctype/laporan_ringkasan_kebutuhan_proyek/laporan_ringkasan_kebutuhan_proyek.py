# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	add_days,
)

class LaporanRingkasanKebutuhanProyek(Document):
	pass

@frappe.whitelist()
def get_rekap(project, start_date, finish_date):
	x = add_days(start_date, -14)
	y = add_days(finish_date, -14)
	return frappe.db.sql("""
		SELECT
			a.project,
			a.project_name,
			a.purpose,
			a.posting_date,
			a.total_budget_first,
			a.submitted_date,
			a.total_budget,
			b.posting_date tanggal_terbayar,
			b.paid_amount,
			je.realisasi,
			je.tanggal_realisasi,
			a.keterangan
			FROM `tabForm Payment Entry Project` a
		LEFT JOIN `tabPayment Entry` b ON b.type = 'Form Payment Entry Project' AND a.name = b.form_payment_entry_project
		LEFT JOIN (
					SELECT je.form_payment_entry_project, SUM(COALESCE(jea.debit_in_account_currency, jea.debit)) realisasi, je.posting_date tanggal_realisasi FROM `tabJournal Entry` je
					INNER JOIN `tabJournal Entry Account` jea ON jea.parent = je.name
					INNER JOIN `tabAccount` a ON a.name = jea.account
					WHERE a.root_type = 'Expense' AND (jea.debit_in_account_currency != 0 or jea.debit != 0)
					GROUP BY je.form_payment_entry_project
		) je ON je.form_payment_entry_project = a.name
		WHERE a.project = '{0}' AND a.posting_date BETWEEN '{1}' AND '{2}';
	""".format(project, x, y), as_dict=1)

@frappe.whitelist()
def get_rekap_material(project, start_date, finish_date):
	aa = frappe.db.sql("""
				SELECT a.name FROM `tabLaporan Ringkasan Kebutuhan Proyek` a
					WHERE a.project = '{0}' AND a.finish_date < '{1}'
					ORDER BY a.start_date DESC
					LIMIT 1
	""".format(project, start_date), as_dict=1)
	
	if aa:
		return frappe.db.sql("""
			SELECT
				uraian_material,
				uom,
				rencana,
				keterangan
			FROM `tabLaporan Ringkasan Kebutuhan Proyek Rencana` b
			WHERE b.parent = '{0}';
		""".format(aa[0].name), as_dict=1)