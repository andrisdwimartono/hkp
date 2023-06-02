// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sub Contract Hand Over', {
	// refresh: function(frm) {

	// },
	setup: function(frm){
		frm.set_query("budget", function() {
			return {
				filters: {
					'project': frm.doc.project,
					'docstatus': frm.doc.project?1:100
				}
			};
		});

		frm.set_query("pos_rap", function() {
			return {
				query: "erpnext.accounts.doctype.budget_realization.budget_realization.get_pos_rap",
				filters: {
					'budget': frm.doc.budget
				}
			}
		});
	},
	pos_rap: function(frm){
		frappe.call({
			method: 'erpnext.accounts.doctype.form_payment_entry_project.form_payment_entry_project.check_budget',
			args: {
				'budget': frm.doc.budget,
				'pos_rap': frm.doc.pos_rap
			},
			callback: function(r) {
				console.log(r)
				if(r.message){
					var vals = r.message[0];
					frm.set_value("budget_amount", vals.budget_amount);
					frm.refresh_field("budget_amount");
				}
			}
		});
	}
});
