# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.support.doctype.risalah_rapat.risalah_rapat import get_department_abbr_by_session
import datetime

class FormulirPerbaikanAlatKerjaYangRusak(Document):
	def validate(self):
		self.abbr = get_department_abbr_by_session()

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.tanggal, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabFormulir Perbaikan Alat Kerja Yang Rusak` WHERE tanggal between '{0}' and '{1}'""".format("{0}-01-01".format(mydate.year), "{0}-12-31".format(mydate.year)), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/{3}/FPAKYR/{0}/{1}".format(bulan, mydate.year-2000, urut2, get_department_abbr_by_session())
		else:
			self.name = "001/{2}/FPAKYR/{0}/{1}".format(bulan, mydate.year-2000, get_department_abbr_by_session())

def get_permission_query_conditions(user):
	if get_department_abbr_by_session() == "ADU":
		return ""
	return """(`tabFormulir Perbaikan Alat Kerja Yang Rusak`.`abbr` = '{0}')
	""".format(get_department_abbr_by_session())