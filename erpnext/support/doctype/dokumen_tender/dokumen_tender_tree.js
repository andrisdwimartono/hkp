frappe.provide("frappe.treeview_settings")

frappe.treeview_settings["Dokumen Tender"] = {
	breadcrumb: "Support",
	title: __("Dokumen Tender"),
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
			fieldtype: 'Link', fieldname: 'informasi_pembukaan_tender', label: __('Informasi Pembukaan Tender'), options: "INFORMASI PEMBUKAAN TENDER", reqd: 1
		},
		{
			fieldtype: 'Data', fieldname: 'lingkup_pekerjaan', label: __('Lingkup Pekerjaan')
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
				frappe.db.get_value("Dokumen Tender", {"name": node.data.value}, "document", function(value) {
					window.location.href = value.document;
				});
			},
			btnClass: "hidden-xs"
		}
	],
	extend_toolbar: true
}
