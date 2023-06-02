// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daftar Deposito"] = {
	"filters": [
		{
            "fieldname":"date_from",
            "label": __("Date From"),
            "fieldtype": "Date"
        },
		{
            "fieldname":"date_to",
            "label": __("Date To"),
            "fieldtype": "Date"
        },
	]
};
