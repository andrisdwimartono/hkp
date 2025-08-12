// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Form Payment Entry Project', {
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

		// if (frm.doc.__unsaved == 1)	{
		// 	frm.clear_table("pejabat");
		// 	var x = ["Direktur Operasi", "Estimasi", "Manager Logistik", "Manager Sekretariat", "Manager Keuangan"];
		// 	var y = ["DIR. OPS", "EST", "LOG", "SEK", "KEU"];
		// 	var z = ["Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui", "Mengetahui"];
		// 	for(var i = 0; i < x.length; i++){
		// 		let d = frm.add_child("pejabat");
		// 		d.jabatan = x[i];
		// 		d.jabatan_abbr = y[i];
		// 		d.aksi = z[i];
		// 		d.employee = "HR-EMP-00044";
		// 		d.user = "opshkp@gmail.com";
		// 	}
		// 	frm.refresh_fields("pejabat");
		// }else{
		// 	frm.disable_save();
		// 	frappe.call({
		// 		method: 'erpnext.projects.utils.get_next_process_rule',
		// 		args: {
		// 			'doctype': frm.doc.doctype,
		// 			'docname': frm.doc.name
		// 		},
		// 		callback: function(r) {
		// 			if(r.message){
		// 				var vals = r.message;
		// 				frm.add_custom_button(vals.aksi, function () {
		// 					frappe.prompt([
		// 						{
		// 							label: 'Status',
		// 							fieldname: 'status',
		// 							fieldtype: 'Select',
		// 							options: ["Yes", "No"],
		// 							default: "Yes",
		// 							reqd: 1
		// 						},
		// 						{
		// 							label: __('Comment'),
		// 							fieldname: 'comment',
		// 							fieldtype: 'Small Text'
		// 						},
		// 						{
		// 							label: 'process_rule_name',
		// 							fieldname: 'process_rule_name',
		// 							fieldtype: 'Data',
		// 							hidden: 1,
		// 							default: vals.name
		// 						},
		// 					], (values) => {
		// 						frappe.call({
		// 							method: 'erpnext.projects.utils.save_process_rule',
		// 							args: {
		// 								'docname': values.process_rule_name,
		// 								'status': values.status,
		// 								'comment': values.comment
		// 							},
		// 							callback: function(r) {
		// 								if(r.message){
		// 									frm.reload_doc();
		// 								}
		// 							}
		// 						});
		// 					},
		// 						vals.jabatan+' '+vals.aksi,
		// 						'Simpan'
		// 					);
		// 				}).removeClass("btn-default").addClass("btn-info");
		// 			}
		// 		}
		// 	});
		// }

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
	setup: function(frm) {
		frm.set_query("budget", function() {
			return {
				filters: {
					'project': frm.doc.project
				}
			};
		});

		frm.set_query("purchase_order", function() {
			return {
				filters: {
					'docstatus': 1
				}
			};
		});

		frm.set_query("hand_over_progress", function() {
			return {
				filters: {
					'docstatus': 1
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
		frappe.call({
			method: 'erpnext.accounts.doctype.form_payment_entry_project.form_payment_entry_project.get_details_hand_over_progress',
			args: {
				hand_over_progress: frm.doc.hand_over_progress
			},
			callback: function(r, rt) {
				if(r.message) {
					cur_frm.clear_table("details");
					refresh_field("details");
					$.each(r.message, function(i, d) {
						var c = frm.add_child("details");
						var vals = d;
						c.pos_rap = vals.pos_rap;
						c.rap = 0;
						c.volume = 1;
						c.unit_price = vals.unit_price;
						c.budget_amount = 0;
						c.budget_amount_submission = vals.budget_amount;
						c.remarks = "Progress ke-"+vals.progress_sequence
						refresh_field("details");
						cur_frm.set_value("project", vals.project);
						refresh_field("project");
						cur_frm.set_value("purpose", vals.job_name);
						refresh_field("purpose");
					});
				}
			}
		});
	},
	base_on: function(frm){
		var checklist = ["KONTRAK KERJA/ SPK", "KWITANSI/ PROGRESS FISIK", "CHECK LIST/LKPP/BERITA ACARA", "FAKTUR PAJAK"];
		var checklist2 = ["SPB/ SPJB/ MEMO BON", "NOTA/ KWITANSI", "TANDA TERIMA BARANG", "FAKTUR PAJAK"];
		cur_frm.clear_table("form_payment_entry_checklist");
		refresh_field("form_payment_entry_checklist");
		if(frm.doc.base_on == "Purchase Order"){
			for(var i = 0; i < checklist2.length; i++) {
				var c = frm.add_child("form_payment_entry_checklist");
				c.remark = checklist2[i];
				refresh_field("form_payment_entry_checklist");
			}
		}else if(frm.doc.base_on == "Hand Over Progress"){
			for(var i = 0; i < checklist.length; i++) {
				var c = frm.add_child("form_payment_entry_checklist");
				c.remark = checklist[i];
				refresh_field("form_payment_entry_checklist");
			}
		}
	},
	purchase_order: function(frm){
		frappe.call({
			method: 'erpnext.accounts.doctype.form_payment_entry_project.form_payment_entry_project.get_details_po',
			args: {
				purchase_order: frm.doc.purchase_order
			},
			callback: function(r, rt) {
				if(r.message) {
					cur_frm.clear_table("details");
					refresh_field("details");
					$.each(r.message, function(i, d) {
						var c = frm.add_child("details");
						var vals = d;
						c.pos_rap = vals.pos_rap;
						c.duration = vals.duration+1;
						c.rap = 0;
						var vols = vals.volume;
						if(vals.volume_realization){
							vols = vals.volume-vals.volume_realization;	
						}
						c.volume = vols;
						c.unit_price = vals.unit_price;
						c.budget_amount = 0;
						c.budget_amount_submission = vals.unit_price*vols;
						c.account = vals.account;
						c.cost_center = vals.cost_center;
						c.description = vals.description;
						refresh_field("details");
					});
				}
			}
		});
	},
	budget: function(frm){
		// frappe.call({
		// 	method: 'erpnext.accounts.doctype.form_payment_entry_project.form_payment_entry_project.get_details',
		// 	args: {
		// 		budget: frm.doc.budget
		// 	},
		// 	callback: function(r, rt) {
		// 		if(r.message) {
		// 			cur_frm.clear_table("details");
		// 			refresh_field("details");
		// 			$.each(r.message, function(i, d) {
		// 				var c = frm.add_child("details");
		// 				var vals = d;
		// 				c.pos_rap = vals.pos_rap;
		// 				c.duration = vals.duration+1;
		// 				var vols = vals.volume;
		// 				if(vals.volume_realization){
		// 					vols = vals.volume-vals.volume_realization;	
		// 				}
		// 				c.volume = vols;
		// 				c.unit_price = vals.unit_price;
		// 				c.budget_amount = vals.unit_price*vols;
		// 				c.account = vals.account;
		// 				c.cost_center = vals.cost_center;
		// 				c.description = vals.description;
		// 				refresh_field("details");
		// 			});
		// 		}
		// 	}
		// });
	}
});

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
		method: 'erpnext.accounts.doctype.form_payment_entry_project.form_payment_entry_project.check_budget',
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
				d.budget_amount = 0;
				d.budget_amount_submission = vals.budget_amount;
				d.account = vals.account;
				d.cost_center = vals.cost_center;
				d.description = vals.description;
				frm.refresh_field("details");
			}
		}
	});
});

// frappe.ui.form.on("Form Payment Entry Account", "approved_budget", function(frm, cdt, cdn) {
//     var total_budget = 0;
// 	var total_approved_budget = 0;
// 	for(var i = 0; i < frm.doc.details.length; i++){
// 		var budget=frm.doc.details[i].budget_amount?frm.doc.details[i].budget_amount:0;
// 		var approved_budget=frm.doc.details[i].approved_budget?frm.doc.details[i].approved_budget:0;
// 		total_budget = total_budget+budget;
// 		total_approved_budget = total_approved_budget+approved_budget;
// 	}
// 	frm.set_value("total_budget", total_budget);
// 	frm.set_value("total_approved_budget", total_approved_budget);
// 	frm.refresh_field("total_budget");
// 	frm.refresh_field("total_approved_budget");
// });