// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('DAFTAR PERIKSA SAAT KUNJUNGAN LAPANGAN', {
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			if(!frm.doc.manajerial){
				var uraian = [
					'Jadwal pekerjaan (kurva-s dan pms), gambar kerja, metode kerja, HSE Plan disajikan dengan baik ke seluruh pemangku kebijakan',
					'Salinan Buku kontrak',
					'Laporan harian, mingguan, dan bulanan',
					'Pelaksanaan pekerjaan yang tepat mutu dan waktu',
					'Patuh K3L di lokasi pekerjaan'
				]
				var kriteria = [
					'Semua dicetak di dinding kantor dan dapat terbaca dengan baik',
					'Buku kontrak tertata rapi di lemari',
					'Seluruh laporan diterima oleh direksi dan pengawas pekerjaan, tertandatangani, dan terarsip dengan baik',
					'Pekrerjaan dilaksanakan sesuai dengan metode kerja dan penilaian risiko yang ada',
					'Seluruh direksi lapangan dan pekerja menggunakan APD yang sesuai dan mematuhi standar dan ketentuan K3L yang ada (zero accident)'

				]
				frm.clear_table("manajerial");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("manajerial");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("manajerial");
			}

			if(!frm.doc.sdm){
				var uraian = [
					'Direksi lapangan beraktivitas di lokasi dengan rapi',
					'Budaya dan nilai-nilai perusahaan terimplementasikan dengan baik di lapangan'
				]
				var kriteria = [
					'Direksi pekerjaan menggunakan atribut perusahaan yang sesuai',
					'Direksi pekerjaan memahami dan memaknai budaya dan nilainilai perusahaan'
				]
				frm.clear_table("sdm");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("sdm");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("sdm");
			}

			if(!frm.doc.k3l){
				var uraian = [
					'Seluruh pekerja, pengawas lapangan, dan tamu menggunakan APD yang sesuai',
					'Seluruh pekerja, pengawas lapangan, dan tamu memahami dan mengerti kebijakan K3L yang ada di lokasi',
					'Terdapat zonasi kerja di lokasi',
					'Terpasang rambu dan pengaman yang sesuai dengan lingkup pekerjaan di lokasi',
					'Tersedia tempat sampah di lokasi, site office, dan gudang',
					'Seluruh pekerja, pengawas lapangan, dan tamu berkontribusi pada kebersihan dan keamanan lingkungan',
					'Seluruh pekerja, pengawas lapangan, dan tamu tidak merokok di lokasi pekerjaan',
					'Barak pekerja dalam kondisi baik',
					'Terpasang bendera K3L, perusahaan, dan Indonesia',
					'Terpasang LOTO',
					'Tersedia sarana kecelakaan kerja dan tanggap darurat'
				]
				var kriteria = [
					'Tersedia cukup APD dan dalam kondisi yang baik untuk seluruh pekerja, pengawas lapangan, dan dipakai dengan sesuai',
					'Safety briefing rutin setiap pagi/dilakukan setiap ada pekerja,pengawas lapangan dan tamu baru',
					'Terdapat denah zonasi area kerja di lokasi dan terimplementasi',
					'Rambu dan pengaman terpasang jelas, layak, dan sesuai',
					'Tempat sampah diberi plastik/tempat sampah tong besi',
					'Tidak membuang sampah sembarangan, ada program pembersihan area kerja setelah bekerja',
					'Ada area khusus merokok, tidak ada bungkus dan puntung rokok di lokasi pekerjaan',
					'Barak pekerja dalam kondisi layak dan bersih',
					'Terpasang bendera K3L, perusahaan, dan Indonesia dengan ukuran yang sesuai',
					'Loto terpasang pada setiap alat/barang yang berpotensi bahaya sebelum dioperasikan',
					'Terdapat perlengkapan P3K , kotak obat, dan sistem penanganan kondisi darurat di lokasi. Ada struktur organisasi K3L di lokasi'
				]
				frm.clear_table("k3l");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("k3l");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("k3l");
			}

			if(!frm.doc.kelengkapan_organisasi){
				var uraian = [
					'Buku tamu dan logbook',
					'Papan tulis berisi catatan aktivitas dan pemantauan pekerjaan',
					'Jadwal uji tekan sampel beton',
					'Struktur Organisasi',
					'Gambar Kerja'
				]
				var kriteria = [
					'Terisi oleh seluruh tamu',
					'Aktivitas yg tetulis terkini dan jelas penulisannya',
					'Jadwal yang terisi jelas dan dapat dilaksanakan dengan sesuai',
					'Tercantum yang terkini ',
					'Tercetak jelas dan terkini'
				]
				frm.clear_table("kelengkapan_organisasi");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("kelengkapan_organisasi");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("kelengkapan_organisasi");
			}

			if(!frm.doc.sarana_kerja_teknologi){
				var uraian = [
					'Komputer (laptop dan PC)',
					'Printer A4',
					'Printer A3'
				]
				var kriteria = [
					'Bersih, dirawat dengan baik, dan beroperasi dengan baik',
					'Bersih, dirawat dengan baik, dan beroperasi dengan baik',
					'Bersih, dirawat dengan baik, dan beroperasi dengan baik'
				]
				frm.clear_table("sarana_kerja_teknologi");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("sarana_kerja_teknologi");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("sarana_kerja_teknologi");
			}

			if(!frm.doc.sarana_kerja_prasarana){
				var uraian = [
					'Meja & Kursi',
					'Rak ordner'
				]
				var kriteria = [
					'Bersih, dirawat dengan baik, dan dipakai dengan baik',
					'Bersih, dirawat dengan baik, dan dipakai dengan baik'
				]
				frm.clear_table("sarana_kerja_prasarana");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("sarana_kerja_prasarana");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("sarana_kerja_prasarana");
			}

			if(!frm.doc.sarana_transportasi){
				var uraian = [
					'Sepeda Motor',
					'Mobil'
				]
				var kriteria = [
					'Bersih, dirawat dengan baik, dan dipakai dengan baik',
					'Bersih, dirawat dengan baik, dan dipakai dengan baik'
				]
				frm.clear_table("sarana_transportasi");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("sarana_transportasi");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("sarana_transportasi");
			}

			if(!frm.doc.alat_kerja){
				var uraian = [
					'Alat survei topografi',
					'Perkakas dan APD',
					'HT'
				]
				var kriteria = [
					'Kalibrasi aktif, dirawat dan dipakai dengan baik',
					'Bersih, dirawat dengan baik, dan dipakai dengan baik',
					'Bersih, dirawat dengan baik, dan dipakai dengan baik'
				]
				frm.clear_table("alat_kerja");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("alat_kerja");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("alat_kerja");
			}

			if(!frm.doc.gudang){
				var uraian = [
					'Kartu stok/laporan stok barang',
					'Penyimpanan barang'
				]
				var kriteria = [
					'Terisi dengan baik, lengkap, dilaporkan kepada dept.logistik secara mingguan, dan dapat dipertanggungjawabkan',
					'Barang disimpan dengan baik, tertata, dan aman sesuai site dan warehouse management yang baik'
				]
				frm.clear_table("gudang");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("gudang");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("gudang");
			}

			if(!frm.doc.kebersihan_dan_kenyamanan){
				var uraian = [
					'Mess',
					'Gudang Tertutup',
					'Gudang Terbuka',
					'Site Office',
					'Mushola',
					'Kamar Mandi & Toilet'
				]
				var kriteria = [
					'Bersih, rapi, wangi, nyaman, tidak ada sampah berserakan, dan instalasi listrik baik',
					'Bersih, rapi, dan semua barang tertata dengan baik',
					'Bersih, rapi, dan semua barang tertata dengan baik',
					'Bersih, rapi, wangi, nyaman, tidak ada sampah berserakan, dan instalasi listrik baik',
					'Bersih, rapi, nyaman, dan wangi',
					'Bersih, rapi, nyaman, dan wangi'
				]
				frm.clear_table("kebersihan_dan_kenyamanan");
				for(var i = 0; i < uraian.length; i++){
					var pr = frm.add_child("kebersihan_dan_kenyamanan");
					pr.uraian = uraian[i];
					pr.kriteria = kriteria[i];
				}
				
				frm.refresh_field("kebersihan_dan_kenyamanan");
			}
		}

		if (frm.doc.workflow_state == "Diketahui") {
			frm.add_custom_button(__('Buat Verifikasi'), function () {
				frappe.call({
					method: "erpnext.projects.doctype.daftar_periksa_saat_kunjungan_lapangan.daftar_periksa_saat_kunjungan_lapangan.create_verifikasi",
					args: {
						docname: frm.doc.name
					},
					callback: function(r) {
						if(r.message){
							frappe.show_alert({message:"Berhasil buat Verifikasi", indicator:'green'});
							window.location.href = "/app/daftar-periksa-saat-verifikasi-kunjungan-lapangan/"+r.message;
						}
					}
				});
			});
		}
	}
});