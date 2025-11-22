// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Slip Pembayaran Subkon', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			var x = ["Kontrak Kerja / SPK", "Kwitansi / Progres Fisik", "Checklist / LKPP / Berita Acara", "Faktur Pajak"];
			if(frm.doc.form_payment_entry_checklist == undefined){
				for(var i = 0; i < x.length; i++){
					var c = frm.add_child("form_payment_entry_checklist");
					c.remark = x[i];
				}
			}
			
			frm.refresh_field("form_payment_entry_checklist");
		}
	},
	setup: function(frm){
		frm.set_query("budget", function() {
			return {
				filters: {
					'project': frm.doc.project
				}
			};
		});
	},
	hand_over_progress: function(frm){
		if(frm.doc.hand_over_progress){
			frappe.call({
				method: 'erpnext.pengendalian_biaya.doctype.slip_pembayaran_subkon.slip_pembayaran_subkon.get_total',
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
					method: 'erpnext.pengendalian_biaya.doctype.slip_pembayaran_subkon.slip_pembayaran_subkon.get_outstanding',
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
		frm.set_value("ppn", frm.doc.ppn_percent*frm.doc.paid/100);
		frm.refresh_field("ppn");

		frm.set_value("pph", frm.doc.pph_percent*frm.doc.paid/100);
		frm.refresh_field("pph");

		set_total(frm);
	},
	ppn_percent: function(frm){
		frm.set_value("ppn", frm.doc.ppn_percent*frm.doc.paid/100);
		frm.refresh_field("ppn");

		set_total(frm);
	},
	pph_percent: function(frm){
		frm.set_value("pph", frm.doc.pph_percent*frm.doc.paid/100);
		frm.refresh_field("pph");

		set_total(frm);
	},
	potongan: function(frm){
		set_total(frm);
	}
});

function set_total(frm){
	frm.set_value("total", frm.doc.paid+frm.doc.ppn-frm.doc.potongan);
	frm.refresh_field("total");
}