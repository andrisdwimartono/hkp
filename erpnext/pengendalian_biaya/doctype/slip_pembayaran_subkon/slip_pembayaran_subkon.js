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
		
		frm.set_query("pos_rap", "details", function(doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			if(row.rap == 1){
				if(cur_frm.doc.budget)
					return {
						query: "erpnext.accounts.doctype.budget_realization.budget_realization.get_pos_rap",
						filters: {
							'budget': cur_frm.doc.budget
						}
					}
			}else{
				return {
					filters: {
						'docstatus': 100
					}
				}
			}
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


frappe.ui.form.on("Form Payment Entry Account", "volume", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	get_budget(d);

});

frappe.ui.form.on("Form Payment Entry Account", "unit_price", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	get_budget(d);
});

function get_budget(d){
	var vol = d.unit_price?d.unit_price:0;
	var up = d.volume?d.volume:0;
	d.budget_amount = vol*up;
	d.budget_amount_submission = vol*up;
	cur_frm.refresh_field("details");
}

frappe.ui.form.on("Form Payment Entry Account", "budget_amount", function(frm, cdt, cdn) {
    var total_budget = 0;
	for(var i = 0; i < frm.doc.details.length; i++){
		var budget_amount=frm.doc.details[i].budget_amount?frm.doc.details[i].budget_amount:0;
		total_budget = total_budget+budget_amount;
	}
	frm.set_value("total_budget", total_budget);
	frm.refresh_field("total_budget");
});

frappe.ui.form.on("Form Payment Entry Account", "pos_rap", function(frm, cdt, cdn) {
    let d = locals[cdt][cdn];

	frappe.call({
		method: 'erpnext.accounts.doctype.form_payment_entry_supplier.form_payment_entry_supplier.check_budget',
		args: {
			'budget': frm.doc.budget,
			'pos_rap': d.pos_rap
		},
		callback: function(r) {
			if(r.message){
				var vals = r.message[0];
				d.duration = vals.duration+1;
				var vols = vals.volume;
				if(vals.volume_realization){
					vols = vals.volume-vals.volume_realization;	
				}
				d.volume = vols;
				d.unit_price = vals.unit_price;
				d.budget_amount = vals.budget_amount;
				d.budget_amount_submission = vals.budget_amount;
				d.account = vals.account;
				d.cost_center = vals.cost_center;
				d.description = vals.description;
				frm.refresh_field("details");
			}
		}
	});
});