// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Surat Permintaan Harga', {
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			var surat_permintaan_harga_dokumen = [
				"Brosur",
				"Hasil Routine Test",
				"Spesifikasi Teknik (Technical Particular Guaranted)",
				"Type Test",
				"Reference List",
				"Kelengkapan Administrasi Pembelian",
				"Sertifikasi ISO",
				"Surat Garansi",
				"Cara Pembayaran dan Discont Maksimal",
				"End User / Letter Of Satisfaction",
				"Franko dan Waktu Penyerahan Barang"
			];
			frm.clear_table("surat_permintaan_harga_dokumen");
			for(var i = 0; i < surat_permintaan_harga_dokumen.length; i++){
				var pr = frm.add_child("surat_permintaan_harga_dokumen");
				pr.document = surat_permintaan_harga_dokumen[i];
			}
			frm.refresh_field("surat_permintaan_harga_dokumen");

			var surat_permintaan_harga_kirim = [
				"Faksimili",
				"Pos",
				"Email"
			];
			frm.clear_table("surat_permintaan_harga_kirim");
			for(var i = 0; i < surat_permintaan_harga_kirim.length; i++){
				var pr = frm.add_child("surat_permintaan_harga_kirim");
				pr.pengiriman_via = surat_permintaan_harga_kirim[i];
			}
			frm.refresh_field("surat_permintaan_harga_kirim");

			var surat_permintaan_harga_lampiran = [
				"Copy Rencana Kerja dan Syarat (RKS)",
				"Spesifikasi teknik",
				"Gambar tender",
				"Kebutuhan material (BQ)"
			];
			frm.clear_table("surat_permintaan_harga_lampiran");
			for(var i = 0; i < surat_permintaan_harga_lampiran.length; i++){
				var pr = frm.add_child("surat_permintaan_harga_lampiran");
				pr.lampiran = surat_permintaan_harga_lampiran[i];
			}
			frm.refresh_field("surat_permintaan_harga_lampiran");
		}
	}
});
