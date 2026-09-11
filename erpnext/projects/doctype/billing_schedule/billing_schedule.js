// Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Billing Schedule', {
	refresh: function(frm) {
		setMaxTermin(frm)

		frm.events.billing_date(frm);

		// if create, fill frm.doc.documents table with this
		if(cur_frm.doc.__unsaved){
			let documents_list = ["Kwitansi & Faktur Pajak", "Surat Permohonan Pembayaran", "NPWP", "Bank Account Pembayaran", "Bank Account Kemajuan Pekerjaan", "BA Penyelesaian Pekerjaan", "BAPM"]

			for(let document_name of documents_list){
				let new_row = frm.add_child("documents");
				new_row.document_name = document_name;
				new_row.avaibility = 'Not Available';
			}
			frm.refresh_field("documents");
		}
	},
	expected_end_date: function(frm){
		setDayCountDown(frm)
	},

	bond_validity_period: function(frm){
		setDayCountDownBond(frm)
	},

	project: function(frm){
		setMaxTermin(frm)
	},

	billing_date: function(frm){
		setDayCountDown(frm)

		setDayCountDownBond(frm)

		setSbuDocumentExpiredAndDayCountDownSbu(frm)
	}
});

function setDayCountDown(frm){
	if(frm.doc.expected_end_date){
		let billing_date = new Date();
		if(frm.doc.billing_date){
			billing_date = new Date(frm.doc.billing_date);
		}
		var startDate = billing_date;
		var endDate = new Date(frm.doc.expected_end_date);

		var millisecondsPerDay = 24 * 60 * 60 * 1000;
		$(`div[data-fieldname="day_count_down"]`).html("<h4 class='text-center'>"+(((endDate - startDate) / millisecondsPerDay) < 0? "Sudah Melewati "+Math.floor((endDate - startDate) / millisecondsPerDay*(-1))+" Hari ❌": "Kurang "+Math.ceil((endDate - startDate) / millisecondsPerDay)+" Hari ✅")+"</h4>");
	}else{
		$(`div[data-fieldname="day_count_down"]`).html("");
	}
}

function setDayCountDownBond(frm){
	if(frm.doc.bond_validity_period){
		let billing_date = new Date();
		if(frm.doc.billing_date){
			billing_date = new Date(frm.doc.billing_date);
		}
		var startDate = billing_date;
		var endDate = new Date(frm.doc.bond_validity_period);

		var millisecondsPerDay = 24 * 60 * 60 * 1000;
		$(`div[data-fieldname="day_count_down_bond"]`).html("<h4 class='text-center'>"+(((endDate - startDate) / millisecondsPerDay) < 0? "Sudah Melewati "+Math.floor((endDate - startDate) / millisecondsPerDay*(-1))+" Hari ❌": "Kurang "+Math.ceil((endDate - startDate) / millisecondsPerDay)+" Hari ✅")+"</h4 >");
	}else{
		$(`div[data-fieldname="day_count_down_bond"]`).html("");
	}
}

// get max termin for this project
function setMaxTermin(frm){
	if((!frm.doc.termin || frm.doc.termin == 0) && frm.doc.project){
		frappe.call({
			method: "erpnext.projects.doctype.billing_schedule.billing_schedule.get_max_termin_by_project",
			args: {
				project: frm.doc.project
			},
			callback: function(r) {
				frm.set_value("termin", (Number(r.message[0].termin) || 0) + 1);
				frm.refresh_field("termin");
			}
		});
	}
}
	
function setSbuDocumentExpiredAndDayCountDownSbu(frm){
	frappe.call({
		method: "erpnext.projects.doctype.billing_schedule.billing_schedule.get_sbu_expired_date",
		callback: function(r) {
			if((!frm.doc.sbu_validity_period || frm.doc.sbu_validity_period == 0) && r.message[0].expired_date){
				frm.set_value("sbu_validity_period", r.message[0].expired_date);
				frm.refresh_field("sbu_validity_period");
			}

			let billing_date = new Date();
			if(frm.doc.billing_date){
				billing_date = new Date(frm.doc.billing_date);
			}

			let startDate = billing_date;
			let sbuDocumentExpiredDate = new Date(r.message[0].expired_date);

			let millisecondsPerDay = 24 * 60 * 60 * 1000;
			$(`div[data-fieldname="day_count_down_sbu"]`).html("<h4 class='text-center'>"+(((sbuDocumentExpiredDate - startDate) / millisecondsPerDay) < 0? "Sudah Melewati "+Math.floor((sbuDocumentExpiredDate - startDate) / millisecondsPerDay*(-1))+" Hari ❌": "Kurang "+Math.ceil((sbuDocumentExpiredDate - startDate) / millisecondsPerDay)+" Hari ✅")+"</h4 >");
		}
	});
}

