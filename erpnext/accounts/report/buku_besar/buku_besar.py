# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns()
	return columns, data

def get_data(filters=None):
	filter_dates = ""
	if filters.from_date and filters.to_date:
		if filters.from_date > filters.to_date:
			frappe.throw(_("From Date cannot be greater than To Date."))
		filter_dates = "AND ge.posting_date BETWEEN '{from_date}' AND '{to_date}'".format(
			from_date=filters.from_date,
			to_date=filters.to_date
		)
	filter_account = ""
	if filters.account:
		filter_account = "AND ge.account = '{account}'".format(
			account=filters.account
		)
	filter_voucher_no = ""
	if filters.voucher_no:
		filter_voucher_no = "AND ge.voucher_no LIKE '%{voucher_no}%'".format(
			voucher_no=filters.voucher_no
		)
	
	filter_party = ""
	if filters.party_type and filters.party:
		filter_party = "AND ge.party_type = '{party_type}' AND ge.party = '{party}'".format(
			party_type=filters.party_type,
			party=filters.party
		)
	filter_project = ""
	if filters.project:
		filter_project = "AND ge.project = '{project}'".format(
			project=filters.project
		)
	
	# Step 1: Calculate initial_balance
	initial_balance = frappe.db.sql("""
		SELECT
			IFNULL(SUM(ge.debit), 0) - IFNULL(SUM(ge.credit), 0)
		FROM
			`tabGL Entry` ge
		WHERE
			ge.docstatus = 1
			AND ge.is_cancelled = 0
			{0} {1} {2} {3}
			AND ge.posting_date < '{4}'
	""".format(filter_account, filter_voucher_no, filter_party, filter_project, filters.from_date))[0][0]

	# Step 2: Use initial_balance in your main query
	data = frappe.db.sql("""
		SELECT
			ge.posting_date,
			ge.nomor_bukti,
			ge.remarks,
			ge.account,
			0 as initial_balance,  -- will override in Python
			CASE WHEN ge.voucher_type = 'Journal Entry' THEN jea.debit
				ELSE ge.debit END AS debit,
			CASE WHEN ge.voucher_type = 'Journal Entry' THEN jea.credit
				ELSE ge.credit END AS credit,
			@saldo := @saldo +
					  (CASE WHEN ge.voucher_type = 'Journal Entry' THEN jea.debit ELSE ge.debit END) - 
					  (CASE WHEN ge.voucher_type = 'Journal Entry' THEN jea.credit ELSE ge.credit END) AS balance,
			ge.voucher_type,
			ge.voucher_no,
			ge.project,
			p.project_name
		FROM (SELECT @saldo := {0}) AS init,
		`tabGL Entry` ge
		LEFT JOIN `tabJournal Entry Account` jea ON jea.parent = ge.voucher_no AND ge.account = jea.account AND ge.voucher_type = 'Journal Entry'
		LEFT JOIN `tabProject` p ON p.name = ge.project
		WHERE ge.docstatus = 1 AND ge.is_cancelled = 0
		{1} {2} {3} {4} {5}
		ORDER BY ge.posting_date, ge.account
	""".format(initial_balance, filter_dates, filter_account, filter_voucher_no, filter_party, filter_project), as_dict=True)
	# data = frappe.db.sql("""
	# 	SELECT
	# 		ge.posting_date,
	# 		ge.nomor_bukti,
	# 		ge.remarks,
	# 		ge.account,
	# 		0 as initial_balance,  -- will override in Python
	# 		ge.debit,
	# 		ge.credit,
	# 		@saldo := @saldo + ge.debit - ge.credit AS balance,
	# 		ge.voucher_type,
	# 		ge.voucher_no,
	# 		ge.project,
	# 		p.project_name
	# 	FROM (SELECT @saldo := {0}) AS init,
	# 	`tabGL Entry` ge
	# 	LEFT JOIN `tabProject` p ON p.name = ge.project
	# 	WHERE ge.docstatus = 1 AND ge.is_cancelled = 0
	# 	{1} {2} {3} {4} {5}
	# 	ORDER BY ge.posting_date, ge.account
	# """.format(initial_balance, filter_dates, filter_account, filter_voucher_no, filter_party, filter_project), as_dict=True)

	# Step 3: Add initial balance row at the top
	initial_row = {
		"posting_date": filters.from_date,
		"nomor_bukti": "",
		"remarks": "Initial Balance",
		"account": "",  # or the filtered account
		"initial_balance": initial_balance,
		"debit": 0,
		"credit": 0,
		"balance": initial_balance,
		"voucher_type": "",
		"voucher_no": "",
		"project": "",
		"project_name": "",
	}

	data.insert(0, initial_row)

	return data

def get_columns():
	columns = [
		{
			"fieldname": "posting_date",
			"label": _("Posting Date"),
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"fieldname": "nomor_bukti",
			"label": _("Nomor Bukti"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "remarks",
			"label": _("Remarks"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "account",
			"label": _("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"width": 200,
		},
		{
			"fieldname": "debit",
			"label": _("Debit"),
			"fieldtype": "Currency",
			"width": 180,
		},
		{
			"fieldname": "credit",
			"label": _("Credit"),
			"fieldtype": "Currency",
			"width": 180,
		},
		{
			"fieldname": "balance",
			"label": _("Balance"),
			"fieldtype": "Currency",
			"width": 180,
		},
		{
			"fieldname": "voucher_type",
			"label": _("Voucher Type"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "voucher_no",
			"label": _("Voucher No"),
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 150,
		},
		{
			"fieldname": "project",
			"label": _("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 150,
		},
		{
			"fieldname": "project_name",
			"label": _("Project Name"),
			"fieldtype": "Data",
			"width": 150,
		}
	]
	return columns