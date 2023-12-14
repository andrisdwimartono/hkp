# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class ScheduleAktivitas(Document):
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.tanggal, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabSchedule Aktivitas` WHERE tanggal between '{0}' and '{1}'""".format("{0}-01-01".format(mydate.year), "{0}-12-31".format(mydate.year)), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/ADU/SCHH/{0}/{1}".format(bulan, mydate.year-2000, urut2)
		else:
			self.name = "001/ADU/SCHH/{0}/{1}".format(bulan, mydate.year-2000)

@frappe.whitelist()
def get_schedule_aktivitas(start, end, user=None, for_reminder=False, filters=None):
	results = []
	schedule_aktivitass = frappe.db.sql("""SELECT * FROM `tabSchedule Aktivitas` WHERE tanggal >= '{0}' AND tanggal <= '{1}'""".format(start, end), as_dict=1)
	if schedule_aktivitass:
		for d in schedule_aktivitass:
			d.tanggalwaktu = "{0} {1}".format(d.tanggal, d.jam)
			results.append(d)
	return results