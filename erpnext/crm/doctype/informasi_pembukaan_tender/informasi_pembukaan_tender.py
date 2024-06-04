# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import (
	today,
)

class INFORMASIPEMBUKAANTENDER(Document):
	pass

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabINFORMASI PEMBUKAAN TENDER` WHERE name like '%/{0}/{1}'""".format(bulan, mydate.year), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/SAR/LPT/{0}/{1}".format(bulan, mydate.year, urut2)
		else:
			self.name = "01/SAR/LPT/{0}/{1}".format(bulan, mydate.year)


@frappe.whitelist()
def get_peserta(informasi_pembuatan_penawaran_terkait):
	return frappe.db.sql("""SELECT a.* FROM `tabLAPORAN PENJELASAN TENDER _ PESERTA TENDER` a
			INNER JOIN `tabLAPORAN PENJELASAN TENDER` b ON b.name = a.parent		  
			WHERE b.informasi_pembuatan_penawaran = '{0}' ORDER BY idx ASC""".format(informasi_pembuatan_penawaran_terkait), as_dict=1)
