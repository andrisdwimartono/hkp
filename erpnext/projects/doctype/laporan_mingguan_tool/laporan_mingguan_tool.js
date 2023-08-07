// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt


frappe.ui.form.on('Laporan Mingguan Tool', {
	
	refresh: function(frm) {
		frm.set_value("sub_contract_hand_over", "SPK-2023-000001");
		frm.refresh_field("sub_contract_hand_over");

		//$(frm.fields_dict.abc.wrapper).html("<table><tr><td>ss</td></tr></table>aaa");
		//frm.set_value("result_html", "<table><tr><td>ss</td></tr></table>aaa");
		//frm.refresh_field("result_html");
		
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

		if(frm.doc.posting_date && frm.doc.week && frm.doc.sub_contract_hand_over){
			frm.trigger("set_sub_contract_weekly_progress");
		}
	},

	set_sub_contract_weekly_progress: function(frm){
		frappe.call({
			method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.get_sub_contract_weekly_progress',
			args: {
				'week': frm.doc.week,
				'sub_contract_hand_over': frm.doc.sub_contract_hand_over
			},
			callback: function(r) {
				if(r.message && r.message.length > 0){
					var vals = r.message;
					frm.set_value("sub_contract_weekly_progress", vals[0].name);
					frm.refresh_field("sub_contract_weekly_progress");
				}else{
					frm.set_value("sub_contract_weekly_progress", "");
					frm.refresh_field("sub_contract_weekly_progress");
				}
			}
		});

		frappe.call({
			method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.get_sub_contract_weekly_progress',
			args: {
				'week': parseInt(frm.doc.week)-1,
				'sub_contract_hand_over': frm.doc.sub_contract_hand_over
			},
			callback: function(r) {
				if(r.message && r.message.length > 0){
					var vals = r.message;
					frm.set_value("sub_contract_weekly_progress_last_week", vals[0].name);
					frm.refresh_field("sub_contract_weekly_progress_last_week");
				}else{
					frm.set_value("sub_contract_weekly_progress_last_week", "");
					frm.refresh_field("sub_contract_weekly_progress_last_week");
				}
			}
		});

		frappe.call({
			method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.get_sub_contract_weekly_progress_detail',
			args: {
				'week': frm.doc.week,
				'sub_contract_hand_over': frm.doc.sub_contract_hand_over
			},
			callback: function(r) {
				if(r.message && r.message.length > 0){
					frm.clear_table('sub_contract_weekly_progress_detail');
					for(var i = 0; i < r.message.length; i++){
						frm.add_child('sub_contract_weekly_progress_detail', {
							job_detail: r.message[i].job_detail,
							uom: r.message[i].uom,
							volume: r.message[i].volume,
							weight: r.message[i].weight,
							volume_plan_from_last_week: r.message[i].volume_plan_from_last_week,
							vol_next_week_plan: r.message[i].vol_next_week_plan,
							volume_cumulative_last_week: r.message[i].volume_cumulative_last_week,
							vol_this_week: r.message[i].vol_this_week,
							volume_cumulative_thist_week: r.message[i].volume_cumulative_thist_week,
							deviasi: r.message[i].deviasi
						});
					}
					frm.refresh_field('sub_contract_weekly_progress_detail');
				}
			}
		});
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
					frm.trigger("sub_contract_hand_over");
					if(frm.doc.posting_date && frm.doc.week && frm.doc.sub_contract_hand_over){
						frm.trigger("set_sub_contract_weekly_progress");
					}
				}
			}
		});
	},

	sub_contract_hand_over: function(frm) {
		if(frm.doc.posting_date && frm.doc.week && frm.doc.sub_contract_hand_over){
			frm.trigger("set_sub_contract_weekly_progress");
		}
		
		frm.doc.show_submit = false;
	},
});
