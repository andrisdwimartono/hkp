# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ScheduleAktivitas(Document):
	pass

@frappe.whitelist()
def get_schedule_aktivitas(start, end, user=None, for_reminder=False, filters=None):
	results = []
	schedule_aktivitass = frappe.db.sql("""SELECT * FROM `tabSchedule Aktivitas` WHERE tanggal >= '{0}' AND tanggal <= '{1}'""".format(start, end), as_dict=1)
	if schedule_aktivitass:
		for d in schedule_aktivitass:
			d.tanggalwaktu = "{0} {1}".format(d.tanggal, d.jam)
			results.append(d)
	return results