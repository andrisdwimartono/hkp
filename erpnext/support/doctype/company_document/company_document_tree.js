frappe.provide("frappe.treeview_settings")

frappe.treeview_settings["Company Document"] = {
	breadcrumb: "Support",
	title: __("Company Document"),
	fields: [
		{
			fieldtype: 'Data', fieldname: 'document_name', label: __('Document Name'), reqd: 1
		},
		{
			fieldtype: 'Check', fieldname: 'is_group', label: __('Folder?'),
			description: __("Jika di-check, maka akan berbentuk folder")
		},
		{
			fieldtype: 'Link', fieldname: 'uom', label: __('Satuan'), options: "UOM", reqd: 1
		},
		{
			fieldtype: 'Select', fieldname: 'pemilik_dokumen', label: __('Pemilik Dokumen'), options: "\nPerusahaan\nPersonal"
		},
		{
			fieldtype: 'Link', fieldname: 'jenis_dokumen', label: __('Jenis Dokumen'), options: "Jenis Dokumen"
		},
		{
			fieldtype: 'Data', fieldname: 'no_dokumen', label: __('No Dokumen')
		},
		{
			fieldtype: 'Data', fieldname: 'lembaga_terkait', label: __('Lembaga Terkait')
		},
		{
			fieldtype: 'Link', fieldname: 'project', label: __('Project'), options: "Project"
		},
		{
			fieldtype: 'Link', fieldname: 'employee', label: __('Employee'), options: "Employee"
		},
		{
			fieldtype: 'Link', fieldname: 'ordner', label: __('Ordner'), options: "Ordner"
		},
		{
			fieldtype: 'Date', fieldname: 'tanggal_terbit', label: __('Tanggal Terbit'), default: "Today", reqd: 1
		},
		{
			fieldtype: 'Date', fieldname: 'tanggal_expired', label: __('Tanggal Expired'), default: "Today", reqd: 1
		},
		{
			fieldtype: 'Attach', fieldname: 'document', label: __('Document')
		},
		{
			fieldtype: 'Small Text', fieldname: 'description', label: __('Description')
		},
	],
	ignore_fields:["parent_account"],
	toolbar: [
		{
			label: __("Download File"),
			click: function(node, btn) {
				console.log(node.data.value);
				frappe.db.get_value("Company Document", {"name": node.data.value}, "document", function(value) {
					window.location.href = value.document;
				});
			},
			btnClass: "hidden-xs"
		}
	],
	extend_toolbar: true
}
