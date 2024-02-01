# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _, throw
from frappe.desk.form import assign_to
from frappe.model.document import Document
from frappe.utils import add_days, add_months, add_years, getdate, nowdate


class AssetMaintenance(Document):
	def validate(self):
		for task in self.get("asset_maintenance_tasks"):
			if task.end_date and (getdate(task.start_date) >= getdate(task.end_date)):
				throw(_("Start date should be less than end date for task {0}").format(task.maintenance_task))
			if getdate(task.next_due_date) < getdate(nowdate()):
				task.maintenance_status = "Overdue"
			if not task.assign_to and self.docstatus == 0:
				throw(_("Row #{}: Please asign task to a member.").format(task.idx))

	def on_update(self):
		for task in self.get("asset_maintenance_tasks"):
			assign_tasks(self.name, task.assign_to, task.maintenance_task, task.next_due_date)
		self.sync_maintenance_tasks()

	def sync_maintenance_tasks(self):
		tasks_names = []
		for task in self.get("asset_maintenance_tasks"):
			tasks_names.append(task.name)
			update_maintenance_log(
				asset_maintenance=self.name, item_code=self.item_code, item_name=self.item_name, task=task
			)
		asset_maintenance_logs = frappe.get_all(
			"Asset Maintenance Log",
			fields=["name"],
			filters={"asset_maintenance": self.name, "task": ("not in", tasks_names)},
		)
		if asset_maintenance_logs:
			for asset_maintenance_log in asset_maintenance_logs:
				maintenance_log = frappe.get_doc("Asset Maintenance Log", asset_maintenance_log.name)
				maintenance_log.db_set("maintenance_status", "Cancelled")


@frappe.whitelist()
def assign_tasks(asset_maintenance_name, assign_to_member, maintenance_task, next_due_date):
	team_member = frappe.db.get_value("User", assign_to_member, "email")
	args = {
		"doctype": "Asset Maintenance",
		"assign_to": [team_member],
		"name": asset_maintenance_name,
		"description": maintenance_task,
		"date": next_due_date,
	}
	if not frappe.db.sql(
		"""select owner from `tabToDo`
		where reference_type=%(doctype)s and reference_name=%(name)s and status="Open"
		and owner=%(assign_to)s""",
		args,
	):
		assign_to.add(args)


@frappe.whitelist()
def calculate_next_due_date(
	periodicity, start_date=None, end_date=None, last_completion_date=None, next_due_date=None
):
	if not start_date and not last_completion_date:
		start_date = frappe.utils.now()

	if last_completion_date and (
		(start_date and last_completion_date > start_date) or not start_date
	):
		start_date = last_completion_date
	if periodicity == "Daily":
		next_due_date = add_days(start_date, 1)
	if periodicity == "Weekly":
		next_due_date = add_days(start_date, 7)
	if periodicity == "Monthly":
		next_due_date = add_months(start_date, 1)
	if periodicity == "Yearly":
		next_due_date = add_years(start_date, 1)
	if periodicity == "2 Yearly":
		next_due_date = add_years(start_date, 2)
	if periodicity == "Quarterly":
		next_due_date = add_months(start_date, 3)
	if end_date and (
		(start_date and start_date >= end_date)
		or (last_completion_date and last_completion_date >= end_date)
		or next_due_date
	):
		next_due_date = ""
	return next_due_date


def update_maintenance_log(asset_maintenance, item_code, item_name, task):
	asset_maintenance_log = frappe.get_value(
		"Asset Maintenance Log",
		{
			"asset_maintenance": asset_maintenance,
			"task": task.name,
			"maintenance_status": ("in", ["Planned", "Overdue"]),
		},
	)

	if not asset_maintenance_log:
		asset_maintenance_log = frappe.get_doc(
			{
				"doctype": "Asset Maintenance Log",
				"asset_maintenance": asset_maintenance,
				"asset_name": asset_maintenance,
				"item_code": item_code,
				"item_name": item_name,
				"task": task.name,
				"has_certificate": task.certificate_required,
				"description": task.description,
				"assign_to_name": task.assign_to_name,
				"periodicity": str(task.periodicity),
				"maintenance_type": task.maintenance_type,
				"due_date": task.next_due_date,
			}
		)
		asset_maintenance_log.insert()
	else:
		maintenance_log = frappe.get_doc("Asset Maintenance Log", asset_maintenance_log)
		maintenance_log.assign_to_name = task.assign_to_name
		maintenance_log.has_certificate = task.certificate_required
		maintenance_log.description = task.description
		maintenance_log.periodicity = str(task.periodicity)
		maintenance_log.maintenance_type = task.maintenance_type
		maintenance_log.due_date = task.next_due_date
		maintenance_log.save()


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_team_members(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.get_values(
		"Maintenance Team Member", {"parent": filters.get("maintenance_team")}, "team_member"
	)

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_team_members2(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.get_values(
		"Maintenance Team Member", {"parent": filters.get("maintenance_team")}, "employee"
	)

@frappe.whitelist()
def get_maintenance_log(asset_name):
	return frappe.db.sql(
		"""
        select maintenance_status, count(asset_name) as count, asset_name
        from `tabAsset Maintenance Log`
        where asset_name=%s group by maintenance_status""",
		(asset_name),
		as_dict=1,
	)

@frappe.whitelist()
def create_asset_maintenance():
	bulan_depan = getdate(add_months(nowdate(), 1))
	amts = frappe.db.sql("""SELECT * FROM `tabAsset Maintenance Task` amt WHERE amt.next_due_date = '{0}' and amt.periodicity IN ('Monthly', 'Quarterly', 'Yearly', '2 Yearly')""".format(bulan_depan), as_dict=1)

	amts2 = frappe.db.sql("""SELECT * FROM `tabAsset Maintenance Task` amt WHERE amt.next_due_date = '{0}' and amt.periodicity IN ('Weekly')""".format(getdate(add_days(nowdate(), 7))), as_dict=1)
	amts = amts+amts2
	amts3 = frappe.db.sql("""SELECT * FROM `tabAsset Maintenance Task` amt WHERE amt.next_due_date = '{0}' and amt.periodicity IN ('Daily')""".format(getdate(add_days(nowdate(), 1))), as_dict=1)
	amts = amts+amts3
	for amt in amts:
		asset_maintenance_doc = frappe.get_doc("Asset Maintenance", amt.parent)
		next_due_date = calculate_next_due_date(
			amt.periodicity, start_date=amt.next_due_date, end_date=None, last_completion_date=None, next_due_date=None
		)
		last_completion_date = None
		if amt.last_completion_date:
			last_completion_date = calculate_next_due_date(
				amt.periodicity, start_date=amt.last_completion_date, end_date=None, last_completion_date=None, next_due_date=None
			)
		asset_maintenance_doc.append("asset_maintenance_tasks", {
			"maintenance_task": amt.maintenance_task,
			"maintenance_status": "Planned",
			"periodicity": amt.periodicity,
			"start_date": amt.next_due_date,
			"end_date": amt.last_completion_date,
			"next_due_date": next_due_date,
			"last_completion_date": last_completion_date,
			"assign_to_employee": amt.assign_to_employee,
			"assign_to": amt.assign_to,
			"description": amt.description
		})
		asset_maintenance_doc.save()

@frappe.whitelist()
def get_asset_maintenance_task():
	next_due_date = getdate(add_days(nowdate(), 7))
	amts = frappe.db.sql("""SELECT * FROM `tabAsset Maintenance Task` WHERE next_due_date = '{0}'""".format(next_due_date), as_dict=1)
	if amts:
		for amt in amts:
			assigner = []
			x = frappe.get_doc("Asset Maintenance", amt.parent)
			log_employees = frappe.db.sql("""SELECT DISTINCT u.name user_id FROM `tabHas Role` hr
							INNER JOIN tabUser u ON u.name = hr.parent
							WHERE hr.role IN ('Logistik') AND hr.parenttype = 'User'""", as_dict=1)
			for adu in log_employees:
				assigner.append(adu.user_id)
				x.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(adu.user_id))

			assigner.append(amt.assign_to)
			x.add_comment('Edit', text='Notifikasi terkirim ke {0}'.format(amt.assign_to))
			notification_doc = {
				"type": "Alert",
				"document_type": amt.parenttype,
				"document_name": amt.parent,
				"subject": "{1} di tanggal {0}".format(amt.parent, amt.maintenance_task),
				"from_user": amt.owner,
			}
			
			notification_doc = frappe._dict(notification_doc)
			from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
			make_notification_logs(notification_doc, assigner)