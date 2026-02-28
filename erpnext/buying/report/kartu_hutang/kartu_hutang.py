# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = [
		{
			"label": "Type",
			"fieldname": "type",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": "No. SPK/SPB",
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Sub Contract Hand Over",
			"width": 150
		},
		{
			"label": "Tanggal",
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": "Vendor",
			"fieldname": "sub_contract",
			"fieldtype": "Link",
			"options": "Sub Contract Hand Over",
			"width": 150
		},
		{
			"label": "Nama Vendor",
			"fieldname": "contractor_name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": "Project",
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 150
		},
		{
			"label": "Nama Project",
			"fieldname": "project_name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": "Nilai Kontrak",
			"fieldname": "budget_amount",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": "Progress",
			"fieldname": "progress_achieved",
			"fieldtype": "Percent",
			"width": 80
		},
		{
			"label": "Total Dibayar",
			"fieldname": "total_paid",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": "Sisa Kontrak",
			"fieldname": "sisa_budget",
			"fieldtype": "Currency",
			"width": 150
		}
	]
	data = get_data(filters)
	return columns, data

def get_data(filters=None):
	whereSPK = "WHERE spk.docstatus = 0"
	whereSPB = "WHERE spb.docstatus = 1"
	if filters:
		if filters.get("project"):
			whereSPK += " AND spk.project = '{0}'".format(filters.get("project"))
			whereSPB += " AND spb.project = '{0}'".format(filters.get("project"))
		if filters.get("sub_contract"):
			whereSPK += " AND spk.sub_contract = '{0}'".format(filters.get("sub_contract"))
			if not filters.get("supplier"):
				whereSPB += " AND spb.supplier = '{0}'".format(filters.get("sub_contract"))
		if filters.get("spk"):
			whereSPK += " AND spk.name = '{0}'".format(filters.get("spk"))
			if not filters.get("purchase_order"):
				whereSPB += " AND spb.name = '{0}'".format(filters.get("spk"))
		if filters.get("supplier"):
			whereSPB += " AND spb.supplier = '{0}'".format(filters.get("supplier"))
			if not filters.get("sub_contract"):
				whereSPK += " AND spk.sub_contract = '{0}'".format(filters.get("supplier"))
		if filters.get("purchase_order"):
			whereSPB += " AND spb.name = '{0}'".format(filters.get("purchase_order"))
			if not filters.get("spk"):
				whereSPK += " AND spk.name = '{0}'".format(filters.get("purchase_order"))
	return frappe.db.sql(
		"""
		SELECT
			'SPK' AS type,
			spk.name,
			spk.posting_date,
			spk.sub_contract,
			spk.contractor_name,
			spk.project,
			spk.project_name,
			spk.budget_amount,
			COALESCE(progress.progress_achieved, 0) AS progress_achieved,
			COALESCE(realisasi.total_paid, 0) AS total_paid,
			COALESCE(spk.budget_amount - realisasi.total_paid, 0) AS sisa_budget
		FROM `tabSub Contract Hand Over` AS spk
		LEFT JOIN (
			SELECT
				prog.sub_contract_hand_over,
				MAX(prog.progress_achieved) AS progress_achieved
			FROM `tabHand Over Progress` prog
			WHERE prog.docstatus = 1
			GROUP BY prog.sub_contract_hand_over
		) AS progress ON progress.sub_contract_hand_over = spk.name
		LEFT JOIN (
			SELECT
				reali.sub_contract_hand_over,
				SUM(reali.paid) AS total_paid
			FROM `tabSlip Pembayaran Subkon` AS reali
			GROUP BY reali.sub_contract_hand_over
		) AS realisasi ON realisasi.sub_contract_hand_over = spk.name
		{0}
		UNION
		SELECT
			'SPB' AS type,
			spb.name,
			spb.transaction_date AS posting_date,
			spb.supplier AS sub_contract,
			spb.supplier AS contractor_name,
			spb.project,
			spb.project_name,
			spb.grand_total AS budget_amount,
			CASE WHEN spb.grand_total IS NOT NULL AND spb.grand_total > 0 THEN realisasi.total_paid/spb.grand_total*100 ELSE 0 END AS progress_achieved,
			COALESCE(realisasi.total_paid, 0) AS total_paid,
			COALESCE(spb.grand_total - realisasi.total_paid, 0) AS sisa_budget
		FROM
			`tabPurchase Order` spb
		LEFT JOIN
			(
				SELECT
					reali.purchase_order,
					SUM(reali.total_budget) AS total_paid
				FROM `tabForm Payment Entry Supplier` reali
				WHERE reali.docstatus = 1
				GROUP BY reali.purchase_order
			) realisasi ON spb.name = realisasi.purchase_order
		{1}
		""".format(whereSPK, whereSPB), as_dict=1)

@frappe.whitelist()
def get_supplier_by_project(project):
	return frappe.db.sql("SELECT supplier FROM `tabPurchase Order` WHERE project = %s AND docstatus = 1", project, as_dict=1)