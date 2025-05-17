frappe.listview_settings['Journal Entry'] = {
	colwidths: {
	  name: 1, // make it very narrow
	  user_remark: 3, // wider for your custom field
	  voucher_type: 2,
	  posting_date: 2,
	  total_debit: 2
	},
	add_fields: ["voucher_type", "posting_date", "total_debit", "user_remark"],
  
	onload: function(listview) {
	  listview.page.sidebar.hide(); // hide filter sidebar

	  // Modify column widths by adding custom CSS
	  $('<style>\
		.list-row-col[data-fieldname="name"] { max-width: 80px !important; width: 80px !important; }\
		.list-row-col[data-fieldname="user_remark"] { min-width: 300px !important; width: 300px !important; }\
		.list-row-col[data-fieldname="voucher_type"] { width: 150px !important; }\
		.list-row-col[data-fieldname="posting_date"] { width: 150px !important; }\
		.list-row-col[data-fieldname="total_debit"] { width: 150px !important; }\
	  </style>').appendTo('head');
	},
  
	get_indicator: function(doc) {
	  if (doc.docstatus === 0) {
		return [__("Draft"), "red", "docstatus,=,0"];
	  } else if (doc.docstatus === 2) {
		return [__("Cancelled"), "grey", "docstatus,=,2"];
	  } else {
		return [__(doc.voucher_type), "blue", "voucher_type,=," + doc.voucher_type];
	  }
	}
  };

// frappe.listview_settings['Journal Entry'] = {
// 	onload: function(listview) {
// 		if (frappe.get_route().join('/') === 'List/Journal Entry/List') {
// 		frappe.set_route('journal-entry/view/report');
// 		}
// 	},
// };