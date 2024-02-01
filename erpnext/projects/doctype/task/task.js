// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.projects");

frappe.ui.form.on("Task", {
	setup: function (frm) {
		frm.make_methods = {
			'Timesheet': () => frappe.model.open_mapped_doc({
				method: 'erpnext.projects.doctype.task.task.make_timesheet',
				frm: frm
			})
		}
	},

	onload: function (frm) {
		frm.set_query("task", "depends_on", function () {
			let filters = {
				name: ["!=", frm.doc.name]
			};
			if (frm.doc.project) filters["project"] = frm.doc.project;
			return {
				filters: filters
			};
		})

		frm.set_query("parent_task", function () {
			let filters = {
				"is_group": 1,
				"name": ["!=", frm.doc.name]
			};
			if (frm.doc.project) filters["project"] = frm.doc.project;
			return {
				filters: filters
			}
		});
	},

	is_group: function (frm) {
		frappe.call({
			method: "erpnext.projects.doctype.task.task.check_if_child_exists",
			args: {
				name: frm.doc.name
			},
			callback: function (r) {
				if (r.message.length > 0) {
					let message = __('Cannot convert Task to non-group because the following child Tasks exist: {0}.',
						[r.message.join(", ")]
					);
					frappe.msgprint(message);
					frm.reload_doc();
				}
			}
		})
	},

	validate: function (frm) {
		frm.doc.project && frappe.model.remove_from_locals("Project",
			frm.doc.project);
	}
});


frappe.ui.form.on("Task Progress", {
	task_progress_add: function(frm, dt, dn){
		var d = locals[dt][dn];
		for(var i = cur_frm.doc.task_progress.length-1; i >= 0; i--){
			if(cur_frm.doc.task_progress[i].idx == d.idx-1){
				d.task_weight = cur_frm.doc.task_progress[i].task_weight;
				break;
			}
		}
		frm.refresh_field("task_progress");
	},
	rencana_mingguan: function (frm, dt, dn) {
		var d = locals[dt][dn];
		var sebelumnya = 0;
		for(var i = cur_frm.doc.task_progress.length-1; i >= 0; i--){
			if(cur_frm.doc.task_progress[i].idx == d.idx-1){
				sebelumnya = cur_frm.doc.task_progress[i].rencana;
				break;
			}
		}
		d.rencana = sebelumnya+d.rencana_mingguan;
		frm.refresh_field("task_progress");
	},
	rencana: function (frm, dt, dn) {
		var d = locals[dt][dn];
		d.deviasi = d.rencana-d.realisasi;
		frm.refresh_field("task_progress");

		var progress = 0;
		for(var i = cur_frm.doc.task_progress.length-1; i >= 0; i--){
			if(cur_frm.doc.task_progress[i].realisasi > 0){
				progress = cur_frm.doc.task_progress[i].realisasi;
				break;
			}
		}
		frm.set_value("progress", progress);
		frm.refresh_field("progress");
	},
	realisasi_mingguan: function (frm, dt, dn) {
		var d = locals[dt][dn];
		var sebelumnya = 0;
		for(var i = cur_frm.doc.task_progress.length-1; i >= 0; i--){
			if(cur_frm.doc.task_progress[i].idx == d.idx-1){
				sebelumnya = cur_frm.doc.task_progress[i].realisasi;
				break;
			}
		}
		d.realisasi = sebelumnya+d.realisasi_mingguan;
		frm.refresh_field("task_progress");
	},
	realisasi: function (frm, dt, dn) {
		var d = locals[dt][dn];
		d.deviasi = d.rencana-d.realisasi;
		frm.refresh_field("task_progress");
		
		var progress = 0;
		for(var i = cur_frm.doc.task_progress.length-1; i >= 0; i--){
			if(cur_frm.doc.task_progress[i].realisasi > 0){
				progress = cur_frm.doc.task_progress[i].realisasi;
				break;
			}
		}
		frm.set_value("progress", progress);
		frm.refresh_field("progress");
	},
});
