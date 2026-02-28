# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import (
	today,
)
from erpnext.support.doctype.risalah_rapat.risalah_rapat import get_department_abbr_by_session

class LAPORANAKTIVITASDILUARKANTOR(Document):
	pass

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		abbr = get_department_abbr_by_session()
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabLAPORAN AKTIVITAS DI LUAR KANTOR` WHERE name like '%/{0}/{1}'""".format(bulan, mydate.year), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			if abbr != None and abbr != "":
				abbr = "SAR"
			self.name = "{2}/{3}/LAA/{0}/{1}".format(bulan, mydate.year, urut2, abbr)
		else:
			self.name = "01/{2}/LAA/{0}/{1}".format(bulan, mydate.year, abbr)

def get_permission_query_conditions(user):
	return """(`tabLAPORAN AKTIVITAS DI LUAR KANTOR`.owner = '{0}')""".format(frappe.session.user)