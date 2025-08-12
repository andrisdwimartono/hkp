# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

import erpnext
from erpnext.accounts.general_ledger import make_reverse_gl_entries, make_gl_entries
from erpnext.controllers.accounts_controller import AccountsController
from frappe.utils import (
	add_days,
	today,
	date_diff,
)

from erpnext.projects.bot import send_message_finance

class Deposite(AccountsController):
	def validate(self):
		self.items = []
	def on_submit(self):
		return
		student_gl_entries = self.get_gl_dict(
			{
				"account": self.account_receivable,
				"against": self.account,
				"debit": self.balance,
				"debit_in_account_currency": self.balance,
				"against_voucher": self.name,
				"against_voucher_type": self.doctype,
				"transaction_date": self.posting_date,
				"cost_center": self.cost_center
			},
			item=self,
		)

		fee_gl_entry = self.get_gl_dict(
			{
				"account": self.account,
				"against": self.account_receivable,
				"credit": self.balance,
				"credit_in_account_currency": self.balance,
				"transaction_date": self.posting_date,
				"cost_center": self.cost_center
			},
			item=self,
		)

		make_gl_entries(
			[student_gl_entries, fee_gl_entry],
			cancel=(False),
			update_outstanding="Yes",
			merge_entries=False,
		)
		
	def on_update_after_submit(self):
		self.items = []
		if self.status != "Deposited":
			return
		if not self.taken_balance:
			return
		# student_gl_entries = self.get_gl_dict(
		# 	{
		# 		"account": self.account,
		# 		"against": self.account_receivable,
		# 		"debit": self.taken_balance,
		# 		"debit_in_account_currency": self.taken_balance,
		# 		"against_voucher": self.name,
		# 		"against_voucher_type": self.doctype,
		# 		"transaction_date": self.taken_date,
		# 		"cost_center": self.cost_center
		# 	},
		# 	item=self,
		# )

		# fee_gl_entry = self.get_gl_dict(
		# 	{
		# 		"account": self.account_receivable,
		# 		"against": self.account,
		# 		"credit": self.taken_balance,
		# 		"credit_in_account_currency": self.taken_balance,
		# 		"transaction_date": self.taken_date,
		# 		"cost_center": self.cost_center
		# 	},
		# 	item=self,
		# )

		# make_gl_entries(
		# 	[student_gl_entries, fee_gl_entry],
		# 	cancel=(False),
		# 	update_outstanding="Yes",
		# 	merge_entries=False,
		# )

		if not self.interest_balance:
			return
		# student_gl_entries = self.get_gl_dict(
		# 	{
		# 		"account": self.account_interest,
		# 		"against": self.account_receivable_interest,
		# 		"debit": self.interest_balance,
		# 		"debit_in_account_currency": self.interest_balance,
		# 		"against_voucher": self.name,
		# 		"against_voucher_type": self.doctype,
		# 		"transaction_date": self.taken_date,
		# 		"cost_center": self.cost_center
		# 	},
		# 	item=self,
		# )

		# fee_gl_entry = self.get_gl_dict(
		# 	{
		# 		"account": self.account_receivable_interest,
		# 		"against": self.account_interest,
		# 		"credit": self.interest_balance,
		# 		"credit_in_account_currency": self.interest_balance,
		# 		"transaction_date": self.taken_date,
		# 		"cost_center": self.cost_center
		# 	},
		# 	item=self,
		# )

		# make_gl_entries(
		# 	[student_gl_entries, fee_gl_entry],
		# 	cancel=(False),
		# 	update_outstanding="Yes",
		# 	merge_entries=False,
		# )

		frappe.db.sql("update `tabDeposite` SET status = 'Taken' where name = '{0}'".format(self.name))
		frappe.db.commit()
		self.reload()

		def set_incoming_rate(self):
			return

@frappe.whitelist()
def pencairan_deposito(dt = None, dn = None, taken_date = None, taken_balance = 0, account = None, account_receivable = None, interest_balance = 0, account_interest = None, account_receivable_interest = None):
		if not taken_balance:
			return
		student_gl_entries = self.get_gl_dict(
			{
				"account": account,
				"against": account_receivable,
				"debit": taken_balance,
				"debit_in_account_currency": taken_balance,
				"against_voucher": dn,
				"against_voucher_type": dt,
				"transaction_date": taken_date
			},
			item=None,
		)

		fee_gl_entry = self.get_gl_dict(
			{
				"account": account_receivable,
				"against": account,
				"credit": taken_balance,
				"credit_in_account_currency": taken_balance,
				"transaction_date": taken_date
			},
			item=None,
		)

		from erpnext.accounts.general_ledger import make_gl_entries

		make_gl_entries(
			[student_gl_entries, fee_gl_entry],
			cancel=(False),
			update_outstanding="Yes",
			merge_entries=False,
		)

		if not interest_balance:
			return
		student_gl_entries = self.get_gl_dict(
			{
				"account": account_interest,
				"against": account_receivable_interest,
				"debit": interest_balance,
				"debit_in_account_currency": interest_balance,
				"against_voucher": dn,
				"against_voucher_type": dt,
				"transaction_date": taken_date
			},
			item=None,
		)

		fee_gl_entry = self.get_gl_dict(
			{
				"account": account_receivable_interest,
				"against": account_interest,
				"credit": interest_balance,
				"credit_in_account_currency": interest_balance,
				"transaction_date": taken_date
			},
			item=None,
		)

		from erpnext.accounts.general_ledger import make_gl_entries

		make_gl_entries(
			[student_gl_entries, fee_gl_entry],
			cancel=(False),
			update_outstanding="Yes",
			merge_entries=False,
		)

@frappe.whitelist()
def get_deposite_obsolete():
	x = today()
	deposites = frappe.db.sql("""
		SELECT 
			a.*, 
			DATE_FORMAT(a.schedule_date, "%%d-%%m-%%Y") AS dend, 
			a.schedule_date
		FROM 
			`tabDeposite` a 
		WHERE 
			DATE_SUB(a.schedule_date, INTERVAL 15 DAY) <= %s
	""", (x), as_dict=1)
	for d in deposites:
		if date_diff(x, d.schedule_date)%7 == 0:
			notification_doc = {
				"type": "Alert",
				"document_type": "Deposite",
				"document_name": d.name,
				"subject": "Deposito {0} akan jatuh tempo di {1}".format(d.name, d.dend),
				"from_user": d.owner or "Administrator",
			}
			
			assigner = [d.owner]
			adu_employees = frappe.db.sql("""SELECT DISTINCT u.name user_id FROM `tabHas Role` hr
								INNER JOIN tabUser u ON u.name = hr.parent
								WHERE hr.role IN ('ADU') AND hr.parenttype = 'User'""", as_dict=1)
			for hr in adu_employees:
				assigner.append(hr.user_id)
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)
			send_message_finance("Deposito {0} akan jatuh tempo di {1}".format(d.name, d.dend), chat_id="-1002718415291")