// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Realisasi KPI', {
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
	},
	setup: function(frm) {
		frm.set_query("employee", function() {
			if(frappe.session.user != "Administrator"){
				return {
					filters: {
						user_id: frappe.session.user
					}
				};
			}
		});
	},
	designation: function(frm){
		frm.clear_table("detail");
		frappe.call({
			method: 'erpnext.hr.utils.get_designation_kpi',
			args: {
				'designation': frm.doc.designation
			},
			callback: function(r) {
				if(r.message){
					var vals = r.message;
					for(var i = 0; i < vals.length; i++){
						var pr = frm.add_child("detail");
						pr.kpi = vals[i].kpi;
						pr.description = vals[i].description;
						pr.aktivitas_pekerjaan = vals[i].aktivitas_pekerjaan;
						pr.target = vals[i].target;
						pr.weight = vals[i].weight;
						pr.type = vals[i].type;
					}
					frm.refresh_field("detail");
				}
			}
		});
	}
});

frappe.ui.form.on("Realisasi KPI Detail", "actual", function(frm, dt, dn) {
    let d = locals[dt][dn]
	if(d.type == "Higher is Better"){
		d.achievement = (d.actual/d.target)*100;
	}else{
		// Lower is Better
		// Nilai actual lebih kecil, maka lebih baik! Contoh waktu pengerjaan, jumlah keluhan dll
		d.achievement = (d.target/d.actual)*100;
	}
    

	if(d.achievement > 100){
		d.score = 100;
	}else if (d.achievement == 100){
		d.score = 90;
	}else if (d.achievement >= 90){
		d.score = 80;
	}else if (d.achievement <= 90 && d.achievement >= 50){
		d.score = 50;
	}else{
		d.score = 0;
	}

	d.final_score = d.weight*d.score/100;

    cur_frm.refresh_field("detail");
});