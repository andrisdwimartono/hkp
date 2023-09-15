// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('KUESIONER LAPANGAN', {
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			var bagian_a_pertanyaan = [
				"Bagaimana komunikasi kami di dalam pelaksanaan proyek ini.",
				"Bagaimana koordinasi kami di dalam pelaksanaan proyek ini.",
				"Bagaimana kesigapan staf kami dalam melaksanakan instruksi/saran-saran Bapal/Ibu.",
				"Bagaimana sikap kerja para staf kami dalam melaksanakan proyek ini.",
				"Bagaimana motivasi kerja staf kami untuk memberikan pelayanan yang baik dalam pelaksanaan proyek ini.",
				"Secara umum bagaimana tingkat kompetensi staf kami di lapangan."
			];
			frm.clear_table("bagian_a_pertanyaan");
			for(var i = 0; i < bagian_a_pertanyaan.length; i++){
				var pr = frm.add_child("bagian_a_pertanyaan");
				pr.pertanyaan = bagian_a_pertanyaan[i];
			}
			frm.refresh_field("bagian_a_pertanyaan");

			var bagian_b_pertanyaan = [
				"Bagaimana menurut Bapak/Ibu mutu material yang kami pergunakan dalam proyek ini.",
				"Bagaimana ketepatan waktu pengiriman material ke lapangan."
			];
			frm.clear_table("bagian_b_pertanyaan");
			for(var i = 0; i < bagian_b_pertanyaan.length; i++){
				var pr = frm.add_child("bagian_b_pertanyaan");
				pr.pertanyaan = bagian_b_pertanyaan[i];
			}
			frm.refresh_field("bagian_b_pertanyaan");

			var bagian_c_pertanyaan = [
				"Bagaimana kelengkapan peralatan kerja kami di dalam pelaksanaan proyek ini.",
				"Bagaimana kelengkapan peralatan K3 yang kami pergunakan di dalam pelaksanaan proyek ini."
			];
			frm.clear_table("bagian_c_pertanyaan");
			for(var i = 0; i < bagian_c_pertanyaan.length; i++){
				var pr = frm.add_child("bagian_c_pertanyaan");
				pr.pertanyaan = bagian_c_pertanyaan[i];
			}
			frm.refresh_field("bagian_c_pertanyaan");

			var bagian_d_pertanyaan = [
				"Bagaimana kesesuaian dan ketepatan penggunaan metode kerja yang digunakan dalam proyek ini."
			];
			frm.clear_table("bagian_d_pertanyaan");
			for(var i = 0; i < bagian_d_pertanyaan.length; i++){
				var pr = frm.add_child("bagian_d_pertanyaan");
				pr.pertanyaan = bagian_d_pertanyaan[i];
			}
			frm.refresh_field("bagian_d_pertanyaan");

			var bagian_e_pertanyaan = [
				"Menurut Bapak/Ibu, bagaimana dukungan keuangan kami dalam melaksanakan proyek ini"
			];
			frm.clear_table("bagian_e_pertanyaan");
			for(var i = 0; i < bagian_e_pertanyaan.length; i++){
				var pr = frm.add_child("bagian_e_pertanyaan");
				pr.pertanyaan = bagian_e_pertanyaan[i];
			}
			frm.refresh_field("bagian_e_pertanyaan");

			var bagian_f_pertanyaan = [
				"Secara umum bagaimana kemampuan staf kami dalam mengerjakan proses administrasi, laporan aktivitas proyek dan dokumentasi dalam proyek ini",
				"Secara umum bagaimana kemampuan manajerial staf kami dalam melaksanakan proyek ini."
			];
			frm.clear_table("bagian_f_pertanyaan");
			for(var i = 0; i < bagian_f_pertanyaan.length; i++){
				var pr = frm.add_child("bagian_f_pertanyaan");
				pr.pertanyaan = bagian_f_pertanyaan[i];
			}
			frm.refresh_field("bagian_f_pertanyaan");
		}
	}
});
