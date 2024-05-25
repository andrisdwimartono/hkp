// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MONITORING PENAWARAN HARGA"] = {
	"filters": [
		{
			fieldname:"customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer"
		},
		{
			fieldname:"start_date",
			label: __("Start Date"),
			fieldtype: "Date"
		},
		{
			fieldname:"finish_date",
			label: __("Finish Date"),
			fieldtype: "Date"
		},
	]
};
