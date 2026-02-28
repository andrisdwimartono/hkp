// Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Kartu Hutang"] = {
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
			"width": 200,
			"get_query": function () {
				let project = frappe.query_report.get_filter_value('project');
				if (project) {
					return {
						"filters": { project: project }
					};
				}
			},

		},
		{
			"label": "SPK",
			"fieldname": "spk",
			"fieldtype": "Link",
			"options": "Sub Contract Hand Over",
			"width": 200,
			"get_query": function () {
				let sub_contract = frappe.query_report.get_filter_value('sub_contract');
				if (sub_contract) {
					return {
						"filters": { sub_contract: sub_contract }
					};
				}
			}
		},
		{
			"label": "Supplier",
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 200,
			"get_query": function () {
				let project = frappe.query_report.get_filter_value('project');
				if (project) {
					frappe.call({
						method: "erpnext.buying.report.kartu_hutang.kartu_hutang.get_supplier_by_project",
						args: {
							project: project,
						},
						callback: function(r) {
							if(r.message) {
								let list_supplier = [];
								for (let i = 0; i < r.message.length; i++) {
									list_supplier.push(r.message[i].supplier);
								}
								console.log(list_supplier);
								return {
									filters: ["name", "in", list_supplier]
								};
							}
						}
					});
				}
			}
		},
		{
			"label": "Purchase Order",
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 200,
			"get_query": function () {
				let supplier = frappe.query_report.get_filter_value('supplier');
				let project = frappe.query_report.get_filter_value('project');
				if (supplier && project) {
					return {
						filters: { supplier: supplier, project: project }
					};
				}
				if (supplier && !project) {
					return {
						filters: { supplier: supplier }
					};
				}
				if (!supplier && project) {
					return {
						filters: { project: project }
					};
				}
			}
		}
	]
};
