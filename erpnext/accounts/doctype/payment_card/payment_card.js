// Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Card', {
	// refresh: function(frm) {

	// },
	setup: function(frm) {
		frm.set_query("document", function() {
			if(frm.doc.vendor_type === "Sub Contract" && frm.doc.vendor) {
				return {
					filters: {
						sub_contract: frm.doc.vendor
					}
				};
			}else if(frm.doc.vendor_type === "Supplier" && frm.doc.vendor) {
				return {
					filters: {
						supplier: frm.doc.vendor
					}
				}
			}
		});
	},
	type: function(frm) {
		frm.set_value("vendor", "");
		frm.set_value("document", "");
		if(frm.doc.type === "Sub Contract Hand Over") {
			// set vendor type to sub contractor
			frm.set_value("vendor_type", "Sub Contract");
		}else{
			// set vendor type to supplier
			frm.set_value("vendor_type", "Supplier");
		}
	},
	vendor: function(frm) {
		if(frm.doc.vendor){
			if(frm.doc.vendor_type === "Sub Contract") {
				// get value of document using frappe get_doc
				frappe.db.get_value("Sub Contract", frm.doc.vendor, ["contractor_name"]).then((r) => {
					let detail = r.message;
					frm.set_value("vendor_name", detail.contractor_name);
				});
			}else{
				frm.set_value("vendor_name", frm.doc.vendor);
			}
		}
	},
	document: function(frm) {
		if(frm.doc.document){
			if(frm.doc.type === "Sub Contract Hand Over") {
				// get value of document using frappe get_doc
				frappe.db.get_value("Sub Contract Hand Over", frm.doc.document, ["sub_contract", "project", "job_name", "berdasarkan", "lokasi_pekerjaan", "start_work", "finish_work", "budget_amount"]).then((r) => {
					let detail = r.message;
					frm.set_value("vendor", detail.sub_contract);
					frm.set_value("project", detail.project);
					frm.set_value("job_name", detail.job_name);
					frm.set_value("address", detail.lokasi_pekerjaan);
					frm.set_value("description", detail.berdasarkan);
					frm.set_value("contract_date", detail.start_work);
					frm.set_value("contract_due_date", detail.finish_work);
					frm.set_value("contract_value", detail.budget_amount);
				});
			}else{
				frappe.db.get_value("Purchase Order", frm.doc.document, ["supplier", "project", "terms", "shipping_address_display", "transaction_date", "grand_total"]).then((r) => {
					let detail = r.message;
					frm.set_value("vendor", detail.supplier);
					frm.set_value("project", detail.project);
					frm.set_value("job_name", "Pesanan Barang");
					frm.set_value("address", detail.shipping_address_display);
					// frm.set_value("description", detail.terms);
					frm.set_value("description", "");
					frm.set_value("contract_date", detail.transaction_date);
					frm.set_value("contract_due_date", detail.transaction_date);
					frm.set_value("contract_value", detail.grand_total);
				});
			}
			
		}
	},
	contract_value: function(frm) {
		if(!frm.doc.detail){
			var c = frm.add_child("detail");
			c.payment = 0;
			c.total_payment = 0;
			c.saldo = frm.doc.contract_value;
			refresh_field("detail");
		}else{
			// replace saldo in array 0
			frm.doc.detail[0].saldo = frm.doc.contract_value;
			refresh_field("detail");
		}
	}
});