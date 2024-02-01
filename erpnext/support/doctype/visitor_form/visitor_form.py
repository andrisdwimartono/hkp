# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	formatdate,
)

class VisitorForm(Document):
	def on_submit(self):
		if self.status == "Diajukan":
			frappe.throw("Status masih diajukan, ubah sebelum submit")
		if frappe.session.user != "hasta.satriautama@gmail.com":
			frappe.throw("Hanya bisa disubmit oleh hasta.satriautama@gmail.com")
	def validate(self):
		if self.status != "Diajukan":
			if frappe.session.user != "hasta.maudyrismaslodia@gmail.com" and frappe.session.user != "hasta.satriautama@gmail.com":
				frappe.throw("Hanya bisa diubah oleh hasta.maudyrismaslodia@gmail.com atau hasta.satriautama@gmail.com".format(self.user))
			else:
				assigner = []

				assigner.append("hasta.satriautama@gmail.com")
				self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format("hasta.satriautama@gmail.com"))
				notification_doc = {
					"type": "Alert",
					"document_type": self.doctype,
					"document_name": self.name,
					"subject": "Kunjungan dari {0} - {1} keperluan {4} untuk tanggal {2} hingga {3}".format(self.nama, self.perusahaan, formatdate(self.start_date) if self.start_date else "-", formatdate(self.finish_date) if self.finish_date else "-", self.keperluan or "-"),
					"from_user": "hasta.maudyrismaslodia@gmail.com",
				}
				
				notification_doc = frappe._dict(notification_doc)
				from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
				make_notification_logs(notification_doc, assigner)

	def after_insert(self):
		assigner = []

		assigner.append("hasta.maudyrismaslodia@gmail.com")
		self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format("hasta.maudyrismaslodia@gmail.com"))
		# assigner.append("hasta.satriautama@gmail.com")
		# self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format("hasta.satriautama@gmail.com"))
		notification_doc = {
			"type": "Alert",
			"document_type": self.doctype,
			"document_name": self.name,
			"subject": "Kunjungan dari {0} - {1} keperluan {4} untuk tanggal {2} hingga {3}".format(self.nama, self.perusahaan, formatdate(self.start_date) if self.start_date else "-", formatdate(self.finish_date) if self.finish_date else "-", self.keperluan or "-"),
			"from_user": "hasta.maudyrismaslodia@gmail.com",
		}
		
		notification_doc = frappe._dict(notification_doc)
		from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
		make_notification_logs(notification_doc, assigner)

# @frappe.whitelist(allow_guest=True)
# def make_payment_request(**args):
# 	return frappe.db.sql("""""", as_dict=1)