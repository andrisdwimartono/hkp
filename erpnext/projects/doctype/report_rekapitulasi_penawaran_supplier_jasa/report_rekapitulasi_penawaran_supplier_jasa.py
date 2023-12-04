# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import (
	today,
)

class ReportREKAPITULASIPENAWARANSUPPLIERJASA(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabReport REKAPITULASI PENAWARAN SUPPLIER JASA` WHERE name like '%/{2}/{0}/{1}'""".format(bulan, mydate.year, self.project), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "RRPSJ/{2}/{3}/{0}/{1}".format(bulan, mydate.year, urut2, self.project)
		else:
			self.name = "RRPSJ/001/{2}/{0}/{1}".format(bulan, mydate.year, self.project)

@frappe.whitelist()
def get_data(project, jenis_pekerjaan):
	return frappe.db.sql("""
		SELECT a.name penawaran, a.bulan, a.tahun, a.jenis_pekerjaan, a.harga_rap, a.total_nilai, a.peringkat FROM `tabREKAPITULASI PENAWARAN SUPPLIER JASA` a
		WHERE project = '{0}' AND jenis_pekerjaan = '{1}'
		ORDER BY a.total_nilai ASC;
	""".format(project, jenis_pekerjaan), as_dict=1)