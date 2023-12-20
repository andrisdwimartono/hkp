// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tarik Data Absensi', {
	refresh: function(frm) {

	},
	get_data: function(frm){
		// $.ajax({
		// 	method: "GET",
		// 	url: "http://localhost:8003/index3.php",
		// 	dataType: "json",
		// 	success: function(data) {
		// 		console.log("token");
		// 		console.log(data);
		// 	}
		// });


		// $.ajax({
		// 	method: "POST",
		// 	url: "http://192.168.18.250:8091/jwt-api-token-auth/",
		// 	dataType: "json",
		// 	data: {
		// 		username: "hasta.subag",
		// 		password: "hast@hkp123321"
		// 	},
		// 	success: function(data) {
		// 		console.log("token");
		// 		console.log(data);
		// 		//get department
		// 		$.ajax({
		// 			method: "GET",
		// 			url: "http://192.168.18.250:8091/personnel/api/departments/?page_size=20",
		// 			beforeSend: function (xhr) {
		// 				xhr.setRequestHeader("Authorization", "JWT " + data);
		// 			},
		// 			dataType: "json",
		// 			success: function(data) {
		// 				console.log("data");
		// 				console.log(data);
		// 				for(var i = 0; i < data.length; i++){
		// 					var start_date = cur_frm.doc.start_date;
		// 					var end_date = cur_frm.doc.end_date;
		// 					var dept_id = data[i].id;
		// 					console.log("get_data");
		// 					$.ajax({
		// 						method: "GET",
		// 						url: "http://192.168.18.250:8091/att/api/transactionReport/?start_date="+start_date+"&end_date="+end_date+"&departments="+dept_id,
		// 						beforeSend: function (xhr) {
		// 							xhr.setRequestHeader("Authorization", "JWT " + data);
		// 						},
		// 						dataType: "json",
		// 						success: function(data) {
		// 							for(var i = 0; i < data.length; i++){
		// 								console.log(data[i]);
		// 							}
		// 						}
		// 					});
		// 				}
		// 			}
		// 		});
		// 	}
		// });
	}
});
