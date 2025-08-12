# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_data(filters=None):
	data = frappe.db.sql("""
		SELECT
			depo.bank,
			depo.location,
			depo.account_number,
			depo.start_date,
			depo.time_length,
			depo.length_type,
			depo.schedule_date,
			depo.currency,
			CASE WHEN depo.currency != 'IDR' THEN depo.balance ELSE 0 END AS balance,
			CASE WHEN depo.currency = 'IDR' THEN depo.balance ELSE 0 END AS principal_amount,
			CASE WHEN depo.balance > 0 THEN (depo.interest_balance / depo.balance)*100 ELSE 0 END AS interest_percent, 
			CASE WHEN depo.collateral = 'No' THEN 'Tdk Dijaminkan' ELSE 'Dijaminkan' END AS collateral,
			CASE WHEN depo.collateral = 'YES' THEN depo.collateral_to ELSE NULL END AS collateral_to,
			depo.available_status AS available_status,
			depo.keterangan
		FROM
			`tabDeposite` depo
		WHERE
			depo.docstatus < 2
	""", filters, as_dict=True)

	return data

def get_columns():
	columns = [
		{
			"label": "Nama Bank",
			"fieldname": "bank",
			"fieldtype": "Link",
			"options": "Bank",
			"width": 100,
		},
		{
			"label": "Lokasi",
			"fieldname": "location",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": "Bilyet",
			"fieldname": "account_number",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": "Pembukaan",
			"fieldname": "start_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": "Jangka Waktu",
			"fieldname": "time_length",
			"fieldtype": "Int",
			"width": 80,
		},
		{
			"label": "Satuan",
			"fieldname": "length_type",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": "Jatuh Tempo",
			"fieldname": "schedule_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": "Valas Currency",
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"width": 100,
			"hidden": 1,
		},
		{
			"label": "Valas",
			"fieldname": "balance",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 110,
		},
		{
			"label": "Nominal Pokok",
			"fieldname": "principal_amount",
			"fieldtype": "Currency",
			"options": "IDR",
			"width": 140,
		},
		{
			"label": "Bunga",
			"fieldname": "interest_percent",
			"fieldtype": "Percent",
			"width": 50,
		},
		{
			"label": "Posisi",
			"fieldname": "collateral",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": "Proyek",
			"fieldname": "collateral_to",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": "Status",
			"fieldname": "available_status",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": "Keterangan",
			"fieldname": "keterangan",
			"fieldtype": "Data",
			"width": 150,
		}
	]
	return columns
