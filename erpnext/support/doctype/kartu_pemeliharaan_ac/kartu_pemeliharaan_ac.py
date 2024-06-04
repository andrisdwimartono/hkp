# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.support.doctype.risalah_rapat.risalah_rapat import get_department_abbr_by_session
import datetime
from frappe.utils import (
	today,
)

class KartuPemeliharaanAC(Document):
	def validate(self):
		self.abbr = get_department_abbr_by_session()

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabKartu Pemeliharaan AC` WHERE name like '%/{0}/{1}'""".format(bulan, mydate.year), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/IT/KPA/{0}/{1}".format(bulan, mydate.year, urut2)
		else:
			self.name = "01/IT/KPA/{0}/{1}".format(bulan, mydate.year)

def get_permission_query_conditions(user):
	if get_department_abbr_by_session() == "ADU":
		return ""
	return """(`tabKartu Pemeliharaan AC`.`abbr` = '{0}')
	""".format(get_department_abbr_by_session())