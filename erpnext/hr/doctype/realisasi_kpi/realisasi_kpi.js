// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Realisasi KPI', {
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: {
					user_id: frappe.session.user
				}
			};
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
	}else{
		d.score = 50;
	}

	d.final_score = d.weight*d.score/100;

    cur_frm.refresh_field("detail");
});