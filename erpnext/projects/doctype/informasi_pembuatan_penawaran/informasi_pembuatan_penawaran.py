# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import (
	today,
)

class INFORMASIPEMBUATANPENAWARAN(Document):
	def validate(self):
		row = 0
		for d in self.pejabat:
			row = row+1
			if not d.employee:
				frappe.throw("Pejabat di baris ke {0} harus diisi".format(row))
		row = 0
		for d in self.aktivitas:
			row = row+1
			if not d.target:
				frappe.throw("Sasaran di baris ke {0} harus diisi".format(row))
				
	def after_insert(self):
		assigner = []
		for d in self.pejabat:
			if d.user:
				assigner.append(d.user)
				self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user))
			notification_doc = {
				"type": "Alert",
				"document_type": self.doctype,
				"document_name": self.name,
				"subject": "Informasi Pembuatan Penawaran baru {0}".format(self.name),
				"from_user": self.owner,
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabINFORMASI PEMBUATAN PENAWARAN` WHERE name like '%/{0}/{1}'""".format(bulan, mydate.year), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/SAR/INP/{0}/{1}".format(bulan, mydate.year, urut2)
		else:
			self.name = "01/SAR/INP/{0}/{1}".format(bulan, mydate.year)

@frappe.whitelist()
def view_doc(docname):
	frappe.db.sql("UPDATE `tabProcess Rule2` SET status = 'Viewed' WHERE parent = '{0}' AND parenttype = 'Informasi Pembuatan Penawaran' AND user = '{1}'".format(docname, frappe.session.user))