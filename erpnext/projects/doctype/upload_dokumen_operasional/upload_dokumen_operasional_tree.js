frappe.provide("frappe.treeview_settings")

frappe.treeview_settings["Upload Dokumen Operasional"] = {
	breadcrumb: "Projects",
	title: __("Upload Dokumen Operasional"),
	fields: [
		{
			fieldtype: 'Check', fieldname: 'is_group', label: __('Apakah Folder?'),
			description: __("Jika di-check, maka akan berbentuk folder")
		},
		{
			fieldtype: 'Link', fieldname: 'project', label: __('Project'), options: 'Project', fetch_from: "parent_upload_dokumen_operasional.project", fetch_if_empty: 1
		},
		{
			fieldtype: 'Select', fieldname: 'ruang', label: __('Ruang'), options: "\nIzin Kerja\nRencana Kerja\nLaporan", fetch_from: "parent_upload_dokumen_operasional.ruang", fetch_if_empty: 1
		},
		{
			fieldtype: 'Select', fieldname: 'ruang_1', label: __('Izin Kerja'), options: "\nWorking Permit", fetch_from: "parent_upload_dokumen_operasional.ruang_1", fetch_if_empty: 1, depends_on: "eval: doc.ruang == 'Izin Kerja'", mandatory_depends_on: "eval: doc.ruang == 'Izin Kerja'"
		},
		{
			fieldtype: 'Select', fieldname: 'ruang_2', label: __('Rencana Kerja'), options: "\nIKP\nSOP\nMK", fetch_from: "parent_upload_dokumen_operasional.ruang_2", fetch_if_empty: 1, depends_on: "eval: doc.ruang == 'Rencana Kerja'", mandatory_depends_on: "eval: doc.ruang == 'Rencana Kerja'"
		},
		{
			fieldtype: 'Select', fieldname: 'ruang_3', label: __('Laporan'), options: "\nK3", fetch_from: "parent_upload_dokumen_operasional.ruang_3", fetch_if_empty: 1, depends_on: "eval: doc.ruang == 'Laporan'", mandatory_depends_on: "eval: doc.ruang == 'Laporan'"
		},
		{
			fieldtype: 'Data', fieldname: 'document_name', label: __('Document Name'), depends_on: "eval: doc.is_group != 1", mandatory_depends_on: "eval: doc.is_group != 1"
		},
		{
			fieldtype: 'Attach', fieldname: 'document', label: __('Document'), depends_on: "eval: doc.is_group != 1", mandatory_depends_on: "eval: doc.is_group != 1"
		}
	],
	ignore_fields:["parent_account"],
	toolbar: [
		{
			condition: function(node) {
				return !node.expandable
			},
			label: __("Download File"),
			click: function(node, btn) {
				console.log(node.data.value);
				frappe.db.get_value("Upload Dokumen Operasional", {"name": node.data.value}, "document", function(value) {
					window.location.href = value.document;
				});
			},
			btnClass: "hidden-xs"
		}
	],
	extend_toolbar: true
}
