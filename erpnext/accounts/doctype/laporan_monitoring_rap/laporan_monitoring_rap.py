# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LaporanMonitoringRAP(Document):
	def validate(self):
		self.is_synchronized = 0
		for d in self.detail:
			d.is_synchronized = 0

	def after_insert(self):
		self.queue_update_realization()

	def on_update(self):
		self.queue_update_realization()

	def queue_update_realization(self):
		frappe.enqueue(
			"erpnext.api.laporan_monitoring_rap.update_income_realization",
			queue="short",
			docname=self.name,
			income_adjustment=self.income_adjustment
		)

		for d in self.detail:
			frappe.enqueue(
				"erpnext.api.laporan_monitoring_rap.update_cost_realization",
				queue="short",
				docname=d.name,
				cost_adjustment=d.adjustment
			)

	def get_income_realization(self):
		if self.income:
			amount = frappe.db.sql("""
				SELECT SUM(credit-debit) as amount FROM `tabGL Entry`
				WHERE account = '{0}'
				AND docstatus = 1
				AND is_cancelled = 0
				AND voucher_type != 'Period Closing Voucher'
			""".format(self.income), as_dict=True)

			if amount and amount[0] and amount[0].amount:
				return amount[0].amount
			else:
				return 0
		else:
			return 0