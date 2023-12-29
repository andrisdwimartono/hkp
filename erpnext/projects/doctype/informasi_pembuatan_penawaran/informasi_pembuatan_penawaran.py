# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

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

@frappe.whitelist()
def view_doc(docname):
	frappe.db.sql("UPDATE `tabProcess Rule2` SET status = 'Viewed' WHERE parent = '{0}' AND parenttype = 'Informasi Pembuatan Penawaran' AND user = '{1}'".format(docname, frappe.session.user))