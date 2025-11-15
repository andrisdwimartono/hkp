# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RealisasiKPI(Document):
	pass

def get_permission_query_conditions(user):
	emplpoyee = frappe.db.sql("""SELECT * FROM `tabEmployee` where user_id = '{0}'""".format(frappe.session.user), as_dict=1)
	if emplpoyee AND employee[0].name:
		return """(`tabRealisasi KPI`.employee = '{0}')""".format(employee[0].name)
	else:
		return ""