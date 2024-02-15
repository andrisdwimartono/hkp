frappe.treeview_settings["Quality Procedure"] = {
	ignore_fields:["parent_quality_procedure"],
	fields: [
		{
			fieldtype: 'Check', fieldname: 'is_group', label: __('Apakah Folder?'),
			description: __("Jika di-check, maka akan berbentuk folder")
		},
		{
			fieldtype: 'Attach', fieldname: 'document', label: __('Document'), depends_on: "eval: doc.is_group != 1", mandatory_depends_on: "eval: doc.is_group != 1"
		}
	],
	get_tree_nodes: 'erpnext.quality_management.doctype.quality_procedure.quality_procedure.get_children',
	add_tree_node: 'erpnext.quality_management.doctype.quality_procedure.quality_procedure.add_node',
	filters: [
		{
			fieldname: "parent_quality_procedure",
			fieldtype: "Link",
			options: "Quality Procedure",
			label: __("Quality Procedure"),
			get_query: function() {
				return {
					filters: [["Quality Procedure", 'is_group', '=', 1]]
				};
			}
		},
	],
	breadcrumb: "Quality Management",
	disable_add_node: true,
	root_label: "All Quality Procedures",
	get_tree_root: false,
	menu_items: [
		{
			label: __("New Quality Procedure"),
			action: function() {
				frappe.new_doc("Quality Procedure", true);
			},
			condition: 'frappe.boot.user.can_create.indexOf("Quality Procedure") !== -1'
		}
	],
	onload: function(treeview) {
		treeview.make_tree();
	},
	toolbar: [
		{
			condition: function(node) {
				return !node.expandable
			},
			label: __("Download File"),
			click: function(node, btn) {
				frappe.db.get_value("Quality Procedure", {"name": node.data.value}, "document", function(value) {
					window.location.href = value.document;
				});
			},
			btnClass: "hidden-xs"
		}
	],
	extend_toolbar: true
};
