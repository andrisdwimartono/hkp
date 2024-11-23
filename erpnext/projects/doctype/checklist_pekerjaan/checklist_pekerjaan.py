# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import (
	today,
)

class ChecklistPekerjaan(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabChecklist Pekerjaan` WHERE name like '%/{0}/{1}'""".format(bulan, mydate.year), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/DKD/CKL/{0}/{1}".format(bulan, mydate.year, urut2)
		else:
			self.name = "01/DKD/CKL/{0}/{1}".format(bulan, mydate.year)

@frappe.whitelist()
def get_detail(laporan_pengajuan_penagihan):
	return frappe.db.sql("""SELECT lppd.* FROM `tabLaporan Pengajuan Penagihan` lpp
					  INNER JOIN `tabLaporan Pengajuan Penagihan Detail` lppd ON lpp.name = lppd.parent
					  WHERE lpp.name = '{0}' AND lppd.group != 1 AND lppd.vol_terpasang_saat_ini > 0
					  ORDER BY lppd.idx ASC
					  """.format(laporan_pengajuan_penagihan), as_dict=1)