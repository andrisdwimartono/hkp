# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class RekapitulasiAnggaranProyek(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.posting_date, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabRekapitulasi Anggaran Proyek` WHERE name like '%/{2}/{0}/{1}'""".format(bulan, mydate.year, self.project), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "REKAP/{2}/{3}/{0}/{1}".format(bulan, mydate.year, urut2, self.project)
		else:
			self.name = "REKAP/001/{2}/{0}/{1}".format(bulan, mydate.year, self.project)


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
	""".format(project, start_date, finish_date), as_dict=1)