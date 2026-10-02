// Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily K3', {
	refresh: function(frm) {
		setPicturesChecklist(frm);
	},

	man_power: function(frm){
		setTotalWorkingHours(frm);
	},

	working_hours: function(frm){
		setTotalWorkingHours(frm);
	}
});


function setPicturesChecklist(frm){
	$(`div[data-fieldname="body_harness_html"]`)
		.html("<img data-target='body_harness' class='w-100 mb-2 checkable-image' src='/files/1_body_harness.jpeg'>");
	$(`div[data-fieldname="pelindung_mata_html"]`)
		.html("<img data-target='pelindung_mata' class='w-100 mb-2 checkable-image' src='/files/2_pelindung_mata.jpeg'>");
	$(`div[data-fieldname="masker_html"]`)
		.html("<img data-target='masker' class='w-100 mb-2 checkable-image' src='/files/3_masker.jpeg'>");
	$(`div[data-fieldname="respirator_html"]`)
		.html("<img data-target='respirator' class='w-100 mb-2 checkable-image' src='/files/4_respirator.jpeg'>");
	$(`div[data-fieldname="kedok_las_html"]`)
		.html("<img data-target='kedok_las' class='w-100 mb-2 checkable-image' src='/files/5_kedok_las.jpeg'>");
	$(`div[data-fieldname="helm_safety_html"]`)
		.html("<img data-target='helm_safety' class='w-100 mb-2 checkable-image' src='/files/6_helm_safety.jpeg'>");
	$(`div[data-fieldname="earmuff_earplug_html"]`)
		.html("<img data-target='earmuff_earplug' class='w-100 mb-2 checkable-image' src='/files/7_earmuff_earplug.jpeg'>");
	$(`div[data-fieldname="sarung_tangan_html"]`)
		.html("<img data-target='sarung_tangan' class='w-100 mb-2 checkable-image' src='/files/8_sarung_tangan.jpeg'>");
	$(`div[data-fieldname="sepatu_safety_html"]`)
		.html("<img data-target='sepatu_safety' class='w-100 mb-2 checkable-image' src='/files/9_sepatu_safety.jpeg'>");
	$(`div[data-fieldname="sabuk_pengaman_html"]`)
		.html("<img data-target='sabuk_pengaman' class='w-100 mb-2 checkable-image' src='/files/10_sabuk_pengaman.jpeg'>");
	$(`div[data-fieldname="pelampung_html"]`)
		.html("<img data-target='pelampung' class='w-100 mb-2 checkable-image' src='/files/11_pelampung.jpeg'>");
	$(`div[data-fieldname="wearpack_html"]`)
		.html("<img data-target='wearpack' class='w-100 mb-2 checkable-image' src='/files/12_wearpack.jpeg'>");

	// on click, check/uncheck the checkbox
	$(document).on('click', '.checkable-image', function() {
		let target = $(this).data('target');
		if(frm.doc[target]){
			frm.set_value(target, 0);
		}else{
			frm.set_value(target, 1);
		}
		frm.refresh_field(target);
	});
}

function setTotalWorkingHours(frm){
	let total_working_hours = 0;
	
	let man_power = frm.doc.man_power;
	let working_hours = frm.doc.working_hours;
	
	total_working_hours = man_power * working_hours;
	frm.set_value("total_working_hours", total_working_hours);
	frm.refresh_field("total_working_hours");
}
