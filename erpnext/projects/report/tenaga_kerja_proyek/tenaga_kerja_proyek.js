// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["TENAGA KERJA PROYEK"] = {
	"filters": [
		{
			fieldname:"project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project"
		},
	]
};
