// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
zoomout();
frappe.ui.form.on('Laporan Mingguan Kendala Tool', {
	validate: function(frm){
		
	},
	refresh: function(frm) {
		// frm.set_value("sub_contract_hand_over", "SPK-2023-000003");
		// frm.refresh_field("sub_contract_hand_over");

		frm.doc.show_submit = false;
		frm.disable_save();
		frm.add_custom_button('Simpan', function () {
			frm.trigger("updating");
		});
		frm.add_custom_button('<svg class="icon  icon-sm" style=""><use class="" href="#icon-printer"></use></svg>', function () {
			if(frm.doc.sub_contract_weekly_progress){
				window.location.href = "/printview?doctype=Sub%20Contract%20Weekly%20Progress&name="+frm.doc.sub_contract_weekly_progress+"&format=Kendala%20Design&no_letterhead=0&letterhead=KOP%20HKP&settings=%7B%7D&_lang=id";
			}
			
		});

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
			method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.get_sub_contract_weekly_progress_detail2',
			args: {
				'week': frm.doc.week,
				'sub_contract_hand_over': frm.doc.sub_contract_hand_over
			},
			callback: function(r) {
				frm.clear_table('sub_contract_weekly_progress_detail');
				if(r.message && r.message.length > 0){
					for(var i = 0; i < r.message.length; i++){
						frm.add_child('sub_contract_weekly_progress_detail', {
							namex: r.message[i].name,
							job_detail: r.message[i].job_detail,
							obstacle: r.message[i].obstacle,
							analysis: r.message[i].analysis,
							resolve: r.message[i].resolve,
							pic: r.message[i].pic,
							resolve_target: r.message[i].resolve_target,
							document: r.message[i].document
						});
					}
				}
				frm.refresh_field('sub_contract_weekly_progress_detail');
				zoomout();
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

	updating: function(frm){
		var x = [];
		for(var i = 0; i < frm.doc.sub_contract_weekly_progress_detail.length; i ++){
			x.push({
				"namex":frm.doc.sub_contract_weekly_progress_detail[i].namex?frm.doc.sub_contract_weekly_progress_detail[i].namex:null,
				"idx": frm.doc.idx,
				"job_detail":frm.doc.sub_contract_weekly_progress_detail[i].job_detail,
				"obstacle": frm.doc.sub_contract_weekly_progress_detail[i].obstacle,
				"analysis": frm.doc.sub_contract_weekly_progress_detail[i].analysis,
				"resolve": frm.doc.sub_contract_weekly_progress_detail[i].resolve,
				"pic": frm.doc.sub_contract_weekly_progress_detail[i].pic,
				"resolve_target": frm.doc.sub_contract_weekly_progress_detail[i].resolve_target,
				"document": frm.doc.sub_contract_weekly_progress_detail[i].document
			});
		}
		frappe.call({
			method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.saving2',
			args: {
				"name":frm.doc.name?frm.doc.name:null,
				"sub_contract_hand_over":frm.doc.sub_contract_hand_over,
				"project":frm.doc.project,
				"sub_contract":frm.doc.sub_contract,
				"job_name":frm.doc.job_name,
				"posting_date":frm.doc.posting_date,
				"week":frm.doc.week,
				"contractor_name":frm.doc.contractor_name,
				"project_name":frm.doc.project_name,
				"pic_name":frm.doc.pic_name,
				"budget_amount":frm.doc.budget_amount,
				"sub_contract_weekly_progress":frm.doc.sub_contract_weekly_progress,
				"sub_contract_weekly_progress_last_week":frm.doc.sub_contract_weekly_progress_last_week,
				"sub_contract_weekly_progress_detail":x
			},
			callback: function(r) {
				if(r.message){
					var vals = r.message;
					frm.set_value("sub_contract_weekly_progress", vals);
					frm.refresh_field("sub_contract_weekly_progress");
					msgprint("Berhasil disimpan");
				}
			}
		});
	},
});


frappe.ui.form.on("Sub Contract Weekly Progress Details", {
	sub_contract_weekly_progress_detail_add: function(frm, dt, dn) {
        //console.log('added!');
		// $('[data-fieldname="job_detail"][title="Uraian Pekerjaan"]').css("font-size", "10px");
		zoomout();
		
		
		//row-index
    }
});

function zoomout(){
	$('.grid-static-col').css("font-size", "10px");
	$('.row-index').css("font-size", "10px");
	$('[data-doctype="Sub Contract Weekly Progress Details"]').css("font-size", "10px");
}