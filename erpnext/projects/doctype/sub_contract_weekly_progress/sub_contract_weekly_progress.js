// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.ui.form.on('Sub Contract Weekly Progress', {
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
		if(frm.doc.posting_date && !frm.doc.week){
			frappe.call({
				method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.check_week',
				args: {
					'posting_date': frm.doc.posting_date
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						frm.set_value("week", vals);
						frm.refresh_field("week");
					}
				}
			});
		}
	},
	master_item_pekerjaan: function(frm){
		//get detail last week
		// console.log(frm.doc.master_item_pekerjaan)
		if(frm.doc.master_item_pekerjaan && frm.doc.sub_contract_hand_over && frm.doc.week){
			frappe.call({
				method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.check_last_week',
				args: {
					'master_item_pekerjaan': frm.doc.master_item_pekerjaan,
					'sub_contract_hand_over': frm.doc.sub_contract_hand_over,
					'week': frm.doc.week
				},
				callback: function(r) {
					if(r.message){
						frm.clear_table("sub_contract_weekly_progress_detail");
						for(var x = 0; x < r.message.length; x++){
							let row = frm.add_child("sub_contract_weekly_progress_detail");
							row.job_detail = r.message[x].job_detail;
							row.obstacle = r.message[x].obstacle;
	
							row.analysis = r.message[x].analysis;
							row.resolve = r.message[x].resolve;
							row.pic = r.message[x].pic;
							row.resolve_target = r.message[x].resolve_target;
							row.volume_plan_from_last_week = r.message[x].vol_next_week_plan;
							row.volume_cumulative_last_week = r.message[x].tot_vol_this_week;
						}
						frm.refresh_field("sub_contract_weekly_progress_detail");
					}
				}
			});
		}
	},
	sub_contract_hand_over: function(frm){
		//get detail last week
		// console.log(frm.doc.master_sub_contract_weekly_progress)
		if(frm.doc.master_sub_contract_weekly_progress && frm.doc.sub_contract_hand_over && frm.doc.week){
			frappe.call({
				method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.check_last_week',
				args: {
					'master_sub_contract_weekly_progress': frm.doc.master_sub_contract_weekly_progress,
					'sub_contract_hand_over': frm.doc.sub_contract_hand_over,
					'week': frm.doc.week
				},
				callback: function(r) {
					if(r.message){
						frm.clear_table("sub_contract_weekly_progress_detail");
						for(var x = 0; x < r.message.length; x++){
							let row = frm.add_child("sub_contract_weekly_progress_detail");
							row.job_detail = r.message[x].job_detail;
							row.obstacle = r.message[x].obstacle;
	
							row.analysis = r.message[x].analysis;
							row.resolve = r.message[x].resolve;
							row.pic = r.message[x].pic;
							row.resolve_target = r.message[x].resolve_target;
							row.volume_plan_from_last_week = r.message[x].vol_next_week_plan;
							row.volume_cumulative_last_week = r.message[x].tot_vol_this_week;
						}
						frm.refresh_field("sub_contract_weekly_progress_detail");
					}
				}
			});
		}
	},
	posting_date: function(frm){
		frappe.call({
			method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.check_week',
			args: {
				'posting_date': frm.doc.posting_date
			},
			callback: function(r) {
				if(r.message){
					var vals = r.message;
					frm.set_value("week", vals);
					frm.refresh_field("week");
					frm.trigger("sub_contract_hand_over")
				}
			}
		});
	}
});
