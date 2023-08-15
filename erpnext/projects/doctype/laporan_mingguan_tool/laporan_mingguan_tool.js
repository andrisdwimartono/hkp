// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
zoomout();
frappe.ui.form.on('Laporan Mingguan Tool', {
	validate: function(frm){
		
	},
	refresh: function(frm) {
		// frm.set_value("sub_contract_hand_over", "SPK-2023-000003");
		// frm.refresh_field("sub_contract_hand_over");

		//$(frm.fields_dict.abc.wrapper).html("<table><tr><td>ss</td></tr></table>aaa");
		//frm.set_value("result_html", "<table><tr><td>ss</td></tr></table>aaa");
		//frm.refresh_field("result_html");
		frm.doc.show_submit = false;
		//frm.doc.show_save = false;
		frm.disable_save();
		frm.add_custom_button('Simpan', function () {
			frm.trigger("updating");
		});
		frm.add_custom_button('<svg class="icon  icon-sm" style=""><use class="" href="#icon-printer"></use></svg>', function () {
			if(frm.doc.sub_contract_weekly_progress){
				window.location.href = "/printview?doctype=Sub%20Contract%20Weekly%20Progress&name="+frm.doc.sub_contract_weekly_progress+"&format=LKP%20Desgin&no_letterhead=0&letterhead=KOP%20HKP&settings=%7B%7D&_lang=id";
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
			method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.get_sub_contract_weekly_progress_detail',
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
							uom: r.message[i].uom,
							volume: r.message[i].volume,
							weight: r.message[i].weight,
							volume_plan_from_last_week: r.message[i].volume_plan_from_last_week,
							vol_next_week_plan: r.message[i].vol_next_week_plan,
							volume_cumulative_last_week: r.message[i].volume_cumulative_last_week,
							vol_this_week: r.message[i].vol_this_week,
							volume_cumulative_thist_week: r.message[i].volume_cumulative_thist_week,
							deviasi : r.message[i].volume_plan_from_last_week-r.message[i].vol_this_week
						});
						// $("div[data-fieldname='deviasi']").append("<input value='xxxxx' disabled class='input-with-feedback form-control input-sm'>");
						// $("div[data-fieldname='deviasi']").removeClass("col-xs-1");
						// $('[data-fieldname="sub_contract_weekly_progress_detail"]').html("aasdsss");
						//$('[data-fieldname="job_detail"]').html("aasdsss");
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
				"uom":frm.doc.sub_contract_weekly_progress_detail[i].uom,
				"volume":frm.doc.sub_contract_weekly_progress_detail[i].volume,
				"weight":frm.doc.sub_contract_weekly_progress_detail[i].weight,
				"volume_plan_from_last_week":frm.doc.sub_contract_weekly_progress_detail[i].volume_plan_from_last_week,
				"vol_next_week_plan":frm.doc.sub_contract_weekly_progress_detail[i].vol_next_week_plan,
				"volume_cumulative_last_week":frm.doc.sub_contract_weekly_progress_detail[i].volume_cumulative_last_week,
				"vol_this_week":frm.doc.sub_contract_weekly_progress_detail[i].vol_this_week,
				"volume_cumulative_thist_week":frm.doc.sub_contract_weekly_progress_detail[i].volume_cumulative_thist_week,
				"deviasi":frm.doc.sub_contract_weekly_progress_detail[i].deviasi
			});
		}
		frappe.call({
			method: 'erpnext.projects.doctype.sub_contract_weekly_progress.sub_contract_weekly_progress.saving',
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
    },
	vol_this_week: function(frm, dt, dn) {
		var d = locals[dt][dn];
		d.deviasi = d.volume_plan_from_last_week-d.vol_this_week;
		frm.refresh_field('sub_contract_weekly_progress_detail');
		d.volume_cumulative_thist_week = d.volume_cumulative_last_week+d.vol_this_week;
		frm.refresh_field('volume_cumulative_thist_week');
		zoomout();
	},
	volume_plan_from_last_week: function(frm, dt, dn) {
		var d = locals[dt][dn];
		d.deviasi = d.volume_plan_from_last_week-d.vol_this_week;
		frm.refresh_field('sub_contract_weekly_progress_detail');
		d.volume_cumulative_thist_week = d.volume_cumulative_last_week+d.vol_this_week;
		frm.refresh_field('volume_cumulative_thist_week');
		zoomout();
	}
});

function zoomout(){
	$('.grid-static-col').css("font-size", "10px");
	$('.row-index').css("font-size", "10px");
	$('[data-doctype="Sub Contract Weekly Progress Details"]').css("font-size", "10px");

	//ganti label
	$('.grid-heading-row>.grid-row>.data-row>[data-fieldname="volume"]>.static-area').html("Volume");
	$('.grid-heading-row>.grid-row>.data-row>[data-fieldname="uom"]>.static-area').html("Satuan");
	$('.grid-heading-row>.grid-row>.data-row>[data-fieldname="volume_plan_from_last_week"]>.static-area').html("<div>Rencana</div><div>Minggu Ini</div>");
	$('.grid-heading-row>.grid-row>.data-row>[data-fieldname="vol_next_week_plan"]>.static-area').html("<div>Rencana</div><div>Minggu Depan</div>");
	$('.grid-heading-row>.grid-row>.data-row>[data-fieldname="volume_cumulative_last_week"]>.static-area').html("<div>Kumulatif</div><div>Minggu Lalu</div>");
	$('.grid-heading-row>.grid-row>.data-row>[data-fieldname="vol_this_week"]>.static-area').html("<div>Realisasi</div><div>Minggu Ini</div>");
	$('.grid-heading-row>.grid-row>.data-row>[data-fieldname="volume_cumulative_thist_week"]>.static-area').html("<div>Kumulatif</div><div>Minggu Ini</div>");
}