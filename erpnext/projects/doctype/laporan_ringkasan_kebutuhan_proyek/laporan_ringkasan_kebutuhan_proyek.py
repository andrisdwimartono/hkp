# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	today,
)
import datetime

class LaporanRingkasanKebutuhanProyek(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabLaporan Ringkasan Kebutuhan Proyek` WHERE name like '%/{3}/{2}/{0}/{1}'""".format(bulan, mydate.year, self.project, self.week_periode), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "LKP/{2}/{4}/{3}/{0}/{1}".format(bulan, mydate.year, urut2, self.project, self.week_periode)
		else:
			self.name = "LKP/001/{3}/{2}/{0}/{1}".format(bulan, mydate.year, self.project, self.week_periode)

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

@frappe.whitelist()
def get_rekap_materi(project, start_date, finish_date):
#def get_rekap_materi():
	# project = "22-448"
	# start_date = "2023-01-01"
	# finish_date = "2023-11-30"
	x = add_days(start_date, -14)
	y = add_days(finish_date, -14)
	return frappe.db.sql("""
		SELECT
			concat_ws(" ", sle.posting_date, sle.posting_time) AS date,
			sle.item_code,
			i.item_name uraian_material,
			sle.stock_uom uom,
			sle.warehouse keterangan,
			coalesce(b.rencana, 0) rencana,
			sle.actual_qty,
			sle.qty_after_transaction realisasi,
			sle.incoming_rate,
			sle.valuation_rate,
			sle.stock_value,
			sle.voucher_type,
			sle.voucher_no,
			sle.batch_no,
			sle.serial_no,
			sle.company,
			sle.project,
			sle.project_name,
			sle.stock_value_difference
		FROM
			`tabStock Ledger Entry` sle
		INNER JOIN `tabItem` i ON sle.item_code = i.name
		LEFT JOIN (
					SELECT a.name, a.project FROM `tabLaporan Ringkasan Kebutuhan Proyek` a
					WHERE a.project = '{0}' AND a.finish_date < '{1}'
					ORDER BY a.start_date DESC
					LIMIT 1 
		) a ON a.project = sle.project
		LEFT JOIN `tabLaporan Ringkasan Kebutuhan Proyek Rencana` b ON b.parent = a.name AND b.uraian_material = i.item_name
		WHERE 
			sle.is_cancelled = 0 AND sle.posting_date BETWEEN '{1}' AND '{2}' AND sle.project = '{0}'
	""".format(project, x, y), as_dict=1)