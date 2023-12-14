# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.support.doctype.risalah_rapat.risalah_rapat import get_department_abbr_by_session
import datetime

class SuratdanEmail(Document):
	def validate(self):
		self.abbr = get_department_abbr_by_session()

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.tanggal, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabSurat dan Email` WHERE tanggal between '{0}' and '{1}'""".format("{0}-01-01".format(mydate.year), "{0}-12-31".format(mydate.year)), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/{4}/{5}{3}/{0}/{1}".format(bulan, mydate.year-2000, urut2, "/{0}".format(self.project) if self.project else "", get_department_abbr_by_session(), self.kode_ordner)
		else:
			self.name = "001/{3}/{4}{2}/{0}/{1}".format(bulan, mydate.year-2000, "/{0}".format(self.project) if self.project else "", get_department_abbr_by_session(), self.kode_ordner)

	def on_submit(self):
		if self.notifikasi:
			assigner = []
			for d in self.notifikasi:
				if d.user:
					assigner.append(d.user)
					self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user))
			notification_doc = {
				"type": "Alert",
				"document_type": self.doctype,
				"document_name": self.name,
				"subject": "Ada {0} masuk dari {1} untuk anda ketahui".format(self.type, self.customer),
				"from_user": self.owner,
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)

def get_permission_query_conditions(user):
	if get_department_abbr_by_session() == "ADU":
		return ""
	
	return """(`tabSurat dan Email`.`abbr` = '{0}')
	""".format(get_department_abbr_by_session())