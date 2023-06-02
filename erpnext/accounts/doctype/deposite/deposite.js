// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Deposite', {
	setup: function(frm){
		frm.set_query("account", function() {
			return {
				filters: {'is_group': 0}
			}
		});

		frm.set_query("account_receivable", function() {
			return {
				filters: {'is_group': 0}
			}
		});
	},
	refresh: function(frm) {
		// if(frm.doc.docstatus===1 && frm.doc.status==="Deposited") {
		// 	frm.add_custom_button(__("Cairkan"), function() {
		// 		frm.events.make_pencairan_deposito(frm);
		// 	});
		// }
	},
	make_pencairan_deposito: function(frm){
		frappe.call({
			method:
				"erpnext.accounts.doctype.deposite.deposite.pencairan_deposito",
			args: {
				dt: frm.doc.doctype,
				dn: frm.doc.name,
				taken_date: frm.doc.taken_date,
				taken_balance: frm.doc.taken_balance,
				account: frm.doc.account,
				account_receivable: frm.doc.account_receivable,
				interest_balance: frm.doc.interest_balance,
				account_interest: frm.doc.account_interest,
				account_receivable_interest: frm.doc.account_receivable_interest,
			},
			callback: function (r) {
				if (!r.exc) {
					
				}
			},
		})
	}
});
