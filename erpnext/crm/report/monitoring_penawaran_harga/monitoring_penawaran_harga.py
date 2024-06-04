
# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_column(columns)
	data = get_data(filters)
	return columns, data

def get_column(columns):
	columns.append({
		"fieldname": "customer",
		"label": "Customer",
		"fieldtype": "Link",
		"options": "Customer"
	})
	columns.append({
		"fieldname": "lingkup_pekerjaan",
		"label": "Lingkup Pekerjaan",
		"fieldtype": "Data"
	})
	columns.append({
		"fieldname": "tanggal_rks",
		"label": "Tanggal",
		"fieldtype": "Date"
	})
	columns.append({
		"fieldname": "name",
		"label": "No. Surat Penawaran",
		"fieldtype": "Data"
	})
	columns.append({
		"fieldname": "nilai_penawaran",
		"label": "Nilai Penawaran (Dalam Ribuan)",
		"fieldtype": "Currency"
	})
	columns.append({
		"fieldname": "catatan",
		"label": "Keterangan",
		"fieldtype": "Data"
	})
	return columns

def get_data(filters):
	where = ""
	if filters.customer and (filters.start_date and filters.finish_date):
		where = "WHERE main.customer = '{0}' AND umt.pemasukan_penawaran_tanggal BETWEEN '{1}' AND '{2}'".format(filters.customer, filters.start_date, filters.finish_date)
	if not filters.customer and (filters.start_date and filters.finish_date):
		where = "WHERE umt.pemasukan_penawaran_tanggal BETWEEN '{1}' AND '{2}'".format(filters.customer, filters.start_date, filters.finish_date)
	if filters.customer and not (filters.start_date and filters.finish_date):
		where = "WHERE main.customer = '{0}'".format(filters.customer, filters.start_date, filters.finish_date)
	return frappe.db.sql("""
		SELECT 
			main.customer, main.lingkup_pekerjaan, umt.pemasukan_penawaran_tanggal as tanggal_rks, main.name, COALESCE(ipt.harga_penawaran_hkp/1000, 0) AS nilai_penawaran, COALESCE(ipt.keterangan, "") catatan FROM `tabINFORMASI PEMBUATAN PENAWARAN` AS main
		LEFT JOIN `tabUSULAN MENGIKUTI TENDER` AS umt ON umt.name = main.usulan_mengikuti_tender 
		LEFT JOIN `tabINFORMASI PEMBUKAAN TENDER` AS ipt ON ipt.informasi_pembuatan_penawaran_terkait = main.name 
		{0}""".format(where), as_dict=1)