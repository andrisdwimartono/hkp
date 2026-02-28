// Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Realisasi Rencana Anggaran Proyek"] = {
	"filters": [
		{
			"fieldname": "budget",
			"label": "Budget",
			"fieldtype": "Link",
			"options": "Budget",
			"width": 140
		},
		{
			"fieldname": "date_to",
			"label": "Date To",
			"fieldtype": "Date",
			"width": 140
		}
	]
};
