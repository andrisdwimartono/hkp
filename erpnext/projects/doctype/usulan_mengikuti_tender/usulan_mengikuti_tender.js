// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('USULAN MENGIKUTI TENDER', {
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			var x = ["ADMINISTRASI", "TEKNIS", "PERALATAN", "SPESIFIKASI MATERIAL", "TENAGA KERJA", "PENGALAMAN KERJA", "PERSAINGAN", "LOKASI"];
			for(var i = 0; i < x.length; i++){
				let d = frm.add_child("tinjauan");
				d.tinjauan = x[i];
			}
			
			frm.refresh_fields("tinjauan");
		}
	}
});
