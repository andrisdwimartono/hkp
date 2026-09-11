frappe.provide("frappe.treeview_settings")

frappe.treeview_settings["Project Documentation"] = {
	breadcrumb: "Projects",
	title: __("Project Documentation"),
	fields: [
		{
			fieldtype: 'Check', fieldname: 'is_group', label: __('Is Group'),
			description: __("If checked, it will be a folder")
		},
		{
			fieldtype: 'Link', fieldname: 'project', label: __('Project'), options: "Project",
			description: __("Required if folder"),
			mandatory_depends_on: "eval:doc.is_group == 1",
			depends_on: "eval:doc.is_group == 1",
			onchange: function() {
				let project = this.get_value();
				if (project && cur_dialog) {
					frappe.db.get_value('Project', project, 'project_name', function(r) {
						if (r && r.project_name) {
							cur_dialog.set_value('project_name', r.project_name);
						}
					});
				} else if (!project && cur_dialog) {
					cur_dialog.set_value('project_name', '');
				}
			}
		},
		{
			fieldtype: 'Data', fieldname: 'project_name', label: __('Project Name'),
			read_only: 1,
			fetch_from: 'project.project_name',
			depends_on: "eval:doc.is_group == 1"
		},
		{
			fieldtype: 'Date', fieldname: 'date', label: __('Date'), default: "Today", reqd: 1
		},
		{
			fieldtype: 'Attach Image', fieldname: 'file', label: __('File'),
			description: __("Required if not folder"),
			mandatory_depends_on: "eval:doc.is_group == 0",
			depends_on: "eval:doc.is_group == 0"
		},
		{
			fieldtype: 'Small Text', fieldname: 'description', label: __('Description')
		},
	],
	
	// ignore_fields:["parent_account"],
	toolbar: [
		{
			label: __("Download File"),
			click: function(node, btn) {
				frappe.db.get_value("Project Documentation", {"name": node.data.value}, "file", function(value) {
					window.location.href = value.file;
				});
			},
			condition: function(node) {
				return !node.expandable;
			}
		}
	],
	extend_toolbar: true
}
