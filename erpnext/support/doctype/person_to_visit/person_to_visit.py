# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PersonToVisit(Document):
	def on_submit(self):
		if frappe.session.user != self.user:
			frappe.throw("Hanya bisa disubmit oleh {0}".format(self.user))
	def validate(self):
		if self.user:
			assigner = []

			assigner.append(self.user)
			self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.user))
			notification_doc = {
				"type": "Alert",
				"document_type": self.doctype,
				"document_name": self.name,
				"subject": "Kunjungan dari {0} - {1} kepada anda telah selesai!".format(self.nama, self.perusahaan),
				"from_user": "hasta.maudyrismaslodia@gmail.com",
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)

	def after_insert(self):
		assigner = []

		assigner.append("hasta.maudyrismaslodia@gmail.com")
		self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format("hasta.maudyrismaslodia@gmail.com"))
		notification_doc = {
			"type": "Alert",
			"document_type": self.doctype,
			"document_name": self.name,
			"subject": "Kunjungan dari {0} - {1} selesai!".format(self.nama, self.perusahaan),
			"from_user": "hasta.maudyrismaslodia@gmail.com",
		}
		
		notification_doc = frappe._dict(notification_doc)
		from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
		make_notification_logs(notification_doc, assigner)