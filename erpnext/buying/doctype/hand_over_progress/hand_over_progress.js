// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hand Over Progress', {
	// refresh: function(frm) {

	// }
	// setup: function(frm){
	// 	frm.set_query("sub_contract_hand_over", function() {
	// 		return {
	// 			filters: {
	// 				'docstatus': ["in", [0, 1]],
	// 			}
	// 		};
	// 	});
	// },
	sub_contract_hand_over: function(frm){
		frappe.call({
			method: 'erpnext.buying.doctype.hand_over_progress.hand_over_progress.check_progress',
			args: {
				'sub_contract_hand_over': frm.doc.sub_contract_hand_over
			},
			callback: function(r) {
				if(r.message){
					var vals = r.message[0];
					frm.set_value("progress_sequence", vals.progress_sequence);
					frm.refresh_field("progress_sequence");
					if(vals.progress_sequence != 1){
						frm.set_value("down_payment_percent", vals.down_payment_percent);
						frm.refresh_field("down_payment_percent");
						frm.set_value("down_payment", vals.down_payment);
						frm.refresh_field("down_payment");
					}else{

					}
				}
			}
		});

		cur_frm.clear_table("hand_over_progress_achieved");
		refresh_field("hand_over_progress_achieved");
		var c = frm.add_child("hand_over_progress_achieved");
		c.remarks = "Progres fisik sampai minggu ini";
		c.progress_amount = 0;
		refresh_field("hand_over_progress_achieved");
		var d = frm.add_child("hand_over_progress_achieved");
		d.remarks = "Retensi 5% X A";
		d.progress_amount = 0;
		refresh_field("hand_over_progress_achieved");

		frappe.call({
			method: 'erpnext.buying.doctype.hand_over_progress.hand_over_progress.get_last_discounts',
			args: {
				sub_contract_hand_over: frm.doc.sub_contract_hand_over
			},
			callback: function(r, rt) {
				console.log(r);
				if(r.message) {
					cur_frm.clear_table("hand_over_progress_discount");
					refresh_field("hand_over_progress_discount");
					var c = frm.add_child("hand_over_progress_discount");
					c.remarks = "Potongan Uang Muka ke-"+frm.doc.progress_sequence+" "+frm.doc.progress_achieved+"%";
					c.is_down_payment = 1;
					c.progress_bruto = frm.doc.down_payment;
					c.progress_discount = frm.doc.progress_achieved/100*frm.doc.down_payment;
					refresh_field("hand_over_progress_discount");

					$.each(r.message, function(i, d) {
						var vals = d;
						var c = frm.add_child("hand_over_progress_discount");
						c.remarks = vals.remarks;
						c.is_down_payment = 0;
						c.progress_bruto = vals.progress_discount;
						c.progress_discount = vals.progress_discount;
						refresh_field("hand_over_progress_discount");
					});

				}
			}
		});

		frm.doc.hand_over_progress_achieved[0].progress_amount=frm.doc.budget_amount*frm.doc.progress_achieved/100;
		refresh_field("hand_over_progress_achieved");
		frm.doc.hand_over_progress_achieved[1].progress_amount=frm.doc.hand_over_progress_achieved[0].progress_amount*0.05*(-1);
		refresh_field("hand_over_progress_achieved");
		
		var total_cost = 0;
		for(var i = 0; i < frm.doc.hand_over_progress_achieved.length; i++){
			total_cost = total_cost+frm.doc.hand_over_progress_achieved[i].progress_amount;
		}
		for(var i = 0; i < frm.doc.hand_over_progress_discount.length; i++){
			total_cost = total_cost-frm.doc.hand_over_progress_discount[i].progress_discount;
		}
		frm.set_value("total_cost", total_cost);
		refresh_field("total_cost");
	},
	progress_achieved: function(frm){
		frm.doc.hand_over_progress_achieved[0].progress_amount=frm.doc.budget_amount*frm.doc.progress_achieved/100;
		refresh_field("hand_over_progress_achieved");
		frm.doc.hand_over_progress_achieved[1].progress_amount=frm.doc.hand_over_progress_achieved[0].progress_amount*0.05*(-1);
		refresh_field("hand_over_progress_achieved");

		frm.set_value("down_payment", (frm.doc.down_payment_percent/100)*frm.doc.budget_amount);
		refresh_field("down_payment");
		
		frm.doc.hand_over_progress_discount[0].progress_discount=frm.doc.progress_achieved/100*frm.doc.down_payment;
		frm.doc.hand_over_progress_discount[0].remarks = "Potongan Uang Muka ke-"+frm.doc.progress_sequence+" "+frm.doc.progress_achieved+"%";
		refresh_field("hand_over_progress_discount");

		// var rounded_cost = 0;
		// for(var i = 0; i < frm.doc.hand_over_progress_achieved.length; i++){
		// 	rounded_cost=rounded_cost+frm.doc.hand_over_progress_achieved[i].progress_amount;
		// }
		// for(var i = 0; i < frm.doc.hand_over_progress_discount.length; i++){
		// 	rounded_cost=rounded_cost-frm.doc.hand_over_progress_discount[i].progress_discount;
		// }
		// frm.set_value("rounded_cost", rounded_cost);
		// refresh_field("rounded_cost");

		var total_cost = 0;
		var total_achieved = 0;
		for(var i = 0; i < frm.doc.hand_over_progress_achieved.length; i++){
			total_cost = total_cost+frm.doc.hand_over_progress_achieved[i].progress_amount;
			total_achieved = total_achieved+frm.doc.hand_over_progress_achieved[i].progress_amount;
		}
		frm.set_value("total_achieved", total_achieved);
		refresh_field("total_achieved");
		var total_discount = 0;
		for(var i = 0; i < frm.doc.hand_over_progress_discount.length; i++){
			total_cost = total_cost-frm.doc.hand_over_progress_discount[i].progress_discount;
			total_discount = total_discount-frm.doc.hand_over_progress_discount[i].progress_discount;
		}
		frm.set_value("total_discount", total_discount);
		refresh_field("total_discount");
		frm.set_value("total_cost", total_cost);
		refresh_field("total_cost");
	},
	use_ppn: function(frm){
		frm.set_value("ppn", frm.doc.total_cost*11/100);
		refresh_field("ppn");
	},
	ppn_percentage: function(frm){
		frm.set_value("ppn", frm.doc.total_cost*frm.doc.ppn_percentage/100);
		refresh_field("ppn");
	},
	pph_percentage: function(frm){
		frm.set_value("pph", frm.doc.total_cost*frm.doc.pph_percentage/100);
		refresh_field("pph");
	},
	down_payment_percent: function(frm){
		frm.set_value("down_payment", (frm.doc.down_payment_percent/100)*frm.doc.budget_amount);
		refresh_field("down_payment");

		frm.doc.hand_over_progress_discount[0].progress_discount=frm.doc.progress_achieved/100*frm.doc.down_payment;
		frm.doc.hand_over_progress_discount[0].remarks = "Potongan Uang Muka ke-"+frm.doc.progress_sequence+" "+frm.doc.progress_achieved+"%";
		refresh_field("hand_over_progress_discount");
		
		// var rounded_cost = 0;
		// for(var i = 0; i < frm.doc.hand_over_progress_achieved.length; i++){
		// 	rounded_cost=rounded_cost+frm.doc.hand_over_progress_achieved[i].progress_amount;
		// }
		// for(var i = 0; i < frm.doc.hand_over_progress_discount.length; i++){
		// 	rounded_cost=rounded_cost-frm.doc.hand_over_progress_discount[i].progress_discount;
		// }
		// frm.set_value("rounded_cost", rounded_cost);
		// refresh_field("rounded_cost");

		var total_cost = 0;
		var total_achieved = 0;
		for(var i = 0; i < frm.doc.hand_over_progress_achieved.length; i++){
			total_cost = total_cost+frm.doc.hand_over_progress_achieved[i].progress_amount;
			total_achieved = total_achieved+frm.doc.hand_over_progress_achieved[i].progress_amount;
		}
		frm.set_value("total_achieved", total_achieved);
		refresh_field("total_achieved");
		var total_discount = 0;
		for(var i = 0; i < frm.doc.hand_over_progress_discount.length; i++){
			total_cost = total_cost-frm.doc.hand_over_progress_discount[i].progress_discount;
			total_discount = total_discount-frm.doc.hand_over_progress_discount[i].progress_discount;
		}
		frm.set_value("total_discount", total_discount);
		refresh_field("total_discount");
		frm.set_value("total_cost", total_cost);
		refresh_field("total_cost");
	}
});

frappe.ui.form.on("Hand Over Progress Discount", "progress_bruto", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if(d.is_down_payment == 1){
		d.progress_discount = d.progress_bruto*frm.doc.progress_achieved/100;
	}else{
		d.progress_discount = d.progress_bruto;
	}
	refresh_field("hand_over_progress_discount");
});

frappe.ui.form.on("Hand Over Progress Discount", "progress_discount", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if(d.is_down_payment == 1){
		d.progress_bruto = d.progress_discount/frm.doc.progress_achieved*100;
	}else{
		d.progress_bruto = d.progress_discount;
	}
	refresh_field("hand_over_progress_discount");
});

frappe.ui.form.on("Hand Over Progress Discount", "is_down_payment", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if(d.is_down_payment == 1){
		d.progress_discount = d.progress_bruto*frm.doc.progress_achieved/100;
	}else{
		d.progress_discount = d.progress_bruto;
	}
	refresh_field("hand_over_progress_discount");
});
