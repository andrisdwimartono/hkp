# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class Memo(Document):
	def on_submit(self):
		if self.kepada:
			assigner = []
			if self.dari:
				users = frappe.db.sql("""SELECT u.name FROM tabUser u
				INNER JOIN tabEmployee e ON e.user_id = u.name
				WHERE e.designation = '{0}'""".format(self.dari), as_dict=1)
				for x in users:
					assigner.append(x.name)
				self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.dari))
			for d in self.kepada:
				if d.designation:
					users = frappe.db.sql("""SELECT u.name FROM tabUser u
					INNER JOIN tabEmployee e ON e.user_id = u.name
					WHERE e.designation = '{0}'""".format(d.designation), as_dict=1)
					for x in users:
						assigner.append(x.name)
					self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.designation))
			if self.tembusan:
				users = frappe.db.sql("""SELECT u.name FROM tabUser u
				INNER JOIN tabEmployee e ON e.user_id = u.name
				WHERE e.designation = '{0}'""".format(self.tembusan), as_dict=1)
				for x in users:
					assigner.append(x.name)
				self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.tembusan))
			notification_doc = {
				"type": "Alert",
				"document_type": self.doctype,
				"document_name": self.name,
				"subject": "Memo baru, {0}".format(self.hal),
				"from_user": self.owner,
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)
	
	def on_cancel(self):
		if self.kepada:
			assigner = []
			if self.dari:
				users = frappe.db.sql("""SELECT u.name FROM tabUser u
				INNER JOIN tabEmployee e ON e.user_id = u.name
				WHERE e.designation = '{0}'""".format(self.dari), as_dict=1)
				for x in users:
					assigner.append(x.name)
				self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.dari))
			for d in self.kepada:
				if d.designation:
					users = frappe.db.sql("""SELECT u.name FROM tabUser u
					INNER JOIN tabEmployee e ON e.user_id = u.name
					WHERE e.designation = '{0}'""".format(d.designation), as_dict=1)
					for x in users:
						assigner.append(x.name)
					self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.designation))
			if self.tembusan:
				users = frappe.db.sql("""SELECT u.name FROM tabUser u
				INNER JOIN tabEmployee e ON e.user_id = u.name
				WHERE e.designation = '{0}'""".format(self.tembusan), as_dict=1)
				for x in users:
					assigner.append(x.name)
				self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.tembusan))
			notification_doc = {
				"type": "Alert",
				"document_type": self.doctype,
				"document_name": self.name,
				"subject": "Memo dibatalkan tentang {0}".format(self.hal),
				"from_user": self.owner,
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)
		
		
	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.tanggal_memo, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabMemo` WHERE name like '%{0}/{1}'""".format(bulan, mydate.year), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/DU/Memo/{0}/{1}".format(bulan, mydate.year, urut2)
		else:
			self.name = "001/DU/Memo/{0}/{1}".format(bulan, mydate.year)
