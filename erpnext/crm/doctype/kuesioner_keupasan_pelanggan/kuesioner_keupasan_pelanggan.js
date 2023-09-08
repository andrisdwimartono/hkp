// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Kuesioner Keupasan Pelanggan', {
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			var proses_persiapan_pelaksanaan = [
				"Bagaimana pelayanan staf proyek kami mempersiapkan pelaksanaan proyek sesuai dengan harapan Bapak/Ibu.",
				"Bagaimana kesigapan (responsiveness) staf kami dalam mempersiapkan pelaksanaan proyek Bapak/Ibu.",
				"Bagaimana Ketepatan waktu staf kami dalam mempersiapkan pelaksanaan pekerjaan.",
				"Bagaimana Intensitas komunikasi staf proyek kami dalam mempersiapkan pelaksanaan  proyek sesuai dengan keinginan Bapak/Ibu."
			];
			frm.clear_table("proses_persiapan_pelaksanaan");
			for(var i = 0; i < proses_persiapan_pelaksanaan.length; i++){
				var pr = frm.add_child("proses_persiapan_pelaksanaan");
				pr.pertanyaan = proses_persiapan_pelaksanaan[i];
			}
			frm.refresh_field("proses_persiapan_pelaksanaan");


			var pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan = [
				"Bagaimana staf kami melakukan komunikasi dengan staf Bapak/Ibu.",
				"Bagaimana staf kami melakukan koordinasi pekerjaan dengan Staf Bapak/Ibu.",
				"Bagaimana kesigapan (responsiveness) staf kami dalam memberikan solusi terhadap keluhan Bapak/Ibu.",
				"Bagaimana tingkat kehadiran staf kami di lapangan.",
				"Bagaimana tingkat kehadiran staf proyek kami memenuhi undangan pada rapat-rapat proyek lapangan.",
				"Bagaimana motivasi kerja staf kami dalam pelaksanaan proyek.",
				"Kompetensi tenaga kerja yang kami memiliki sesuai dengan  bidang yang dikerjakannya.",
				"Kemudahan dalam menghubungi staf proyek kami dilapangan sesuai dengan yang Bapak/Ibu perlukan.",
				"Penampilan fisik pekerja kami, sesuai dengan pekerjaan yang Bapak/Ibu percayakan kepada perusahaan kami.",
				"Kualitas material yang kami sediakan sesuai dengan dokumen kontrak.",
				"Kelengkapan alat kerja yang kami pergunakan sesuai dengan lingkup pekerjaan dalam kontrak.",
				"Kelengkapan sarana kerja yang kami pergunakan sesuai dengan  lingkup pekerjaan dalam kontrak.",
				"Kualitas sarana kerja yang kami pergunakansesuai dengan  lingkup pekerjaan dalam kontrak.",
				"Metode kerja yang kami pergunakan sesuai dengan lingkup kontrak.",
				"Kecermatan kerja staf kami di lapangan, sehingga tidak ada  pekerjaan ulang (rework).",
				"Mutu Pengerjaan administrasi proyek yang dikerjakan staf kami.",
				"Keluwesan/fleksibelitas kerja staf kami di lapangan  sesuai dengan keinginan Bapak/Ibu.",
				"Tingkat kepedulian yang tinggi staf kami pada lingkungan kerja."
			];
			frm.clear_table("pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan");
			for(var i = 0; i < pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan.length; i++){
				var pr = frm.add_child("pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan");
				pr.pertanyaan = pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan[i];
			}
			frm.refresh_field("pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan");


			var akhir_pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan = [
				"Bagaimana pendapat Bapak/Ibu terhadap kinerja kami secara umum.",
				"Bagaimana pendapat Bapak/Ibu terhadap harga proyek dibandingkan dengan kecepatan waktu pelaksanaan.",
				"Bagaimana pendapat Bapak/Ibu terhadap harga proyek dibandingkan dengan mutu kinerja kami secara umum.",
				"Bagaimana pendapat Bapak/Ibu terhadap harga proyek dibandingkan dengan mutu material yang kami supply.",
				"Dalam pelaksanaan proyek ini, karyawan perusahaan kami yang terkait dengan pelaksanaan proyek, telah memberikan pelayanan yang baik kepada Bapak/Ibu."
			];
			frm.clear_table("akhir_pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan");
			for(var i = 0; i < akhir_pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan.length; i++){
				var pr = frm.add_child("akhir_pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan");
				pr.pertanyaan = akhir_pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan[i];
			}
			frm.refresh_field("akhir_pelaksanaan_pekerjaan_dan_serah_terima_pekerjaan");
		}
	}
});
