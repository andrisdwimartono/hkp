# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class SuratPermintaanHarga(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.posting_date, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabSurat Permintaan Harga` WHERE project = '{0}'""".format(self.project), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/LOG-SPH/{3}/{0}/{1}".format("0{0}".format(mydate.month) if mydate.month < 10 else mydate.month, mydate.year-2000, urut2, self.project)
		else:
			self.name = "001/LOG-SPH/{2}/{0}/{1}".format("0{0}".format(mydate.month) if mydate.month < 10 else mydate.month, mydate.year-2000, self.project)
