// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Visitor Form', {
	refresh: function(frm) {
		$(`div[data-fieldname="safety_induction_list"]`).addClass("text-center").html(`
		<h3><b>SAFETY INDUCTION</b></h3><br>
		Gedung kantor ini memiliki 2 lantai dan Anda sekarang berada di lantai 1.<br><br>
		<ol>
			<li>Apabila terjadi keadaan darurat/emergency atau kebakaran, jangan panik dan ikuti jalur evakuasi yang telah ditentukan.</li>
			<li>Silahkan mengukuti petunjuk arah keluar untuk menuju Assembly Point yang ada di halaman kantor.</li>
			<li>Bagi karyawati atau tamu wanita yang memakai sepatu haq tinggi agar melepas sepatu saat terjadi keadaan darurat/emergency dan bergegas mengukuti petunjuk arah menuju Assembly Point.</li>
			<li>Untuk jalur evakuasi di lantai satu, silahkan lurus menuju lobby dan keluar ke arah pintu gerbang kemudian berkumpul di Assembly Point.</li>
			<li>Dalam masa pandemi Covid-19 diwajibkan mengikuti protokol kesehatan.</li>
		</ol>
		`);
	},
	a: function(frm){
		frappe.call({
			method:"erpnext.support.doctype.visitor_form.visitor_form.make_payment_request",
			args: {
				"dt": frm.doc.doctype,
				"dn": frm.doc.name,
				"party_type": "Student",
				"party": frm.doc.student,
				"recipient_id": frm.doc.student_email
			},
			callback: function(r) {
				if(!r.exc){
					var doc = frappe.model.sync(r.message);
					frappe.set_route("Form", doc[0].doctype, doc[0].name);
				}
			}
		});
	}
});
