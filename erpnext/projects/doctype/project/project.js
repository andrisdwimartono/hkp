// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
frappe.ui.form.on("Project", {
	setup(frm) {
		frm.make_methods = {
			'Timesheet': () => {
				open_form(frm, "Timesheet", "Timesheet Detail", "time_logs");
			},
			'Purchase Order': () => {
				open_form(frm, "Purchase Order", "Purchase Order Item", "items");
			},
			'Purchase Receipt': () => {
				open_form(frm, "Purchase Receipt", "Purchase Receipt Item", "items");
			},
			'Purchase Invoice': () => {
				open_form(frm, "Purchase Invoice", "Purchase Invoice Item", "items");
			},
		};
	},
	onload: function (frm) {
		const so = frm.get_docfield("sales_order");
		so.get_route_options_for_new_doc = () => {
			if (frm.is_new()) return;
			return {
				"customer": frm.doc.customer,
				"project_name": frm.doc.name
			};
		};

		frm.set_query('customer', 'erpnext.controllers.queries.customer_query');

		frm.set_query("user", "users", function () {
			return {
				query: "erpnext.projects.doctype.project.project.get_users_for_project"
			};
		});

		// sales order
		frm.set_query('sales_order', function () {
			var filters = {
				'project': ["in", frm.doc.__islocal ? [""] : [frm.doc.name, ""]]
			};

			if (frm.doc.customer) {
				filters["customer"] = frm.doc.customer;
			}

			return {
				filters: filters
			};
		});
	},

	refresh: function (frm) {
		if (frm.doc.__islocal) {
			frm.web_link && frm.web_link.remove();
		} else {
			frm.add_web_link("/projects?project=" + encodeURIComponent(frm.doc.name));

			frm.trigger('show_dashboard');
		}
		frm.events.set_buttons(frm);

		if(frm.doc.expected_start_date){
			var endDate = new Date();
			var startDate = new Date(frm.doc.expected_start_date);

			var millisecondsPerDay = 24 * 60 * 60 * 1000;
			$(`div[data-fieldname="day_count_up"]`).html("<h4 class='text-center'>"+(((endDate - startDate) / millisecondsPerDay) < 0? "Belum Dimulai": "Hari Ke-"+Math.ceil((endDate - startDate) / millisecondsPerDay))+"</h4>");
		}else{
			$(`div[data-fieldname="day_count_up"]`).html("");
		}

		if(frm.doc.expected_end_date){
			var startDate = new Date();
			var endDate = new Date(frm.doc.expected_end_date);

			var millisecondsPerDay = 24 * 60 * 60 * 1000;
			$(`div[data-fieldname="day_count_down"]`).html("<h4 class='text-center'>"+(((endDate - startDate) / millisecondsPerDay) < 0? "Sudah Melewati "+Math.floor((endDate - startDate) / millisecondsPerDay*(-1))+" Hari": "Kurang "+Math.ceil((endDate - startDate) / millisecondsPerDay)+" Hari")+"</h4>");
		}else{
			$(`div[data-fieldname="day_count_down"]`).html("");
		}
	},

	expected_start_date: function(frm){
		if(frm.doc.expected_start_date){
			var endDate = new Date();
			var startDate = new Date(frm.doc.expected_start_date);

			var millisecondsPerDay = 24 * 60 * 60 * 1000;
			$(`div[data-fieldname="day_count_up"]`).html("<h4 class='text-center'>"+(((endDate - startDate) / millisecondsPerDay) < 0? "Belum Dimulai": "Hari Ke-"+Math.ceil((endDate - startDate) / millisecondsPerDay))+"</h4>");
		}else{
			$(`div[data-fieldname="day_count_up"]`).html("");
		}
	},

	expected_end_date: function(frm){
		if(frm.doc.expected_end_date){
			var startDate = new Date();
			var endDate = new Date(frm.doc.expected_end_date);

			var millisecondsPerDay = 24 * 60 * 60 * 1000;
			$(`div[data-fieldname="day_count_down"]`).html("<h4 class='text-center'>"+(((endDate - startDate) / millisecondsPerDay) < 0? "Sudah Melewati "+Math.floor((endDate - startDate) / millisecondsPerDay*(-1))+" Hari": "Kurang "+Math.ceil((endDate - startDate) / millisecondsPerDay)+" Hari")+"</h4>");
		}else{
			$(`div[data-fieldname="day_count_down"]`).html("");
		}
	},

	set_buttons: function(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Duplicate Project with Tasks'), () => {
				frm.events.create_duplicate(frm);
			});

			frm.add_custom_button(__('Completed'), () => {
				frm.events.set_status(frm, 'Completed');
			}, __('Set Status'));

			frm.add_custom_button(__('Cancelled'), () => {
				frm.events.set_status(frm, 'Cancelled');
			}, __('Set Status'));


			if (frappe.model.can_read("Task")) {
				frm.add_custom_button(__("Gantt Chart"), function () {
					frappe.route_options = {
						"project": frm.doc.name
					};
					frappe.set_route("List", "Task", "Gantt");
				});

				frm.add_custom_button(__("Kanban Board"), () => {
					frappe.call('erpnext.projects.doctype.project.project.create_kanban_board_if_not_exists', {
						project: frm.doc.name
					}).then(() => {
						frappe.set_route('List', 'Task', 'Kanban', frm.doc.project_name);
					});
				});
			}
		}


	},

	create_duplicate: function(frm) {
		return new Promise(resolve => {
			frappe.prompt('Project Name', (data) => {
				frappe.xcall('erpnext.projects.doctype.project.project.create_duplicate_project',
					{
						prev_doc: frm.doc,
						project_name: data.value
					}).then(() => {
					frappe.set_route('Form', "Project", data.value);
					frappe.show_alert(__("Duplicate project has been created"));
				});
				resolve();
			});
		});
	},

	set_status: function(frm, status) {
		frappe.confirm(__('Set Project and all Tasks to status {0}?', [status.bold()]), () => {
			frappe.xcall('erpnext.projects.doctype.project.project.set_project_status',
				{project: frm.doc.name, status: status}).then(() => { /* page will auto reload */ });
		});
	},

});

function open_form(frm, doctype, child_doctype, parentfield) {
	frappe.model.with_doctype(doctype, () => {
		let new_doc = frappe.model.get_new_doc(doctype);

		// add a new row and set the project
		let new_child_doc = frappe.model.get_new_doc(child_doctype);
		new_child_doc.project = frm.doc.name;
		new_child_doc.parent = new_doc.name;
		new_child_doc.parentfield = parentfield;
		new_child_doc.parenttype = doctype;
		new_doc[parentfield] = [new_child_doc];
		new_doc.project = frm.doc.name;

		frappe.ui.form.make_quick_entry(doctype, null, null, new_doc);
	});

}
