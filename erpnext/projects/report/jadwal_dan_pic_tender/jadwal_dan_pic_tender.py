# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns, data = get_columns(columns, data)
	return columns, data

def get_columns(columns, data):
	row = frappe._dict()
	row.fieldname = "field"
	row.label = ""
	row.fieldtype = "Data"
	columns.append(row)

	field = {}
	rw_labels = ["Pagu (Rp)", "Aanwijzig Kantor", "Aanwijzig Lapangan", "Mempelajari RKS", "Pemasukan penawaran", "PIC", "Koordinator"]
	for r in rw_labels:
		field["field"] = r

	jdpts = frappe.db.sql("""SELECT * FROM `tabJadwal dan PIC Tender` order by name""", as_dict=1)
	for d in jdpts:
		row = frappe._dict()
		row.fieldname = d.name
		row.label = d.nama_paket
		row.fieldtype = "Data"
		columns.append(row)
	
	no = 0
	pagu = {}
	for c in columns:
		pagu = {}
		for d in jdpts:
			if c.fieldname == d.name:
				pagu[c.fieldname] = d.pagu
		data.append(pagu)
	return columns, data