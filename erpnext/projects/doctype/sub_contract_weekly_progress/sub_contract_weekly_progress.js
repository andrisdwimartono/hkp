// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.ui.form.on('Sub Contract Weekly Progress', {
	refresh: function(frm) {
		// console.log(frm.fields_dict.start_week.datepicker)
		// frm.fields_dict.end_week.datepicker.update({
        //     maxDate: '2023-06-26'
        // });
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
	master_sub_contract_weekly_progress: function(frm){
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
