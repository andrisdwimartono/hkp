# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import format_date

class DailyK3(Document):
	def validate(self):
		# check unique of project, date
		exists = frappe.db.get_value(
			"Daily K3",
			{"project": self.project, "date": self.date, "docstatus": 0}
		)
		if exists and exists != self.name:
			frappe.throw(_("Daily K3 already exists for {0} on {1}.").format(self.project, format_date(self.date)))

		# check work hour not more than 24 hours
		if self.working_hours > 24:
			frappe.throw(_("Working hours cannot be more than 24 hours."))

		
			