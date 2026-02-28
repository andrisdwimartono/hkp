// Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monitoring Progress SPK"] = {
	"filters": [
		{
			"label": "Project",
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 200
		},
		{
			"label": "Sub Kontrak",
			"fieldname": "sub_contract",
			"fieldtype": "Link",
			"options": "Sub Contract",
			"width": 200
		},
		{
			"label": "Supplier",
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 200
		},
		{
			"label": "SPK",
			"fieldname": "spk",
			"fieldtype": "Link",
			"options": "Sub Contract Hand Over",
			"width": 200
		},
		{
			"label": "Purchase Order",
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 200
		}
	]
};
