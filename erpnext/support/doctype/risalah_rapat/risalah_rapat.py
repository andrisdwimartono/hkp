# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class RisalahRapat(Document):
	def validate(self):
		self.abbr = get_department_abbr_by_session()

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.datetime.strptime(self.tanggal, '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabRisalah Rapat` WHERE tanggal between '{0}' and '{1}'""".format("{0}-01-01".format(mydate.year), "{0}-12-31".format(mydate.year)), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/{4}/RRAP{3}/{0}/{1}".format(bulan, mydate.year-2000, urut2, "/{0}".format(self.project) if self.project else "", get_department_abbr_by_session())
		else:
			self.name = "001/{3}/RRAP{2}/{0}/{1}".format(bulan, mydate.year-2000, "/{0}".format(self.project) if self.project else "", get_department_abbr_by_session())

	def on_submit(self):
		if self.peserta_rapat:
			assigner = []
			if self.user_pimpinan_rapat:
				assigner.append(self.user_pimpinan_rapat)
				self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(self.user_pimpinan_rapat))
			for d in self.peserta_rapat:
				if d.user:
					assigner.append(d.user)
					self.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(d.user))
			notification_doc = {
				"type": "Alert",
				"document_type": self.doctype,
				"document_name": self.name,
				"subject": "Risalah Rapat {0} baru".format(self.name),
				"from_user": self.owner,
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)

def get_permission_query_conditions(user):
	if get_department_abbr_by_session() == "ADU":
		return ""
	a = frappe.db.sql("""SELECT * FROM `tabPeserta Rapat`
		WHERE user = '{0}'""".format(frappe.session.user), as_dict=1)
	stri = ""
	if a:
		for x in a:
			stri = "{0}{1}".format(stri, " OR `tabRisalah Rapat`.`name` = '{0}'".format(x.parent))
	
	return """(`tabRisalah Rapat`.`abbr` = '{0}'{1})
	""".format(get_department_abbr_by_session(), stri)

def get_department_abbr_by_session():
	a = frappe.db.sql("""SELECT tabDepartment.abbr FROM tabEmployee 
					  INNER JOIN tabDepartment ON tabDepartment.name = tabEmployee.department
					  WHERE user_id = '{0}'
					  LIMIT 1""".format(frappe.session.user), as_dict=1)
	if a:
		return a[0].abbr
	return "ADU"