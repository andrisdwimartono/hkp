// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Budget Realization', {
	// refresh: function(frm) {

	// }
	setup: function(frm) {
		frm.set_query("budget", function() {
			return {
				filters: {
					'project': frm.doc.project,
					'docstatus': frm.doc.project?1:100
				}
			};
		});

		frm.set_query("pos_rap", function() {
			if(frm.doc.budget)
				return {
					query: "erpnext.accounts.doctype.budget_realization.budget_realization.get_pos_rap",
					filters: {"budget": frm.doc.budget}
				};
		});
	},
	pos_rap: function(frm){
		frappe.call({
			method: 'erpnext.accounts.doctype.budget_realization.budget_realization.check_budget',
			args: {
				'budget': frm.doc.budget,
				'pos_rap': frm.doc.pos_rap
			},
			callback: function(r) {
				if(r.message){
					var vals = r.message[0];
					frm.set_value("duration", vals.duration+1);
					var vols = vals.volume;
					if(vals.volume_realization){
						vols = vals.volume-vals.volume_realization;	
					}
					frm.set_value("volume", vols);
					frm.set_value("unit_price", vals.unit_price);
					frm.set_value("budget_amount", vals.budget_amount);
					frm.set_value("account", vals.account);
					frm.set_value("cost_center", vals.cost_center);
					frm.set_value("description", vals.description);
					frm.refresh_field("duration");
					frm.refresh_field("volume");
					frm.refresh_field("unit_price");
					frm.refresh_field("budget_amount");
					frm.refresh_field("account");
					frm.refresh_field("cost_center");
					frm.refresh_field("description");
				}
			}
		});
	},
	unit_price: function(frm){
		frm.set_value("budget_amount", frm.doc.volume*frm.doc.unit_price);
		frm.refresh_field("budget_amount");
	},
	volume: function(frm){
		frm.set_value("budget_amount", frm.doc.volume*frm.doc.unit_price);
		frm.refresh_field("budget_amount");
	}
});
