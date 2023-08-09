// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Berita Acara Klarifikasi dan Negosiasi', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			var c = frm.add_child("syarat_pembayaran");
			c.hal = "Kwintasi";
			var d = frm.add_child("syarat_pembayaran");
			d.hal = "Laporan Kemajuan Phisik Lapangan.";
			var e = frm.add_child("syarat_pembayaran");
			e.hal = "Check List Pekerjaan.";
			var f = frm.add_child("syarat_pembayaran");
			f.hal = "B.A Pemeriksaan pekerjaan.";
			var g = frm.add_child("syarat_pembayaran");
			g.hal = "Foto Dokumentasi.";
			frm.refresh_field("syarat_pembayaran");
		}
		if(frm.doc.syarat_pembayaran.length == 0){
			
		}
	}
});
