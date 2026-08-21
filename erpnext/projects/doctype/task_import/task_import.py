# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from io import BytesIO

import frappe
from openpyxl import load_workbook
from openpyxl.utils.datetime import from_excel
import re

from frappe.model.document import Document

class TaskImport(Document):
	def validate(self):
		if not self.file:
			return

		# Kosongkan child table
		self.set("detail", [])

		file_doc = frappe.get_doc("File", {"file_url": self.file})
		content = file_doc.get_content()

		workbook = load_workbook(
			filename=BytesIO(content),
			data_only=True
		)

		worksheet = workbook.active

		# ==========================
		# Mapping Header
		# ==========================
		headers = {}

		for i, cell in enumerate(worksheet[1], start=1):
			if cell.value:
				headers[str(cell.value).strip()] = i

		required_columns = [
			"ID",
			"Task Name",
			"Start",
			"Finish",
			"Predecessors"
		]

		for column in required_columns:
			if column not in headers:
				frappe.throw("Column <b>{0}</b> not found.".format(column))

		# ==========================
		# Read Excel
		# ==========================
		rows = []

		for row in worksheet.iter_rows(min_row=2):

			task_cell = row[headers["Task Name"] - 1]

			if not task_cell.value:
				continue

			subject = str(task_cell.value)

			# Hitung jumlah spasi di depan
			leading_spaces = len(subject) - len(subject.lstrip())

			# MS Project copy-paste menggunakan 3 spasi setiap level
			outline_level = (leading_spaces // 3) + 1

			rows.append({
				"task_id": row[headers["ID"] - 1].value,
				"subject": subject.strip(),
				"start": row[headers["Start"] - 1].value,
				"finish": row[headers["Finish"] - 1].value,
				"predecessors": row[headers["Predecessors"] - 1].value or "",
				"outline_level": outline_level
			})

		# ==========================
		# Generate Child Table
		# ==========================
		for i, row in enumerate(rows):

			is_group = 0

			# Jika level task berikutnya lebih dalam,
			# maka task sekarang adalah group
			if i < len(rows) - 1:
				if rows[i + 1]["outline_level"] > row["outline_level"]:
					is_group = 1

			start_date = row["start"]
			finish_date = row["finish"]

			if isinstance(start_date, (int, float)):
				start_date = from_excel(start_date)

			if isinstance(finish_date, (int, float)):
				finish_date = from_excel(finish_date)

			self.append("detail", {
				"task_id": row["task_id"],
				"subject": row["subject"],
				"exp_start_date": start_date,
				"exp_end_date": finish_date,
				"outline_level": row["outline_level"],
				"is_group": is_group,
				"predecessors": str(row["predecessors"]).strip()
			})
	def on_submit(self):
		frappe.enqueue(
			"erpnext.api.task.create_tasks",
			queue="short",
			docname=self.name,
			enqueue_after_commit=True
		)

	def on_cancel(self):
		frappe.enqueue(
			"erpnext.api.task.cancel_tasks",
			queue="short",
			docname=self.name,
			enqueue_after_commit=True
		)

	def create_tasks(self):
		task_map = {}

		# =====================================================
		# 1. Create semua Task terlebih dahulu
		# =====================================================

		for d in self.detail:

			task = frappe.new_doc("Task")
			task.project = self.project
			task.subject = d.subject
			task.exp_start_date = d.exp_start_date
			task.exp_end_date = d.exp_end_date
			task.status = "Open"

			task.insert(ignore_permissions=True)
			frappe.db.commit()

			d.db_set(
				"task",
				task.name,
				update_modified=False
			)

			d.task = task.name

			task_map[int(d.task_id)] = task.name

		# =====================================================
		# 2. Tentukan Parent Task berdasarkan Outline Level
		# =====================================================

		stack = []

		for d in self.detail:

			while stack and stack[-1]["level"] >= d.outline_level:
				stack.pop()

			if stack:
				frappe.db.set_value(
					"Task",
					d.task,
					"parent_task",
					stack[-1]["task"],
					update_modified=False
				)

			stack.append({
				"task": d.task,
				"task_id": d.task_id,
				"level": d.outline_level
			})

		# =====================================================
		# 3. Generate Dependent Tasks
		# =====================================================

		total = len(self.detail)
		completed = 0
		for d in self.detail:

			if d.predecessors:
				task = frappe.get_doc("Task", d.task)
				task.set("depends_on", [])

				predecessors = str(d.predecessors).split(",")

				for predecessor in predecessors:
					predecessor = predecessor.strip()
					if not predecessor:
						continue

					# Ambil angka di depan
					match = re.match(r"(\d+)", predecessor)
					if not match:
						continue

					predecessor_id = int(match.group(1))
					if predecessor_id not in task_map:
						continue

					task.append("depends_on", {
						"task": task_map[predecessor_id]
					})

				task.save(ignore_permissions=True)

			completed += 1
			progress = round((completed / total) * 100, 2)

			frappe.publish_realtime(
				"task_sync_progress",
				{
					"docname": self.name,
					"progress": progress,
					"completed": completed,
					"total": total
				}
			)
		# doc reload
		self.reload()

	def cancel_tasks(self):
		for d in self.detail:
			if not d.task:
				continue
			if not frappe.db.exists("Task", d.task):
				continue
			task = frappe.get_doc("Task", d.task)
			task.status = "Cancelled"
			task.save(ignore_permissions=True)