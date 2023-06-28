// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Berita Acara Klarifikasi dan Negosiasi', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			var c = frm.add_child("dasar_berita_acara_klarifikasi_dan_negosiasi");
			c.dasar = "Surat PT. Hasta Karya Perdana No  tanggal  perihal ";
			var d = frm.add_child("dasar_berita_acara_klarifikasi_dan_negosiasi");
			d.dasar = "E-mail  tanggal  perihal ";
			var e = frm.add_child("dasar_berita_acara_klarifikasi_dan_negosiasi");
			e.dasar = "Telepon  tanggal ";
			refresh_field("dasar_berita_acara_klarifikasi_dan_negosiasi");
		}
	}
});
