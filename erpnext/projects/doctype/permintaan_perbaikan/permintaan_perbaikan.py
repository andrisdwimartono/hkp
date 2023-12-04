# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import (
	today,
)

class PermintaanPerbaikan(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabPermintaan Perbaikan` WHERE name like '%/{2}/{0}/{1}'""".format(bulan, mydate.year, "K" if self.type == "Kendaraan" else "G"), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "PPIP/{2}/{3}/{0}/{1}".format(bulan, mydate.year, urut2, "K" if self.type == "Kendaraan" else "G")
		else:
			self.name = "PPIP/001/{2}/{0}/{1}".format(bulan, mydate.year, "K" if self.type == "Kendaraan" else "G")

	def validate(self):
		total_biaya = 0
		for d in self.tindakan_permintaan_perbaikan:
			total_biaya = total_biaya+d.biaya
		self.total_biaya = total_biaya