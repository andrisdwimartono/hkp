# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RencanaKerja(Document):
	def validate(self):
		checking = frappe.db.sql(
		""" SELECT * FROM `tabJenis Pekerjaan Except` WHERE parent = '{0}' AND pekerjaan = '{1}'
		""".format(self.jenis_pekerjaan, self.pekerjaan), as_dict=1)
		if checking:
			frappe.throw("""Jenis Pekerjaan {0} tidak boleh di Pekerjaan {1}""".format(self.jenis_pekerjaan, self.pekerjaan))

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.strptime(self.tanggal, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabRencana Kerja` WHERE name like '%/{0}/{1}'""".format(bulan, mydate.year), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/SAR/REK/{0}/{1}".format(bulan, mydate.year, urut2)
		else:
			self.name = "01/SAR/REK/{0}/{1}".format(bulan, mydate.year)