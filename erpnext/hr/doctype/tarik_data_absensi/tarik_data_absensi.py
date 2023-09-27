# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.hr.apifacerecognition import get_transaction

class TarikDataAbsensi(Document):
	def validate(self):
		if len(self.ringkasan_absensi_karyawan) <= 0:
			for e in frappe.db.sql("""SELECT * FROM `tabEmployee` e""", as_dict=1):
				self.append("ringkasan_absensi_karyawan", {
					"employee": e.name,
					"employee_name": e.employee_name,
					"emp_code": e.emp_code
				})
		if self.start_date and self.end_date and len(self.ringkasan_absensi_karyawan) > 0:
			for d in self.ringkasan_absensi_karyawan:
				transactions = get_transaction(self.start_date, self.end_date)
