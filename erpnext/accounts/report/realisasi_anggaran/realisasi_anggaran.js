// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Realisasi Anggaran"] = {
	"filters": [
		{
			"fieldname":"date_from",
			"label": __("Tanggal Mulai"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"date_to",
			"label": __("Tanggal Akhir"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
	]
};