// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('INFORMASI PEMBUKAAN TENDER', {
	refresh: function(frm) {
		if (frm.doc.__unsaved == 1)	{
			if(!frm.doc.hasil_pembukaan_tender){
				frm.clear_table("hasil_pembukaan_tender");
				frappe.call({
					method: 'erpnext.crm.utils.get_hasil_pembukaan_tender',
					args: {
						'doctype': frm.doc.doctype
					},
					callback: function(r) {
						if(r.message){
							var vals = r.message;
							for(var i = 0; i < vals.length; i++){
								var pr = frm.add_child("hasil_pembukaan_tender");
								// pr.jabatan = vals[i].jabatan;
								// pr.jabatan_abbr = vals[i].jabatan_abbr;
								// pr.state = vals[i].state;
								// pr.employee = vals[i].employee;
								// pr.employee_name = vals[i].employee_name;
								// pr.user = vals[i].user;
							}
							frm.refresh_field("hasil_pembukaan_tender");
						}
					}
				});
			}
		} else {
			
		}
	}
});
