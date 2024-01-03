// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Realisasi Anggaran Non Proyek', {
	setup: function(frm) {
		frm.set_query("form_payment_entry", function() {
			return {
				filters: {
					'docstatus': 1
				}
			};
		});
	},
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			if(!frm.doc.process_rules){
				frm.clear_table("process_rules");
				frappe.call({
					method: 'erpnext.projects.utils.get_process_rules',
					args: {
						'doctype': frm.doc.doctype
					},
					callback: function(r) {
						if(r.message){
							var vals = r.message;
							for(var i = 0; i < vals.length; i++){
								var pr = frm.add_child("process_rules");
								pr.jabatan = vals[i].jabatan;
								pr.jabatan_abbr = vals[i].jabatan_abbr;
								pr.state = vals[i].state;
								pr.employee = vals[i].employee;
								pr.initial = vals[i].initial;
								pr.employee_name = vals[i].employee_name;
								pr.user = vals[i].user;
							}
							frm.refresh_field("process_rules");
						}
					}
				});
			}
		}else{
			
		}
		cur_frm.fields_dict['process_rules'].$wrapper.find('.grid-add-row').addClass('d-none');
		
		if(frm.doc.posting_date){
			frappe.call({
				method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.check_week',
				args: {
					'posting_date': frm.doc.posting_date
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
	posting_date: function(frm) {
		if(frm.doc.posting_date){
			frappe.call({
				method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.check_week',
				args: {
					'posting_date': frm.doc.posting_date
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
	form_payment_entry: function(frm){
		frm.clear_table("detail");
		frappe.call({
			method: 'erpnext.accounts.doctype.form_payment_entry.form_payment_entry.get_detail',
			args: {
				form_payment_entry: frm.doc.form_payment_entry
			},
			callback: function(r, rt) {
				if(r.message) {
					$.each(r.message, function(i, d) {
						var vals = d;
						console.log(vals)
						var c = frm.add_child("detail");
						c.pos_rap = vals.pos_rap;
						c.duration = vals.duration;
						c.volume = vals.volume;
						c.unit_price = vals.unit_price;
						c.budget_amount = vals.budget_amount;
						c.account = vals.account;
						c.cost_center = vals.cost_center;
						c.description = vals.description;
						refresh_field("detail");
					});

				}
			}
		});
	}
});
