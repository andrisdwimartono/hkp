// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monitoring Anggaran Biaya Pelaksanaan"] = {
	"filters": [
		{
			fieldname: "budget",
			label: __("Budget"),
			fieldtype: "Link",
			options: "Budget",
			reqd: 1,
		},
	]
};
