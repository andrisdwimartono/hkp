# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import cint, cstr
from six import iteritems
from datetime import datetime, timedelta

from erpnext.accounts.report.financial_statements import (
	get_columns,
	get_cost_centers_with_children,
	get_data,
	get_data3,
	get_filtered_list_for_consolidated_report,
	get_period_list,
	get_period_list2,
)
from erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement import (
	get_net_profit_loss,
	get_net_profit_loss2,
)
from erpnext.accounts.utils import get_fiscal_year

def get_saldo_awal(filtering):
	to_fiscal_year = filtering.to_fiscal_year
	fil = filtering
	is_nol = False
	if filtering.filter_based_on == "Fiscal Year":
		fil.period_start_date = filtering.period_start_date
		fil.period_end_date = filtering.period_end_date
		if filtering.from_fiscal_year != "2024":
			fil.from_fiscal_year = "2024"
			fil.to_fiscal_year = str(int(filtering.to_fiscal_year)-1)
		else:
			is_nol = True
	else:
		return {}
		fil.period_start_date = "2024-01-01"
		fil.period_end_date = datetime.strptime(filtering.period_start_date, "%Y-%m-%d") + timedelta(days=(-1))
		fil.from_fiscal_year = filtering.from_fiscal_year
		fil.to_fiscal_year = filtering.to_fiscal_year
	
	period_list2 = get_period_list2(
		fil.from_fiscal_year,
		fil.to_fiscal_year,
		fil.period_start_date,
		fil.period_end_date,
		fil.filter_based_on,
		fil.periodicity,
		company=fil.company,
	)

	cash_flow_accounts2 = get_cash_flow_accounts2()

	# compute net profit / loss
	income2 = get_data3(
		fil.company,
		"Income",
		"Credit",
		period_list2,
		filters=fil,
		accumulated_values=fil.accumulated_values,
		ignore_closing_entries=True,
		ignore_accumulated_values_for_fy=True,
	)
	expense2 = get_data3(
		fil.company,
		"Expense",
		"Debit",
		period_list2,
		filters=fil,
		accumulated_values=fil.accumulated_values,
		ignore_closing_entries=True,
		ignore_accumulated_values_for_fy=True,
	)

	net_profit_loss = get_net_profit_loss2(income2, expense2, period_list2, fil.company)

	data2 = []
	summary_data2 = {}
	company_currency = frappe.get_cached_value("Company", fil.company, "default_currency")

	for cash_flow_account in cash_flow_accounts2:
		section_data2 = []
		data2.append(
			{
				"account_name": cash_flow_account["section_header"],
				"parent_account": None,
				"indent": 0.0,
				"account": cash_flow_account["section_header"],
			}
		)

		if len(data2) == 1:
			# add first net income in operations section
			if net_profit_loss:
				net_profit_loss.update(
					{"indent": 1, "parent_account": cash_flow_accounts2[0]["section_header"]}
				)
				data2.append(net_profit_loss)
				section_data2.append(net_profit_loss)

		for account in cash_flow_account["account_types"]:
			account_data = get_account_type_based_data2(
				fil.company, account["account_type"], period_list2, fil.accumulated_values, fil
			)
			account_data.update(
				{
					"account_name": account["label"],
					"account": account["label"],
					"indent": 1,
					"parent_account": cash_flow_account["section_header"],
					"currency": company_currency,
				}
			)
			data2.append(account_data)
			section_data2.append(account_data)

		add_total_row_account2(
			data2,
			section_data2,
			cash_flow_account["section_footer"],
			period_list2,
			company_currency,
			summary_data2,
			fil,
		)

	add_total_row_account2(
		# data2, data2, _("Net Change in Cash"), period_list, company_currency, summary_data2, fil
		data2, data2, _("Saldo Awal"), period_list2, company_currency, summary_data2, fil
	)

	x = data2[len(data2)-2]
	
	if is_nol:
		x.update({
			"total": 0,
			"dec_{0}".format(to_fiscal_year): 0
		})
	else:
		x.update({
			"dec_{0}".format(to_fiscal_year): x.get("total")
		})
	return x

def execute(filters=None):
	if cint(frappe.db.get_single_value("Accounts Settings", "use_custom_cash_flow")):
		from erpnext.accounts.report.cash_flow.custom_cash_flow import execute as execute_custom

		return execute_custom(filters=filters)

	period_list = get_period_list(
		filters.from_fiscal_year,
		filters.to_fiscal_year,
		filters.period_start_date,
		filters.period_end_date,
		filters.filter_based_on,
		filters.periodicity,
		company=filters.company,
	)

	cash_flow_accounts = get_cash_flow_accounts()

	# compute net profit / loss
	income = get_data(
		filters.company,
		"Income",
		"Credit",
		period_list,
		filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True,
		ignore_accumulated_values_for_fy=True,
	)
	expense = get_data(
		filters.company,
		"Expense",
		"Debit",
		period_list,
		filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True,
		ignore_accumulated_values_for_fy=True,
	)

	net_profit_loss = get_net_profit_loss(income, expense, period_list, filters.company)

	data = []
	summary_data = {}
	company_currency = frappe.get_cached_value("Company", filters.company, "default_currency")

	for cash_flow_account in cash_flow_accounts:
		section_data = []
		data.append(
			{
				"account_name": cash_flow_account["section_header"],
				"parent_account": None,
				"indent": 0.0,
				"account": cash_flow_account["section_header"],
			}
		)

		if len(data) == 1:
			# add first net income in operations section
			if net_profit_loss:
				net_profit_loss.update(
					{"indent": 1, "parent_account": cash_flow_accounts[0]["section_header"]}
				)
				data.append(net_profit_loss)
				section_data.append(net_profit_loss)

		for account in cash_flow_account["account_types"]:
			account_data = get_account_type_based_data(
				filters.company, account["account_type"], period_list, filters.accumulated_values, filters
			)
			account_data.update(
				{
					"account_name": account["label"],
					"account": account["label"],
					"indent": 1,
					"parent_account": cash_flow_account["section_header"],
					"currency": company_currency,
				}
			)
			data.append(account_data)
			section_data.append(account_data)

		add_total_row_account(
			data,
			section_data,
			cash_flow_account["section_footer"],
			period_list,
			company_currency,
			summary_data,
			filters,
		)

	
	add_total_row_account(
		# data, data, _("Net Change in Cash"), period_list, company_currency, summary_data, filters
		data, data, _("KENAIKAN (PENURUNAN) NETO KAS DAN SETARA KAS"), period_list, company_currency, summary_data, filters
	)

	columns = get_columns(
		filters.periodicity, period_list, filters.accumulated_values, filters.company
	)

	chart = get_chart_data(columns, data)

	report_summary = get_report_summary(summary_data, company_currency)

	total3 = 0
	b = get_saldo_awal(filtering=filters)
	data.append(b)
	total3 = total3+b.get("total")
	a = data[len(data)-3]
	data.append(a)

	c = {
		"account_name": "Saldo Akhir",
		"account": None,
		"currency": b["currency"]
	}
	for key in b:
		if key not in ('account_name', 'account', 'currency'):
			c[key] = b[key]+a[key]
	data.append(c)
	# total3 = total3
	# a.update({
	# 	"total": total3
	# })
	# data.append({
	# 	a
	# })
	return columns, data, None, chart, report_summary


def get_cash_flow_accounts():
	operation_accounts = {
		"section_name": "Operations",
		"section_footer": _("Net Cash from Operations"),
		"section_header": _("Cash Flow from Operations"),
		"account_types": [
			{"account_type": "Depreciation", "label": _("Depreciation")},
			{"account_type": "Receivable", "label": _("Net Change in Accounts Receivable")},
			{"account_type": "Payable", "label": _("Net Change in Accounts Payable")},
			{"account_type": "Stock", "label": _("Net Change in Inventory")},
		],
	}

	investing_accounts = {
		"section_name": "Investing",
		"section_footer": _("Net Cash from Investing"),
		"section_header": _("Cash Flow from Investing"),
		"account_types": [{"account_type": "Fixed Asset", "label": _("Net Change in Fixed Asset")}],
	}

	financing_accounts = {
		"section_name": "Financing",
		"section_footer": _("Net Cash from Financing"),
		"section_header": _("Cash Flow from Financing"),
		"account_types": [{"account_type": "Equity", "label": _("Net Change in Equity")}],
	}

	# combine all cash flow accounts for iteration
	return [operation_accounts, investing_accounts, financing_accounts]

def get_cash_flow_accounts2():
	operation_accounts = {
		"section_name": "Operations",
		"section_footer": _("Net Cash from Operations"),
		"section_header": _("Cash Flow from Operations"),
		"account_types": [
			{"account_type": "Depreciation", "label": _("Depreciation")},
			{"account_type": "Receivable", "label": _("Net Change in Accounts Receivable")},
			{"account_type": "Payable", "label": _("Net Change in Accounts Payable")},
			{"account_type": "Stock", "label": _("Net Change in Inventory")},
		],
	}

	investing_accounts = {
		"section_name": "Investing",
		"section_footer": _("Net Cash from Investing"),
		"section_header": _("Cash Flow from Investing"),
		"account_types": [{"account_type": "Fixed Asset", "label": _("Net Change in Fixed Asset")}],
	}

	financing_accounts = {
		"section_name": "Financing",
		"section_footer": _("Net Cash from Financing"),
		"section_header": _("Cash Flow from Financing"),
		"account_types": [{"account_type": "Equity", "label": _("Net Change in Equity")}],
	}

	# combine all cash flow accounts for iteration
	return [operation_accounts, investing_accounts, financing_accounts]

def get_account_type_based_data(company, account_type, period_list, accumulated_values, filters):
	data = {}
	total = 0
	for period in period_list:
		start_date = get_start_date(period, accumulated_values, company)
		filters.start_date = start_date
		filters.end_date = period["to_date"]
		filters.account_type = account_type

		amount = get_account_type_based_gl_data(company, filters)

		if amount and account_type == "Depreciation":
			amount *= -1

		total += amount
		data.setdefault(period["key"], amount)

	data["total"] = total
	return data

def get_account_type_based_data2(company, account_type, period_list, accumulated_values, filters):
	data = {}
	total = 0
	for period in period_list:
		start_date = get_start_date(period, accumulated_values, company)
		filters.start_date = start_date
		filters.end_date = period["to_date"]
		filters.account_type = account_type

		amount = get_account_type_based_gl_data(company, filters)

		if amount and account_type == "Depreciation":
			amount *= -1

		total += amount
		data.setdefault(period["key"], amount)

	data["total"] = total
	return data

def get_account_type_based_gl_data(company, filters=None):
	cond = ""
	filters = frappe._dict(filters or {})

	if filters.include_default_book_entries:
		company_fb = frappe.db.get_value("Company", company, "default_finance_book")
		cond = """ AND (finance_book in (%s, %s, '') OR finance_book IS NULL)
			""" % (
			frappe.db.escape(filters.finance_book),
			frappe.db.escape(company_fb),
		)
	else:
		cond = " AND (finance_book in (%s, '') OR finance_book IS NULL)" % (
			frappe.db.escape(cstr(filters.finance_book))
		)

	if filters.get("cost_center"):
		filters.cost_center = get_cost_centers_with_children(filters.cost_center)
		cond += " and cost_center in %(cost_center)s"

	gl_sum = frappe.db.sql_list(
		"""
		select sum(credit) - sum(debit)
		from `tabGL Entry`
		where company=%(company)s and posting_date >= %(start_date)s and posting_date <= %(end_date)s
			and voucher_type != 'Period Closing Voucher'
			and account in ( SELECT name FROM tabAccount WHERE account_type = %(account_type)s) {cond}
	""".format(
			cond=cond
		),
		filters,
	)

	return gl_sum[0] if gl_sum and gl_sum[0] else 0


def get_start_date(period, accumulated_values, company):
	if not accumulated_values and period.get("from_date"):
		return period["from_date"]

	start_date = period["year_start_date"]
	if accumulated_values:
		start_date = get_fiscal_year(period.to_date, company=company)[1]

	return start_date


def add_total_row_account(
	out, data, label, period_list, currency, summary_data, filters, consolidated=False
):
	total_row = {
		"account_name": "'" + _("{0}").format(label) + "'",
		"account": "'" + _("{0}").format(label) + "'",
		"currency": currency,
	}

	summary_data[label] = 0

	# from consolidated financial statement
	if filters.get("accumulated_in_group_company"):
		period_list = get_filtered_list_for_consolidated_report(filters, period_list)

	for row in data:
		if row.get("parent_account"):
			for period in period_list:
				key = period if consolidated else period["key"]
				total_row.setdefault(key, 0.0)
				total_row[key] += row.get(key, 0.0)
				summary_data[label] += row.get(key)

			total_row.setdefault("total", 0.0)
			total_row["total"] += row["total"]

	out.append(total_row)
	out.append({})

def add_total_row_account2(
	out, data, label, period_list, currency, summary_data, filters, consolidated=False
):
	total_row = {
		"account_name": "'" + _("{0}").format(label) + "'",
		"account": "'" + _("{0}").format(label) + "'",
		"currency": currency,
	}

	summary_data[label] = 0

	# from consolidated financial statement
	if filters.get("accumulated_in_group_company"):
		period_list = get_filtered_list_for_consolidated_report(filters, period_list)

	for row in data:
		if row.get("parent_account"):
			for period in period_list:
				key = period if consolidated else period["key"]
				total_row.setdefault(key, 0.0)
				total_row[key] += row.get(key, 0.0)
				summary_data[label] += row.get(key)

			total_row.setdefault("total", 0.0)
			total_row["total"] += row["total"]

	out.append(total_row)
	out.append({})

def get_report_summary(summary_data, currency):
	report_summary = []

	for label, value in iteritems(summary_data):
		report_summary.append(
			{"value": value, "label": label, "datatype": "Currency", "currency": currency}
		)

	return report_summary


def get_chart_data(columns, data):
	labels = [d.get("label") for d in columns[2:]]
	datasets = [
		{
			"name": account.get("account").replace("'", ""),
			"values": [account.get(d.get("fieldname")) for d in columns[2:]],
		}
		for account in data
		if account.get("parent_account") == None and account.get("currency")
	]
	datasets = datasets[:-1]

	chart = {"data": {"labels": labels, "datasets": datasets}, "type": "bar"}

	chart["fieldtype"] = "Currency"

	return chart
