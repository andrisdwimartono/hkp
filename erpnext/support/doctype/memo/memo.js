// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Memo', {
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			if(!frm.doc.process_rules){
				frm.clear_table("process_rules");
				frappe.call({
					method: 'erpnext.projects.utils.get_process_rules',
					args: {
						'doctype': frm.doc.doctype
					},
					callback: function(r) {
						if(r.message){
							var vals = r.message;
							for(var i = 0; i < vals.length; i++){
								var pr = frm.add_child("process_rules");
								pr.jabatan = vals[i].jabatan;
								pr.jabatan_abbr = vals[i].jabatan_abbr;
								pr.state = vals[i].state;
								pr.employee = vals[i].employee;
								pr.initial = vals[i].initial;
								pr.employee_name = vals[i].employee_name;
								pr.user = vals[i].user;
							}
							frm.refresh_field("process_rules");
						}
					}
				});
			}
		}else{
			
		}
		cur_frm.fields_dict['process_rules'].$wrapper.find('.grid-add-row').addClass('d-none');
	}
});


frappe.ui.form.on('Memo Kepada', {
	pihak: function(frm, dt, dn){
		var d = locals[dt][dn];
		if(d.type == "Employee"){
			frappe.call({
				method: 'erpnext.hr.doctype.employee.employee.get_employee_info',
				args: {
					'name': d.pihak
				},
				callback: function(r) {
					if(r.message){
						var vals = r.message;
						d.employee_name = vals[0].employee_name;
						d.user_id = vals[0].user_id;
						frm.refresh_field("kepada");
						frm.refresh_field("tembusan");
					}
				}
			});
		}
	},
	type: function(frm, dt, dn){
		var d = locals[dt][dn];
		if(d.type != "Employee"){
			d.pihak = "";
			d.employee_name = "";
			d.user_id = "";
			frm.refresh_field("kepada");
			frm.refresh_field("tembusan");
		}
	}
});