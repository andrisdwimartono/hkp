// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

var detail = [];
frappe.ui.form.on('KPI Karyawan', {
	validate: function(frm){
		if(frm.doc.tahun){
			frappe.throw("Tidak boleh simpan karena difilter")
		}
	},
	refresh: function(frm) {

		if (frm.doc.__unsaved == 1)	{
			// frm.clear_table("detail");
			// var bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];
			// for(var i = 0; i < bulan.length; i++){
			// 	var pr = frm.add_child("detail");
			// 	pr.bulan = bulan[i];
			// }
			// frm.refresh_field("detail");
		}
		//cur_frm.fields_dict['detail'].$wrapper.find('.grid-add-row').addClass('d-none');
		detail = frm.doc.detail;
	},
	tahun: function(frm){
		if(frm.doc.tahun){
			frm.clear_table("detail");
			frm.refresh_field("detail");
			for(var i = 0; i < detail.length; i++){
				if(detail[i].tahun == frm.doc.tahun){
					var pr = frm.add_child("detail");
					pr.bulan = detail[i].bulan;
					pr.tahun = detail[i].tahun;
					pr.document = detail[i].document;
				}
			}
			frm.refresh_field("detail");
		}else{
			frm.clear_table("detail");
			frm.refresh_field("detail");
			for(var i = 0; i < detail.length; i++){
				var pr = frm.add_child("detail");
				pr.bulan = detail[i].bulan;
				pr.tahun = detail[i].tahun;
				pr.document = detail[i].document;
			}
			frm.refresh_field("detail");
		}
	}
});


