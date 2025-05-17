# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_datas(filters)
	return columns, data

def get_datas(filters):
	data = frappe.db.sql("""
		SELECT
			fpep.name as document,
			'Kas Bon Proyek' as type,
			group_concat(fpea.pos_rap separator ',') as item,
			fpep.purpose,
			concat(fpep.project, ' - ', fpep.project_name) project,
			fpep.outstanding_amount,
			group_concat(DATE_FORMAT(fp.posting_date, '%d-%m-%Y') separator ',') as payment_date
		FROM
			`tabForm Payment Entry Project` fpep
		LEFT JOIN `tabForm Payment Entry Account` fpea ON fpea.parent = fpep.name
		INNER JOIN `tabPayment Entry` fp ON fp.form_payment_entry_project = fpep.name AND fp.docstatus IN (1)
		LEFT JOIN `tabRealisasi Anggaran Proyek` rap ON rap.form_payment_entry_project = fpep.name AND rap.docstatus IN (1)
		WHERE
			fpep.docstatus in (1) and fpep.base_on != 'Purchase Order' AND rap.name is null
		GROUP BY fpep.name

		UNION

		SELECT
			fpe.name as document,
			'Kas Bon Non Proyek' as type,
			group_concat(fpenp.pos_rap separator ',') as item,
			fpe.purpose,
			'' project,
			fpe.outstanding_amount,
			group_concat(DATE_FORMAT(fp.posting_date, '%d-%m-%Y') separator ',') as payment_date
		FROM
			`tabForm Payment Entry` fpe
		LEFT JOIN `tabForm Payment Entry Non Project` fpenp ON fpenp.parent = fpe.name
		INNER JOIN `tabPayment Entry` fp ON fp.form_payment_entry = fpenp.name AND fp.docstatus IN (1)
		LEFT JOIN `tabRealisasi Anggaran Non Proyek` ranp ON ranp.form_payment_entry = fpenp.name AND ranp.docstatus IN (1)
		WHERE
			fpe.docstatus in (1) AND ranp.name is null
		GROUP BY fpe.name;""", as_dict=True)
	if not data:
		frappe.throw("Tidak ada data yang ditemukan")
	return data

def get_columns():
	columns = [
		{
			"label": "Dokumen",
			"fieldname": "document",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": "Jenis",
			"fieldname": "type",
			"fieldtype": "Data",
			"width": 160,
		},
		# {
		# 	"label": "Item",
		# 	"fieldname": "item",
		# 	"fieldtype": "Data",
		# 	"width": 300,
		# },
		{
			"label": "Purpose",
			"fieldname": "purpose",
			"fieldtype": "Data",
			"width": 400,
		},
		{
			"label": "Project",
			"fieldname": "project",
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"label": "Nilai Sisa",
			"fieldname": "outstanding_amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 180,
		},
		{
			"label": "Tanggal Bayar",
			"fieldname": "payment_date",
			"fieldtype": "Data",
			"width": 250,
		}
	]
	return columns