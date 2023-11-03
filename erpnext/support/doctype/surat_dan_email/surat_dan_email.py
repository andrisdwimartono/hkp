# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SuratdanEmail(Document):
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
