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
			
			var x = ["construction@hastaindonesia.com", "corporate@hastaindonesia.com", "satrio@hastaindonesia.com"];
			var y = ["to", "cc", "cc"];
			for(var i = 0; i < x.length; i++){
				var c = frm.add_child("email");
				c.pemilik = "HKP";
				c.email = x[i];
				c.jenis = y[i];
			}
			frm.refresh_field("email");
		}
		
		if(frm.doc.syarat_pembayaran.length == 0){
			
		}
	},
	mulai_pelaksanaan: function(frm){
		var x = frappe.datetime.get_day_diff(frm.doc.selesai_pelaksanaan, frm.doc.mulai_pelaksanaan);
		frm.set_value("lama_pelaksanaan", x);
		frm.refresh_field("lama_pelaksanaan");
	},
	selesai_pelaksanaan: function(frm){
		var x = frappe.datetime.get_day_diff(frm.doc.selesai_pelaksanaan, frm.doc.mulai_pelaksanaan);
		frm.set_value("lama_pelaksanaan", x);
		frm.refresh_field("lama_pelaksanaan");
	},
	jenis_pembayaran: function(frm){
		if(frm.doc.jenis_pembayaran == "Persen"){
			frm.trigger("uang_muka");
		}else{
			frm.trigger("uang_muka_nominal");
		}
	},
	uang_muka: function(frm){
		var x = frm.doc.uang_muka*frm.doc.harga_pekerjaan;
		frm.set_value("uang_muka_total", x);
		frm.refresh_field("uang_muka_total");
	},
	harga_pekerjaan: function(frm){
		var x = frm.doc.uang_muka*frm.doc.harga_pekerjaan;
		frm.set_value("uang_muka_total", x);
		frm.refresh_field("uang_muka_total");

		var y = frm.doc.retensi*frm.doc.harga_pekerjaan;
		frm.set_value("retensi_total", y);
		frm.refresh_field("retensi_total");
	},
	uang_muka_nominal: function(frm){
		var x = frm.doc.uang_muka_nominal;
		frm.set_value("uang_muka_total", x);
		frm.refresh_field("uang_muka_total");
	},
	jenis_retensi: function(frm){
		if(frm.doc.jenis_retensi == "Persen"){
			frm.trigger("retensi");
		}else{
			frm.trigger("retensi_nominal");
		}
	},
	retensi: function(frm){
		var x = frm.doc.retensi*frm.doc.harga_pekerjaan;
		frm.set_value("retensi_total", x);
		frm.refresh_field("retensi_total");
	},
	retensi_nominal: function(frm){
		var x = frm.doc.retensi_nominal;
		frm.set_value("retensi_total", x);
		frm.refresh_field("retensi_total");
	}
});
