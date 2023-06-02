# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = [
			{
				'fieldname': 'no',
				'label': _('No'),
				'fieldtype': 'Data',
				'width': 20
			},
			{
				'fieldname': 'no_td',
				'label': _('No. T/D'),
				'fieldtype': 'Data',
				'width': 180
			},
			{
				'fieldname': 'schedule_date',
				'label': _('Jatuh Tempo'),
				'fieldtype': 'Date',
				'width': 100
			},
			{
				'fieldname': 'nominal_usd',
				'label': _('USD'),
				'fieldtype': 'Float',
				'width': 140
			},
			{
				'fieldname': 'nominal_eur',
				'label': _('EUR'),
				'fieldtype': 'Float',
				'width': 140
			},
			{
				'fieldname': 'nominal_rp',
				'label': _('Rp'),
				'fieldtype': 'Float',
				'width': 140
			}
		]
	data = get_data(filters)
	return columns, data

def get_data(filters):
	detail = frappe.db.sql(
		"""SELECT * FROM(
			SELECT 'head_1' `type`, d.bank `grp`, d.bank, null `schedule_date`, 0 nominal_usd, 0 nominal_eur, 0 nominal_rp FROM `tabDeposite` d 
			WHERE d.schedule_date BETWEEN '{0}' AND '{1}' 
			GROUP BY d.bank
			UNION
			SELECT 'head_2' `type`, e.bank `grp`, e.account_number, e.schedule_date, CASE WHEN e.currency = 'USD' THEN e.balance ELSE 0 END `nominal_usd`, CASE WHEN e.currency = 'EUR' THEN e.balance ELSE 0 END `nominal_eur`, CASE WHEN e.currency = 'IDR' THEN e.balance ELSE 0 END `nominal_rp` FROM `tabDeposite` e
			WHERE e.schedule_date BETWEEN '{0}' AND '{1}' 
			UNION
			SELECT 'head_3' `type`, f.bank `grp`, f.bank, null `schedule_date`, SUM(CASE WHEN f.currency = 'USD' THEN f.balance ELSE 0 END) `nominal_usd`, SUM(CASE WHEN f.currency = 'EUR' THEN f.balance ELSE 0 END) `nominal_eur`, SUM(CASE WHEN f.currency = 'IDR' THEN f.balance ELSE 0 END) `nominal_rp` FROM `tabDeposite` f 
			WHERE f.schedule_date BETWEEN '{0}' AND '{1}' 
			GROUP BY f.bank
			UNION
			SELECT 'head_4' `type`, 'ZZZZ' `grp`, null bank, null `schedule_date`, SUM(CASE WHEN f.currency = 'USD' THEN f.balance ELSE 0 END) `nominal_usd`, SUM(CASE WHEN f.currency = 'EUR' THEN f.balance ELSE 0 END) `nominal_eur`, SUM(CASE WHEN f.currency = 'IDR' THEN f.balance ELSE 0 END) `nominal_rp` FROM `tabDeposite` f 
			WHERE f.schedule_date BETWEEN '{0}' AND '{1}') bn
			ORDER BY bn.grp, bn.type ASC
		""".format(filters.date_from, filters.date_to),
		as_dict=1,
	)

	result = []
	no_h1 = 0
	no_h2 = 0
	for d in detail:
		if d.type == "head_1":
			no_h1=no_h1+1
			no_h2 = 0
			result.append({
				"no": chr(no_h1+64),
				"no_td": d.bank,
				"schedule_date": d.schedule_date,
				"nominal_usd": None,
				"nominal_eur": None,
				"nominal_rp": None
			})
		elif d.type == "head_2":
			no_h2=no_h2+1
			result.append({
				"no": no_h2,
				"no_td": d.bank,
				"schedule_date": d.schedule_date,
				"nominal_usd": d.nominal_usd,
				"nominal_eur": d.nominal_eur,
				"nominal_rp": d.nominal_rp
			})
		elif d.type == "head_4":
			result.append({
				"no": "",
				"no_td": """JUMLAH TOTAL""",
				"schedule_date": d.schedule_date,
				"nominal_usd": d.nominal_usd,
				"nominal_eur": d.nominal_eur,
				"nominal_rp": d.nominal_rp
			})
		else:
			result.append({
				"no": "",
				"no_td": """JUMLAH {0} ({1})""".format(d.bank, chr(no_h1+64)),
				"schedule_date": d.schedule_date,
				"nominal_usd": d.nominal_usd,
				"nominal_eur": d.nominal_eur,
				"nominal_rp": d.nominal_rp
			})
	return result