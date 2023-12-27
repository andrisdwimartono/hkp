// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tarik Data Absensi', {
	refresh: function(frm) {

	},
	start_date: function(frm){
		if(frm.doc.start_date && frm.doc.end_date){
			frm.clear_table("detail_data_absensi");
			$.ajax({
				method: "GET",
				url: "http://192.168.18.250:8099?start_date="+cur_frm.doc.start_date+"&end_date="+cur_frm.doc.end_date,
				dataType: "json",
				success: function(data) {
					for(var i = 0; i < data.length; i++){
						console.log(data[i].emp_code)
						var pr = frm.add_child("detail_data_absensi");
						// pr.employee = data[i].employee;
						pr.employee_name = data[i].first_name;
						pr.emp_code = data[i].emp_code;
						pr.id = data[i].id;
						pr.att_date = data[i].att_date;
						pr.punch_time = data[i].punch_time;
						pr.punch_state = data[i].punch_state;
						pr.verify_type = data[i].verify_type;
						pr.source = data[i].source;
					}
					frm.refresh_field("detail_data_absensi");
				}
			});
		}
	},
	end_date: function(frm){
		if(frm.doc.start_date && frm.doc.end_date){
			frm.clear_table("detail_data_absensi");
			$.ajax({
				method: "GET",
				url: "http://192.168.18.250:8099?start_date="+cur_frm.doc.start_date+"&end_date="+cur_frm.doc.end_date,
				dataType: "json",
				success: function(data) {
					for(var i = 0; i < data.length; i++){
						console.log(data[i].emp_code)
						var pr = frm.add_child("detail_data_absensi");
						// pr.employee = data[i].employee;
						pr.employee_name = data[i].first_name;
						pr.emp_code = data[i].emp_code;
						pr.id = data[i].id;
						pr.att_date = data[i].att_date;
						pr.punch_time = data[i].punch_time;
						pr.punch_state = data[i].punch_state;
						pr.verify_type = data[i].verify_type;
						pr.source = data[i].source;
					}
					frm.refresh_field("detail_data_absensi");
				}
			});
		}
	},
	get_data: function(frm){
		


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
