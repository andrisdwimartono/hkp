# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.support.doctype.risalah_rapat.risalah_rapat import get_department_abbr_by_session
from datetime import datetime
from frappe.utils import (
	today,
)

class CommunicationForm(Document):
	def validate(self):
		self.abbr = get_department_abbr_by_session()

	# 	#untuk notification
	# 	assigner = []
	# 	for d in self.to_employee:
	# 		to_employee = frappe.db.sql("""SELECT * FROM tabEmployee WHERE name = '{0}'""".format(d.to_employee), as_dict=1)
	# 		if to_employee and to_employee[0].user_id:
	# 			assigner.append(to_employee[0].user_id)

	# 	notification_doc = {
	# 			"type": "Alert",
	# 			"document_type": self.doctype,
	# 			"document_name": self.name,
	# 			"subject": "Communication Form {0} untuk {1}".format(self.name. self.subject),
	# 			"from_user": self.owner,
	# 		}
			
	# 	notification_doc = frappe._dict(notification_doc)
	# 	from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
	# 	make_notification_logs(notification_doc, assigner)

	def autoname(self):
		roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
		mydate = datetime.strptime(today(), '%Y-%m-%d')
		bulan = roman[int(mydate.month)]
		

		a = frappe.db.sql("""SELECT COUNT(*) cnt FROM `tabCommunication Form` WHERE name like '%/{2}/{0}/{1}'""".format(bulan, mydate.year, get_department_abbr_by_session()), as_dict=1)
		if a:
			urut = a[0].cnt+1
			urut2 = ""
			if urut < 9:
				urut2 = "00{0}".format(urut)
			elif urut < 99:
				urut2 = "0{0}".format(urut)
			else:
				urut2 = "{0}".format(urut)
			self.name = "{2}/{3}/{0}/{1}".format(bulan, mydate.year, urut2, get_department_abbr_by_session())
		else:
			self.name = "01/{2}/{0}/{1}".format(bulan, mydate.year, get_department_abbr_by_session())

def get_permission_query_conditions(user):
	if get_department_abbr_by_session() == "ADU":
		return ""
	return """(`tabCommunication Form`.`owner` = '{0}')
	""".format(frappe.session.user)