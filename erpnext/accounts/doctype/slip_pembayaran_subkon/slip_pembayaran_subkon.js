// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Slip Pembayaran Subkon', {
	// refresh: function(frm) {

	// },
	hand_over_progress: function(frm){
		if(frm.doc.hand_over_progress){
			frappe.call({
				method: 'erpnext.accounts.doctype.slip_pembayaran_subkon.slip_pembayaran_subkon.get_total',
				args: {
					'hand_over_progress': frm.doc.hand_over_progress
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						frm.set_value("total_cost", vals);
						frm.refresh_field("total_cost");
					}
				}
			});
			if(frm.doc.total_cost){
				frappe.call({
					method: 'erpnext.accounts.doctype.slip_pembayaran_subkon.slip_pembayaran_subkon.get_outstanding',
					args: {
						'hand_over_progress': frm.doc.hand_over_progress
					},
					callback: function(r) {
						if(r.message){
							var vals = r.message;
							frm.set_value("outstanding_amount", frm.doc.total_cost-vals);
							frm.refresh_field("outstanding_amount");
						}
					}
				});
			}
		}
	},
	required_date: function(frm) {
		if(frm.doc.required_date){
			frappe.call({
				method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.check_week',
				args: {
					'posting_date': frm.doc.required_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						frm.set_value("week_periode", vals);
						frm.refresh_field("week_periode");
					}
				}
			});
		}
	},
	paid: function(frm){
		if(frm.doc.paid){
			frm.set_value("ppn", frm.doc.ppn_percent*frm.doc.total_cost/100);
			frm.refresh_field("ppn");
		}
		if(frm.doc.paid){
			frm.set_value("pph", frm.doc.pph_percent*frm.doc.total_cost/100);
			frm.refresh_field("pph");
		}
		if(frm.doc.paid){
			frm.set_value("total", frm.doc.paid+frm.doc.ppn+frm.doc.pph-frm.doc.potongan);
			frm.refresh_field("total");
		}
	},
	ppn_percent: function(frm){
		if(frm.doc.ppn_percent && frm.doc.paid){
			frm.set_value("ppn", frm.doc.ppn_percent*frm.doc.total_cost/100);
			frm.refresh_field("ppn");

			frm.set_value("total", frm.doc.paid+frm.doc.ppn+frm.doc.pph-frm.doc.potongan);
			frm.refresh_field("total");
		}
	},
	pph_percent: function(frm){
		if(frm.doc.pph_percent && frm.doc.paid){
			frm.set_value("pph", frm.doc.pph_percent*frm.doc.total_cost/100);
			frm.refresh_field("pph");

			frm.set_value("total", frm.doc.paid+frm.doc.ppn+frm.doc.pph-frm.doc.potongan);
			frm.refresh_field("total");
		}
	},
	potongan: function(frm){
		if(frm.doc.potongan){
			frm.set_value("total", frm.doc.paid+frm.doc.ppn+frm.doc.pph-frm.doc.potongan);
			frm.refresh_field("total");
		}
	}
});
