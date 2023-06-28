// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Design and Drawing', {
	refresh: function(frm) {
		frm.add_custom_button(__('UMUM'), () => {
			window.location.href = "/printview?doctype=Project%20Design%20and%20Drawing&name="+cur_frm.doc.name+"&format=DRAWING%20LIST%20PRELIMINARY%20UMUM&no_letterhead=0&letterhead=KOP%20HKP&settings=%7B%7D&_lang=id";
		}, __('Cetak'));

		frm.add_custom_button(__('EM'), () => {
			window.location.href = "/printview?doctype=Project%20Design%20and%20Drawing&name="+cur_frm.doc.name+"&format=DRAWING%20LIST%20PRELIMINARY%20EM&no_letterhead=0&letterhead=KOP%20HKP&settings=%7B%7D&_lang=id";
		}, __('Cetak'));

		frm.add_custom_button(__('CIVIL'), () => {
			window.location.href = "/printview?doctype=Project%20Design%20and%20Drawing&name="+cur_frm.doc.name+"&format=DRAWING%20LIST%20PRELIMINARY%20CIVIL&no_letterhead=0&letterhead=KOP%20HKP&settings=%7B%7D&_lang=id";
		}, __('Cetak'));
	},
	// setup: function(frm){
	// 	frm.set_query("drawing", "tender_drawing", function(doc, cdt, cdn) {
	// 		let d = locals[cdt][cdn];
	// 		return {
	// 			filters: [
	// 				['Drawing', 'sub_section', '=', d.sub_section]
	// 			]
	// 		};
	// 	});

	// 	frm.set_query("drawing", "preliminary_design", function(doc, cdt, cdn) {
	// 		let d = locals[cdt][cdn];
	// 		return {
	// 			filters: [
	// 				['Drawing', 'sub_section', '=', d.sub_section]
	// 			]
	// 		};
	// 	});

	// 	frm.set_query("drawing", "detail_design_drawing", function(doc, cdt, cdn) {
	// 		let d = locals[cdt][cdn];
	// 		return {
	// 			filters: [
	// 				['Drawing', 'sub_section', '=', d.sub_section]
	// 			]
	// 		};
	// 	});

	// 	frm.set_query("drawing", "approval_drawing_sebagai_working_drawing", function(doc, cdt, cdn) {
	// 		let d = locals[cdt][cdn];
	// 		return {
	// 			filters: [
	// 				['Drawing', 'sub_section', '=', d.sub_section]
	// 			]
	// 		};
	// 	});

	// 	frm.set_query("drawing", "as_build_drawing", function(doc, cdt, cdn) {
	// 		let d = locals[cdt][cdn];
	// 		return {
	// 			filters: [
	// 				['Drawing', 'sub_section', '=', d.sub_section]
	// 			]
	// 		};
	// 	});

	// 	frm.set_query("drawing", "pengendalian_approval_drawing", function(doc, cdt, cdn) {
	// 		let d = locals[cdt][cdn];
	// 		return {
	// 			filters: [
	// 				['Drawing', 'sub_section', '=', d.sub_section]
	// 			]
	// 		};
	// 	});
	// }
});
