# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.support.doctype.risalah_rapat.risalah_rapat import get_department_abbr_by_session
import datetime

class Memo(Document):
	def on_submit(self):
		if self.kepada:
			assigner = []
			if self.dari_merupakan_karyawan == 1:
				if self.dari_user_id:
					users = frappe.db.sql("""SELECT u.name FROM tabUser u
					INNER JOIN tabEmployee e ON e.user_id = u.name
					WHERE e.user_id = '{0}'""".format(self.dari_user_id), as_dict=1)
					for x in users:
						assigner.append(x.name)
					self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.dari_user_id))
			else:
				if self.dari_designation:
					users = frappe.db.sql("""SELECT u.name FROM tabUser u
					INNER JOIN tabEmployee e ON e.user_id = u.name
					WHERE e.designation = '{0}'""".format(self.dari_designation), as_dict=1)
					for x in users:
						assigner.append(x.name)
					self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.dari_designation))
			
			for d in self.kepada:
				if d.kepada_merupakan_karyawan == 1:
					if d.user_id:
						users = frappe.db.sql("""SELECT u.name FROM tabUser u
						INNER JOIN tabEmployee e ON e.user_id = u.name
						WHERE e.user_id = '{0}'""".format(d.user_id), as_dict=1)
						for x in users:
							assigner.append(x.name)
						self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user_id))
				else:
					if d.designation:
						users = frappe.db.sql("""SELECT u.name FROM tabUser u
						INNER JOIN tabEmployee e ON e.user_id = u.name
						WHERE e.designation = '{0}'""".format(d.designation), as_dict=1)
						for x in users:
							assigner.append(x.name)
						self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.designation))
			for d in self.tembusan:
				if d.kepada_merupakan_karyawan == 1:
					if d.user_id:
						users = frappe.db.sql("""SELECT u.name FROM tabUser u
						INNER JOIN tabEmployee e ON e.user_id = u.name
						WHERE e.user_id = '{0}'""".format(d.user_id), as_dict=1)
						for x in users:
							assigner.append(x.name)
						self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user_id))
				else:
					if d.designation:
						users = frappe.db.sql("""SELECT u.name FROM tabUser u
						INNER JOIN tabEmployee e ON e.user_id = u.name
						WHERE e.designation = '{0}'""".format(d.designation), as_dict=1)
						for x in users:
							assigner.append(x.name)
						self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.designation))
			# if self.tembusan_merupakan_karyawan == 1:
			# 	if self.tembusan_user_id:
			# 		users = frappe.db.sql("""SELECT u.name FROM tabUser u
			# 		INNER JOIN tabEmployee e ON e.user_id = u.name
			# 		WHERE e.user_id = '{0}'""".format(self.tembusan_user_id), as_dict=1)
			# 		for x in users:
			# 			assigner.append(x.name)
			# 		self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.tembusan_user_id))
			# else:
			# 	if self.tembusan_designation:
			# 		users = frappe.db.sql("""SELECT u.name FROM tabUser u
			# 		INNER JOIN tabEmployee e ON e.user_id = u.name
			# 		WHERE e.designation = '{0}'""".format(self.tembusan_designation), as_dict=1)
			# 		for x in users:
			# 			assigner.append(x.name)
			# 		self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.tembusan_designation))

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
			if self.dari_merupakan_karyawan == 1:
				if self.dari_user_id:
					users = frappe.db.sql("""SELECT u.name FROM tabUser u
					INNER JOIN tabEmployee e ON e.user_id = u.name
					WHERE e.user_id = '{0}'""".format(self.dari_user_id), as_dict=1)
					for x in users:
						assigner.append(x.name)
					self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.dari_user_id))
			else:
				if self.dari_designation:
					users = frappe.db.sql("""SELECT u.name FROM tabUser u
					INNER JOIN tabEmployee e ON e.user_id = u.name
					WHERE e.designation = '{0}'""".format(self.dari_designation), as_dict=1)
					for x in users:
						assigner.append(x.name)
					self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.dari_designation))
			
			for d in self.kepada:
				if d.kepada_merupakan_karyawan == 1:
					if d.user_id:
						users = frappe.db.sql("""SELECT u.name FROM tabUser u
						INNER JOIN tabEmployee e ON e.user_id = u.name
						WHERE e.user_id = '{0}'""".format(d.user_id), as_dict=1)
						for x in users:
							assigner.append(x.name)
						self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user_id))
				else:
					if d.designation:
						users = frappe.db.sql("""SELECT u.name FROM tabUser u
						INNER JOIN tabEmployee e ON e.user_id = u.name
						WHERE e.designation = '{0}'""".format(d.designation), as_dict=1)
						for x in users:
							assigner.append(x.name)
						self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.designation))
			for d in self.tembusan:
				if d.kepada_merupakan_karyawan == 1:
					if d.user_id:
						users = frappe.db.sql("""SELECT u.name FROM tabUser u
						INNER JOIN tabEmployee e ON e.user_id = u.name
						WHERE e.user_id = '{0}'""".format(d.user_id), as_dict=1)
						for x in users:
							assigner.append(x.name)
						self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user_id))
				else:
					if d.designation:
						users = frappe.db.sql("""SELECT u.name FROM tabUser u
						INNER JOIN tabEmployee e ON e.user_id = u.name
						WHERE e.designation = '{0}'""".format(d.designation), as_dict=1)
						for x in users:
							assigner.append(x.name)
						self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.designation))
			# if self.tembusan_merupakan_karyawan == 1:
			# 	if self.tembusan_user_id:
			# 		users = frappe.db.sql("""SELECT u.name FROM tabUser u
			# 		INNER JOIN tabEmployee e ON e.user_id = u.name
			# 		WHERE e.user_id = '{0}'""".format(self.tembusan_user_id), as_dict=1)
			# 		for x in users:
			# 			assigner.append(x.name)
			# 		self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.tembusan_user_id))
			# else:
			# 	if self.tembusan_designation:
			# 		users = frappe.db.sql("""SELECT u.name FROM tabUser u
			# 		INNER JOIN tabEmployee e ON e.user_id = u.name
			# 		WHERE e.designation = '{0}'""".format(self.tembusan_designation), as_dict=1)
			# 		for x in users:
			# 			assigner.append(x.name)
			# 		self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.tembusan_designation))

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
			if self.dari_merupakan_karyawan != 1 and self.dari_designation == "Direktur Utama":
				self.name = "{2}/DU/Memo/{0}/{1}".format(bulan, mydate.year, urut2)
			elif self.dari_merupakan_karyawan != 1 and self.dari_designation == "Direktur Operasi":
				self.name = "{2}/DO/Memo/{0}/{1}".format(bulan, mydate.year, urut2)
			else:
				self.name = "{2}/{3}/Memo/{0}/{1}".format(bulan, mydate.year, urut2, get_department_abbr_by_session())
		else:
			if self.dari_merupakan_karyawan != 1 and self.dari_designation == "Direktur Utama":
				self.name = "001/DU/Memo/{0}/{1}".format(bulan, mydate.year)
			elif self.dari_merupakan_karyawan != 1 and self.dari_designation == "Direktur Operasi":
				self.name = "001/DO/Memo/{0}/{1}".format(bulan, mydate.year)
			else:
				self.name = "001/{2}/Memo/{0}/{1}".format(bulan, mydate.year, get_department_abbr_by_session())

def get_permission_query_conditions(user):
	if get_department_abbr_by_session() == "ADU":
		return ""
	a = frappe.db.sql("""SELECT DISTINCT(`tabMemo Kepada`.parent) parent FROM `tabMemo Kepada`
					INNER JOIN `tabEmployee` ON `tabEmployee`.name = `tabMemo Kepada`.employee
		WHERE `tabEmployee`.user_id = '{0}' AND `tabMemo Kepada`.parenttype = 'Memo'""".format(frappe.session.user), as_dict=1)
	stri = ""
	n = 0
	if a:
		for x in a:
			n=n+1
			stri = "{0}{1}".format(stri, " {1} `tabMemo`.`name` = '{0}'".format(x.parent, "OR" if n > 1 else ""))

	a2 = frappe.db.sql("""SELECT DISTINCT(`tabMemo`.name) name FROM `tabMemo`
					INNER JOIN `tabEmployee` ON `tabEmployee`.name = `tabMemo`.dari_employee
		WHERE `tabEmployee`.user_id = '{0}'""".format(frappe.session.user), as_dict=1)
	if a2:
		for x2 in a2:
			n=n+1
			stri = "{0}{1}".format(stri, " {1} `tabMemo`.`name` = '{0}'".format(x2.name, "OR" if n > 1 else ""))

	a3 = frappe.db.sql("""SELECT `tabMemo`.name name FROM `tabMemo`
		WHERE `tabMemo`.owner = '{0}'""".format(frappe.session.user), as_dict=1)
	if a3:
		for x3 in a3:
			n=n+1
			stri = "{0}{1}".format(stri, " {1} `tabMemo`.`name` = '{0}'".format(x3.name, "OR" if n > 1 else ""))

	return """{0}""".format(stri)