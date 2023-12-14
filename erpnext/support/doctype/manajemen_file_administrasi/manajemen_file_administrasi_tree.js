frappe.provide("frappe.treeview_settings")

frappe.treeview_settings["Manajemen File Administrasi"] = {
	breadcrumb: "Support",
	title: __("Manajemen File Administrasi"),
	fields: [
		{
			fieldtype: 'Check', fieldname: 'is_group', label: __('Folder?'),
			description: __("Jika di-check, maka akan berbentuk folder")
		},
		{
			fieldtype: 'Data', fieldname: 'document_name', label: __('Document Name'), reqd: 1
		},
		{
			fieldtype: 'Date', fieldname: 'tanggal', label: __('Tanggal'), default: "Today", reqd: 1
		},
		{
			fieldtype: 'Data', fieldname: 'perihal', label: __('Perihal')
		},
		{
			fieldtype: 'Link', fieldname: 'project', label: __('Project'), options: "Project"
		},
		{
			fieldtype: 'Link', fieldname: 'kelompok_file', label: __('Kelompok File'), options: "Kelompok File"
		},
		{
			fieldtype: 'Attach', fieldname: 'document', label: __('Document'), reqd: 1
		},
	],
	ignore_fields:["parent_account"],
	toolbar: [
		{
			label: __("Download File"),
			click: function(node, btn) {
				console.log(node.data.value);
				frappe.db.get_value("Manajemen File Administrasi", {"name": node.data.value}, "document", function(value) {
					window.location.href = value.document;
				});
			},
			btnClass: "hidden-xs"
		}
	],
	extend_toolbar: true
}
