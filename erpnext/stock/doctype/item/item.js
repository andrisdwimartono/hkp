// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.item");

frappe.ui.form.on("Item", {
	setup: function(frm) {
		frm.add_fetch('attribute', 'numeric_values', 'numeric_values');
		frm.add_fetch('attribute', 'from_range', 'from_range');
		frm.add_fetch('attribute', 'to_range', 'to_range');
		frm.add_fetch('attribute', 'increment', 'increment');
		frm.add_fetch('tax_type', 'tax_rate', 'tax_rate');

		frm.make_methods = {
			'Sales Order': () => {
				open_form(frm, "Sales Order", "Sales Order Item", "items");
			},
			'Delivery Note': () => {
				open_form(frm, "Delivery Note", "Delivery Note Item", "items");
			},
			'Sales Invoice': () => {
				open_form(frm, "Sales Invoice", "Sales Invoice Item", "items");
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
			'Material Request': () => {
				open_form(frm, "Material Request", "Material Request Item", "items");
			},
		};

	},
	onload: function(frm) {
		erpnext.item.setup_queries(frm);
		if (frm.doc.variant_of){
			frm.fields_dict["attributes"].grid.set_column_disp("attribute_value", true);
		}

		if (frm.doc.is_fixed_asset) {
			frm.trigger("set_asset_naming_series");
		}
	},

	refresh: function(frm) {
		if (frm.doc.is_stock_item) {
			frm.add_custom_button(__("Stock Balance"), function() {
				frappe.route_options = {
					"item_code": frm.doc.name
				}
				frappe.set_route("query-report", "Stock Balance");
			}, __("View"));
			frm.add_custom_button(__("Stock Ledger"), function() {
				frappe.route_options = {
					"item_code": frm.doc.name
				}
				frappe.set_route("query-report", "Stock Ledger");
			}, __("View"));
			frm.add_custom_button(__("Stock Projected Qty"), function() {
				frappe.route_options = {
					"item_code": frm.doc.name
				}
				frappe.set_route("query-report", "Stock Projected Qty");
			}, __("View"));
		}


		if (frm.doc.is_fixed_asset) {
			frm.trigger('is_fixed_asset');
			frm.trigger('auto_create_assets');
		}

		// clear intro
		frm.set_intro();

		if (frm.doc.has_variants) {
			frm.set_intro(__("This Item is a Template and cannot be used in transactions. Item attributes will be copied over into the variants unless 'No Copy' is set"), true);

			frm.add_custom_button(__("Show Variants"), function() {
				frappe.set_route("List", "Item", {"variant_of": frm.doc.name});
			}, __("View"));

			frm.add_custom_button(__("Item Variant Settings"), function() {
				frappe.set_route("Form", "Item Variant Settings");
			}, __("View"));

			frm.add_custom_button(__("Variant Details Report"), function() {
				frappe.set_route("query-report", "Item Variant Details", {"item": frm.doc.name});
			}, __("View"));

			if(frm.doc.variant_based_on==="Item Attribute") {
				frm.add_custom_button(__("Single Variant"), function() {
					erpnext.item.show_single_variant_dialog(frm);
				}, __('Create'));
				frm.add_custom_button(__("Multiple Variants"), function() {
					erpnext.item.show_multiple_variants_dialog(frm);
				}, __('Create'));
			} else {
				frm.add_custom_button(__("Variant"), function() {
					erpnext.item.show_modal_for_manufacturers(frm);
				}, __('Create'));
			}

			// frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
		if (frm.doc.variant_of) {
			frm.set_intro(__('This Item is a Variant of {0} (Template).',
				[`<a href="/app/item/${frm.doc.variant_of}" onclick="location.reload()">${frm.doc.variant_of}</a>`]), true);
		}

		if (frappe.defaults.get_default("item_naming_by")!="Naming Series" || frm.doc.variant_of) {
			frm.toggle_display("naming_series", false);
		} else {
			erpnext.toggle_naming_series();
		}

		if (!frm.doc.published_in_website) {
			frm.add_custom_button(__("Publish in Website"), function() {
				frappe.call({
					method: "erpnext.e_commerce.doctype.website_item.website_item.make_website_item",
					args: {doc: frm.doc},
					freeze: true,
					freeze_message: __("Publishing Item ..."),
					callback: function(result) {
						frappe.msgprint({
							message: __("Website Item {0} has been created.",
								[repl('<a href="/app/website-item/%(item_encoded)s" class="strong">%(item)s</a>', {
									item_encoded: encodeURIComponent(result.message[0]),
									item: result.message[1]
								})]
							),
							title: __("Published"),
							indicator: "green"
						});
					}
				});
			}, __('Actions'));
		} else {
			frm.add_custom_button(__("Website Item"), function() {
				frappe.db.get_value("Website Item", {item_code: frm.doc.name}, "name", (d) => {
					if (!d.name) frappe.throw(__("Website Item not found"));
					frappe.set_route("Form", "Website Item", d.name);
				});
			}, __("View"));
		}

		erpnext.item.edit_prices_button(frm);
		erpnext.item.toggle_attributes(frm);

		if (!frm.doc.is_fixed_asset) {
			erpnext.item.make_dashboard(frm);
		}

		frm.add_custom_button(__('Duplicate'), function() {
			var new_item = frappe.model.copy_doc(frm.doc);
			// Duplicate item could have different name, causing "copy paste" error.
			if (new_item.item_name===new_item.item_code) {
				new_item.item_name = null;
			}
			if (new_item.item_code===new_item.description || new_item.item_code===new_item.description) {
				new_item.description = null;
			}
			frappe.set_route('Form', 'Item', new_item.name);
		});

		const stock_exists = (frm.doc.__onload
			&& frm.doc.__onload.stock_exists) ? 1 : 0;

		['is_stock_item', 'has_serial_no', 'has_batch_no', 'has_variants'].forEach((fieldname) => {
			frm.set_df_property(fieldname, 'read_only', stock_exists);
		});

		frm.toggle_reqd('customer', frm.doc.is_customer_provided_item ? 1:0);
	},

	validate: function(frm){
		erpnext.item.weight_to_validate(frm);
	},

	image: function() {
		refresh_field("image_view");
	},

	is_customer_provided_item: function(frm) {
		frm.toggle_reqd('customer', frm.doc.is_customer_provided_item ? 1:0);
	},

	is_fixed_asset: function(frm) {
		// set serial no to false & toggles its visibility
		frm.set_value('has_serial_no', 0);
		frm.set_value('has_batch_no', 0);
		frm.toggle_enable(['has_serial_no', 'serial_no_series'], !frm.doc.is_fixed_asset);

		frappe.call({
			method: "erpnext.stock.doctype.item.item.get_asset_naming_series",
			callback: function(r) {
				frm.set_value("is_stock_item", frm.doc.is_fixed_asset ? 0 : 1);
				frm.events.set_asset_naming_series(frm, r.message);
			}
		});

		frm.trigger('auto_create_assets');
	},

	set_asset_naming_series: function(frm, asset_naming_series) {
		if ((frm.doc.__onload && frm.doc.__onload.asset_naming_series) || asset_naming_series) {
			let naming_series = (frm.doc.__onload && frm.doc.__onload.asset_naming_series) || asset_naming_series;
			frm.set_df_property("asset_naming_series", "options", naming_series);
		}
	},

	auto_create_assets: function(frm) {
		frm.toggle_reqd(['asset_naming_series'], frm.doc.auto_create_assets);
		frm.toggle_display(['asset_naming_series'], frm.doc.auto_create_assets);
	},

	page_name: frappe.utils.warn_page_name_change,

	item_code: function(frm) {
		if(!frm.doc.item_name)
			frm.set_value("item_name", frm.doc.item_code);
	},

	is_stock_item: function(frm) {
		if(!frm.doc.is_stock_item) {
			frm.set_value("has_batch_no", 0);
			frm.set_value("create_new_batch", 0);
			frm.set_value("has_serial_no", 0);
		}
	},

	has_variants: function(frm) {
		erpnext.item.toggle_attributes(frm);
	},

	item_category: function(frm) {
		if(frm.doc.item_category){
			frm.set_value("naming_series", frm.doc.item_category+".###.");
		}
	},

	item_group: function(frm) {
		if(frm.doc.item_group == "Tools" || frm.doc.item_group == "Alat Bantu Kerja"){
			frm.set_value("naming_series", "TOOLS.###.");
		}

		if(frm.doc.item_group == "Services"){
			frm.set_value("naming_series", "SERVICES.###.");
		}

		if(frm.doc.item_group == "Products"){
			frm.set_value("naming_series", "PRODUCTS.###.");
		}
	}
});

frappe.ui.form.on('Item Reorder', {
	reorder_levels_add: function(frm, cdt, cdn) {
		var row = frappe.get_doc(cdt, cdn);
		var type = frm.doc.default_material_request_type
		row.material_request_type = (type == 'Material Transfer')? 'Transfer' : type;
	}
})

frappe.ui.form.on('Item Customer Detail', {
	customer_items_add: function(frm, cdt, cdn) {
		frappe.model.set_value(cdt, cdn, 'customer_group', "");
	},
	customer_name: function(frm, cdt, cdn) {
		set_customer_group(frm, cdt, cdn);
	},
	customer_group: function(frm, cdt, cdn) {
		if(set_customer_group(frm, cdt, cdn)){
			frappe.msgprint(__("Changing Customer Group for the selected Customer is not allowed."));
		}
	}
});

var set_customer_group = function(frm, cdt, cdn) {
	var row = frappe.get_doc(cdt, cdn);

	if (!row.customer_name) {
		return false;
	}

	frappe.model.with_doc("Customer", row.customer_name, function() {
		var customer = frappe.model.get_doc("Customer", row.customer_name);
		row.customer_group = customer.customer_group;
		refresh_field("customer_group", cdn, "customer_items");
	});
	return true;
}

$.extend(erpnext.item, {
	setup_queries: function(frm) {
		frm.fields_dict["item_defaults"].grid.get_field("expense_account").get_query = function(doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			return {
				query: "erpnext.controllers.queries.get_expense_account",
				filters: { company: row.company }
			}
		}

		frm.fields_dict["item_defaults"].grid.get_field("income_account").get_query = function(doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			return {
				query: "erpnext.controllers.queries.get_income_account",
				filters: { company: row.company }
			}
		}

		frm.fields_dict["item_defaults"].grid.get_field("default_discount_account").get_query = function(doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			return {
				filters: {
					'report_type': 'Profit and Loss',
					'company': row.company,
					"is_group": 0
				}
			};
		};

		frm.fields_dict["item_defaults"].grid.get_field("buying_cost_center").get_query = function(doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			return {
				filters: {
					"is_group": 0,
					"company": row.company
				}
			}
		}

		frm.fields_dict["item_defaults"].grid.get_field("selling_cost_center").get_query = function(doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			return {
				filters: {
					"is_group": 0,
					"company": row.company
				}
			}
		}


		frm.fields_dict['taxes'].grid.get_field("tax_type").get_query = function(doc, cdt, cdn) {
			return {
				filters: [
					['Account', 'account_type', 'in',
						'Tax, Chargeable, Income Account, Expense Account'],
					['Account', 'docstatus', '!=', 2]
				]
			}
		}

		frm.fields_dict['item_group'].get_query = function(doc, cdt, cdn) {
			return {
				filters: [
					['Item Group', 'docstatus', '!=', 2]
				]
			}
		}

		frm.fields_dict['deferred_revenue_account'].get_query = function() {
			return {
				filters: {
					'root_type': 'Liability',
					"is_group": 0
				}
			}
		}

		frm.fields_dict['deferred_expense_account'].get_query = function() {
			return {
				filters: {
					'root_type': 'Asset',
					"is_group": 0
				}
			}
		}

		frm.fields_dict.customer_items.grid.get_field("customer_name").get_query = function(doc, cdt, cdn) {
			return { query: "erpnext.controllers.queries.customer_query" }
		}

		frm.fields_dict.supplier_items.grid.get_field("supplier").get_query = function(doc, cdt, cdn) {
			return { query: "erpnext.controllers.queries.supplier_query" }
		}

		frm.fields_dict["item_defaults"].grid.get_field("default_warehouse").get_query = function(doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			return {
				filters: {
					"is_group": 0,
					"company": row.company
				}
			}
		}

		frm.fields_dict.reorder_levels.grid.get_field("warehouse_group").get_query = function(doc, cdt, cdn) {
			return {
				filters: { "is_group": 1 }
			}
		}

		frm.fields_dict.reorder_levels.grid.get_field("warehouse").get_query = function(doc, cdt, cdn) {
			var d = locals[cdt][cdn];

			var filters = {
				"is_group": 0
			}

			if (d.parent_warehouse) {
				filters.extend({"parent_warehouse": d.warehouse_group})
			}

			return {
				filters: filters
			}
		}

		frm.set_query('default_provisional_account', 'item_defaults', (doc, cdt, cdn) => {
			let row = locals[cdt][cdn];
			return {
				filters: {
					"company": row.company,
					"root_type": ["in", ["Liability", "Asset"]],
					"is_group": 0
				}
			};
		});

	},

	make_dashboard: function(frm) {
		if(frm.doc.__islocal)
			return;

		// Show Stock Levels only if is_stock_item
		if (frm.doc.is_stock_item) {
			frappe.require('assets/js/item-dashboard.min.js', function() {
				const section = frm.dashboard.add_section('', __("Stock Levels"));
				erpnext.item.item_dashboard = new erpnext.stock.ItemDashboard({
					parent: section,
					item_code: frm.doc.name,
					page_length: 20,
					method: 'erpnext.stock.dashboard.item_dashboard.get_data',
					template: 'item_dashboard_list'
				});
				erpnext.item.item_dashboard.refresh();
			});
		}
	},

	edit_prices_button: function(frm) {
		frm.add_custom_button(__("Add / Edit Prices"), function() {
			frappe.set_route("List", "Item Price", {"item_code": frm.doc.name});
		}, __("Actions"));
	},

	weight_to_validate: function(frm) {
		if (frm.doc.weight_per_unit && !frm.doc.weight_uom) {
			frappe.msgprint({
				message: __("Please mention 'Weight UOM' along with Weight."),
				title: __("Note")
			});
		}
	},

	show_modal_for_manufacturers: function(frm) {
		var dialog = new frappe.ui.Dialog({
			fields: [
				{
					fieldtype: 'Link',
					fieldname: 'manufacturer',
					options: 'Manufacturer',
					label: 'Manufacturer',
					reqd: 1,
				},
				{
					fieldtype: 'Data',
					label: 'Manufacturer Part Number',
					fieldname: 'manufacturer_part_no'
				},
			]
		});

		dialog.set_primary_action(__('Create'), function() {
			var data = dialog.get_values();
			if(!data) return;

			// call the server to make the variant
			data.template = frm.doc.name;
			frappe.call({
				method: "erpnext.controllers.item_variant.get_variant",
				args: data,
				callback: function(r) {
					var doclist = frappe.model.sync(r.message);
					dialog.hide();
					frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
				}
			});
		})

		dialog.show();
	},

	show_multiple_variants_dialog: function(frm) {
		var me = this;

		let promises = [];
		let attr_val_fields = {};

		function make_fields_from_attribute_values(attr_dict) {
			let fields = [];
			Object.keys(attr_dict).forEach((name, i) => {
				if(i % 3 === 0){
					fields.push({fieldtype: 'Section Break'});
				}
				fields.push({fieldtype: 'Column Break', label: name});
				attr_dict[name].forEach(value => {
					fields.push({
						fieldtype: 'Check',
						label: value,
						fieldname: value,
						default: 0,
						onchange: function() {
							let selected_attributes = get_selected_attributes();
							let lengths = [];
							Object.keys(selected_attributes).map(key => {
								lengths.push(selected_attributes[key].length);
							});
							if(lengths.includes(0)) {
								me.multiple_variant_dialog.get_primary_btn().html(__('Create Variants'));
								me.multiple_variant_dialog.disable_primary_action();
							} else {

								let no_of_combinations = lengths.reduce((a, b) => a * b, 1);
								let msg;
								if (no_of_combinations === 1) {
									msg = __("Make {0} Variant", [no_of_combinations]);
								} else {
									msg = __("Make {0} Variants", [no_of_combinations]);
								}
								me.multiple_variant_dialog.get_primary_btn().html(msg);
								me.multiple_variant_dialog.enable_primary_action();
							}
						}
					});
				});
			});
			return fields;
		}

		function make_and_show_dialog(fields) {
			me.multiple_variant_dialog = new frappe.ui.Dialog({
				title: __("Select Attribute Values"),
				fields: [
					{
						fieldtype: "HTML",
						fieldname: "help",
						options: `<label class="control-label">
							${__("Select at least one value from each of the attributes.")}
						</label>`,
					}
				].concat(fields)
			});

			me.multiple_variant_dialog.set_primary_action(__('Create Variants'), () => {
				let selected_attributes = get_selected_attributes();

				me.multiple_variant_dialog.hide();
				frappe.call({
					method: "erpnext.controllers.item_variant.enqueue_multiple_variant_creation",
					args: {
						"item": frm.doc.name,
						"args": selected_attributes
					},
					callback: function(r) {
						if (r.message==='queued') {
							frappe.show_alert({
								message: __("Variant creation has been queued."),
								indicator: 'orange'
							});
						} else {
							frappe.show_alert({
								message: __("{0} variants created.", [r.message]),
								indicator: 'green'
							});
						}
					}
				});
			});

			$($(me.multiple_variant_dialog.$wrapper.find('.form-column'))
				.find('.frappe-control')).css('margin-bottom', '0px');

			me.multiple_variant_dialog.disable_primary_action();
			me.multiple_variant_dialog.clear();
			me.multiple_variant_dialog.show();
		}

		function get_selected_attributes() {
			let selected_attributes = {};
			me.multiple_variant_dialog.$wrapper.find('.form-column').each((i, col) => {
				if(i===0) return;
				let attribute_name = $(col).find('label').html().trim();
				selected_attributes[attribute_name] = [];
				let checked_opts = $(col).find('.checkbox input');
				checked_opts.each((i, opt) => {
					if($(opt).is(':checked')) {
						selected_attributes[attribute_name].push($(opt).attr('data-fieldname'));
					}
				});
			});

			return selected_attributes;
		}

		frm.doc.attributes.forEach(function(d) {
			let p = new Promise(resolve => {
				if(!d.numeric_values) {
					frappe.call({
						method: "frappe.client.get_list",
						args: {
							doctype: "Item Attribute Value",
							filters: [
								["parent","=", d.attribute]
							],
							fields: ["attribute_value"],
							limit_page_length: 0,
							parent: "Item Attribute",
							order_by: "idx"
						}
					}).then((r) => {
						if(r.message) {
							attr_val_fields[d.attribute] = r.message.map(function(d) { return d.attribute_value; });
							resolve();
						}
					});
				} else {
					frappe.call({
						method: "frappe.client.get",
						args: {
							doctype: "Item Attribute",
							name: d.attribute
						}
					}).then((r) => {
						if(r.message) {
							const from = r.message.from_range;
							const to = r.message.to_range;
							const increment = r.message.increment;

							let values = [];
							for(var i = from; i <= to; i = flt(i + increment, 6)) {
								values.push(i);
							}
							attr_val_fields[d.attribute] = values;
							resolve();
						}
					});
				}
			});

			promises.push(p);

		}, this);

		Promise.all(promises).then(() => {
			let fields = make_fields_from_attribute_values(attr_val_fields);
			make_and_show_dialog(fields);
		})

	},

	show_single_variant_dialog: function(frm) {
		var fields = []

		for(var i=0;i< frm.doc.attributes.length;i++){
			var fieldtype, desc;
			var row = frm.doc.attributes[i];
			if (row.numeric_values){
				fieldtype = "Float";
				desc = "Min Value: "+ row.from_range +" , Max Value: "+ row.to_range +", in Increments of: "+ row.increment
			}
			else {
				fieldtype = "Data";
				desc = ""
			}
			fields = fields.concat({
				"label": row.attribute,
				"fieldname": row.attribute,
				"fieldtype": fieldtype,
				"reqd": 0,
				"description": desc
			})
		}

		var d = new frappe.ui.Dialog({
			title: __('Create Variant'),
			fields: fields
		});

		d.set_primary_action(__('Create'), function() {
			var args = d.get_values();
			if(!args) return;
			frappe.call({
				method: "erpnext.controllers.item_variant.get_variant",
				btn: d.get_primary_btn(),
				args: {
					"template": frm.doc.name,
					"args": d.get_values()
				},
				callback: function(r) {
					// returns variant item
					if (r.message) {
						var variant = r.message;
						frappe.msgprint_dialog = frappe.msgprint(__("Item Variant {0} already exists with same attributes",
							[repl('<a href="/app/item/%(item_encoded)s" class="strong variant-click">%(item)s</a>', {
								item_encoded: encodeURIComponent(variant),
								item: variant
							})]
						));
						frappe.msgprint_dialog.hide_on_page_refresh = true;
						frappe.msgprint_dialog.$wrapper.find(".variant-click").on("click", function() {
							d.hide();
						});
					} else {
						d.hide();
						frappe.call({
							method: "erpnext.controllers.item_variant.create_variant",
							args: {
								"item": frm.doc.name,
								"args": d.get_values()
							},
							callback: function(r) {
								var doclist = frappe.model.sync(r.message);
								frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
							}
						});
					}
				}
			});
		});

		d.show();

		$.each(d.fields_dict, function(i, field) {

			if(field.df.fieldtype !== "Data") {
				return;
			}

			$(field.input_area).addClass("ui-front");

			var input = field.$input.get(0);
			input.awesomplete = new Awesomplete(input, {
				minChars: 0,
				maxItems: 99,
				autoFirst: true,
				list: [],
			});
			input.field = field;

			field.$input
				.on('input', function(e) {
					var term = e.target.value;
					frappe.call({
						method: "erpnext.stock.doctype.item.item.get_item_attribute",
						args: {
							parent: i,
							attribute_value: term
						},
						callback: function(r) {
							if (r.message) {
								e.target.awesomplete.list = r.message.map(function(d) { return d.attribute_value; });
							}
						}
					});
				})
				.on('focus', function(e) {
					$(e.target).val('').trigger('input');
				})
				.on("awesomplete-open", () => {
					let modal = field.$input.parents('.modal-dialog')[0];
					if (modal) {
						$(modal).removeClass("modal-dialog-scrollable");
					}
				})
				.on("awesomplete-close", () => {
					let modal = field.$input.parents('.modal-dialog')[0];
					if (modal) {
						$(modal).addClass("modal-dialog-scrollable");
					}
				});
		});
	},

	toggle_attributes: function(frm) {
		if((frm.doc.has_variants || frm.doc.variant_of)
			&& frm.doc.variant_based_on==='Item Attribute') {
			frm.toggle_display("attributes", true);

			var grid = frm.fields_dict.attributes.grid;

			if(frm.doc.variant_of) {
				// variant

				// value column is displayed but not editable
				grid.set_column_disp("attribute_value", true);
				grid.toggle_enable("attribute_value", false);

				grid.toggle_enable("attribute", false);

				// can't change attributes since they are
				// saved when the variant was created
				frm.toggle_enable("attributes", false);
			} else {
				// template - values not required!

				// make the grid editable
				frm.toggle_enable("attributes", true);

				// value column is hidden
				grid.set_column_disp("attribute_value", false);

				// enable the grid so you can add more attributes
				grid.toggle_enable("attribute", true);
			}

		} else {
			// nothing to do with attributes, hide it
			frm.toggle_display("attributes", false);
		}
		frm.layout.refresh_sections();
	}
});

frappe.ui.form.on("UOM Conversion Detail", {
	uom: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.uom) {
			frappe.call({
				method: "erpnext.stock.doctype.item.item.get_uom_conv_factor",
				args: {
					"uom": row.uom,
					"stock_uom": frm.doc.stock_uom
				},
				callback: function(r) {
					if (!r.exc && r.message) {
						frappe.model.set_value(cdt, cdn, "conversion_factor", r.message);
					}
				}
			});
		}
	}
});

function open_form(frm, doctype, child_doctype, parentfield) {
	frappe.model.with_doctype(doctype, () => {
		let new_doc = frappe.model.get_new_doc(doctype);

		let new_child_doc = frappe.model.add_child(new_doc, child_doctype, parentfield);
		new_child_doc.item_code = frm.doc.name;
		new_child_doc.item_name = frm.doc.item_name;
		new_child_doc.uom = frm.doc.stock_uom;
		new_child_doc.description = frm.doc.description;

		frappe.ui.form.make_quick_entry(doctype, null, null, new_doc);
	});
}
