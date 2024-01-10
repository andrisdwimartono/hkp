// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('LAPORAN AKTIVITAS DI LUAR KANTOR', {
	// refresh: function(frm) {

	// },
	alamat: function(frm){
		if(frm.doc.alamat.includes("<br>")){
			var al = frm.doc.alamat.replace("<br>", "\n");
			al= al.replace("\n\n", "\n");
			frm.set_value("alamat", al);
			refresh_field("alamat");
		}
	}
});
