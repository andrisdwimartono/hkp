// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sub Contract Hand Over', {
	// refresh: function(frm) {

	// },
	setup: function(frm){
		frm.set_query("budget", function() {
			return {
				filters: {
					'project': frm.doc.project
				}
			};
		});

		frm.set_query("pos_rap", function() {
			return {
				query: "erpnext.accounts.doctype.budget_realization.budget_realization.get_pos_rap",
				filters: {
					'budget': frm.doc.budget
				}
			}
		});
	},
	pos_rap: function(frm){
		frappe.call({
			method: 'erpnext.accounts.doctype.form_payment_entry_project.form_payment_entry_project.check_budget',
			args: {
				'budget': frm.doc.budget,
				'pos_rap': frm.doc.pos_rap
			},
			callback: function(r) {
				if(r.message){
					var vals = r.message[0];
					frm.set_value("unit_price", vals.unit_price);
					frm.refresh_field("unit_price");
					frm.triger("unit_price");
					// if(frm.doc.ppn_type == "Tidak Termasuk PPn"){
					// 	frm.set_value("budget_value", vals.unit_price);
					// 	frm.refresh_field("budget_value");

					// 	// var budget_value = vals.unit_price;
					// 	// var ppn = vals.unit_price*frm.doc.ppn_percent/100;
					// 	// frm.set_value("budget_amount", budget_value+ppn);
					// 	// frm.refresh_field("budget_amount");
					// }else if(frm.doc.ppn_type == "Termasuk PPn"){
					// 	// frm.set_value("budget_amount", vals.unit_price);
					// 	// frm.refresh_field("budget_amount");

					// 	var budget_value = vals.unit_price;
					// 	var ppn = vals.unit_price*frm.doc.ppn_percent/100;
					// 	frm.set_value("budget_value", budget_value-ppn);
					// 	frm.refresh_field("budget_value");						
					// }else{
					// 	frm.set_value("budget_value", vals.unit_price);
					// 	frm.refresh_field("budget_value");

					// 	// frm.set_value("budget_amount", vals.unit_price);
					// 	// frm.refresh_field("budget_amount");
					// }
				}
			}
		});
	},

	unit_price: function(frm){
		if(frm.doc.ppn_type == "Tidak Termasuk PPn"){
			frm.set_value("budget_value", unit_price);
			frm.refresh_field("budget_value");
			var unit_price = frm.doc.unit_price;
			var ppn = frm.doc.unit_price*frm.doc.ppn_percent/100;
			frm.set_value("budget_amount", unit_price+ppn);
			frm.refresh_field("budget_amount");
		}else if(frm.doc.ppn_type == "Termasuk PPn"){
			var unit_price = frm.doc.unit_price;
			var ppn = frm.doc.unit_price*frm.doc.ppn_percent/100;
			frm.set_value("budget_value", unit_price-ppn);
			frm.refresh_field("budget_value");
			
			frm.set_value("budget_amount", unit_price);
			frm.refresh_field("budget_amount");
		}else{
			frm.set_value("budget_value", frm.doc.unit_price);
			frm.refresh_field("budget_value");

			frm.set_value("budget_amount", frm.doc.unit_price);
			frm.refresh_field("budget_amount");
		}
	},
	budget_value: function(frm){
		if(frm.doc.ppn_type == "Tidak Termasuk PPn"){
			var budget_value = frm.doc.budget_value;
			var ppn = frm.doc.budget_value*frm.doc.ppn_percent/100;
			frm.set_value("budget_amount", budget_value+ppn);
			frm.refresh_field("budget_amount");
		}else if(frm.doc.ppn_type == "Termasuk PPn"){
			var budget_value = frm.doc.budget_value;
			// var ppn = frm.doc.budget_value*frm.doc.ppn_percent/100;
			
			// frm.set_value("budget_amount", budget_value-ppn);
			frm.set_value("budget_amount", budget_value);
			frm.refresh_field("budget_amount");
		}else{

			frm.set_value("budget_amount", frm.doc.budget_value);
			frm.refresh_field("budget_amount");
		}
	},
	// budget_amount: function(frm){
	// 	if(frm.doc.ppn_type == "Termasuk PPn"){
	// 		var budget_value = frm.doc.budget_amount;
	// 		var ppn = frm.doc.budget_amount*frm.doc.ppn_percent/100;
	// 		frm.set_value("budget_value", budget_value-ppn);
	// 		frm.refresh_field("budget_value");						
	// 	}
	// 	// else{
	// 	// 	frm.set_value("budget_value", frm.doc.budget_amount);
	// 	// 	frm.refresh_field("budget_value");
	// 	// }
	// },
	ppn_type: function(frm){
		if(frm.doc.ppn_type == "Tidak Termasuk PPn"){
			var budget_value = frm.doc.budget_value;
			var ppn = frm.doc.budget_value*frm.doc.ppn_percent/100;
			frm.set_value("budget_amount", budget_value+ppn);
			frm.refresh_field("budget_amount");
		}else if(frm.doc.ppn_type == "Termasuk PPn"){
			var budget_value = frm.doc.budget_value;
			// var ppn = frm.doc.budget_value*frm.doc.ppn_percent/100;
			
			// frm.set_value("budget_amount", budget_value-ppn);
			frm.set_value("budget_amount", budget_value);
			frm.refresh_field("budget_amount");
		}else{

			frm.set_value("budget_amount", frm.doc.budget_value);
			frm.refresh_field("budget_amount");
		}
	},
});
