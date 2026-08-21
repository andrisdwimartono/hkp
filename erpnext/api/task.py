import frappe
from datetime import datetime, timedelta

def create_tasks(docname):
    task_import = frappe.get_doc("Task Import", docname)
    task_import.create_tasks()

def cancel_tasks(docname):
    task_import = frappe.get_doc("Task Import", docname)
    task_import.cancel_tasks()

@frappe.whitelist(allow_guest=False)
def get_tasks_for_calendar(project=None):
    filters = {}
    if project:
        filters["project"] = project

    tasks = frappe.get_all(
        "Task",
        filters=filters,
        fields=["name", "subject", "project", "exp_start_date", "exp_end_date", "status", "color", "is_group", "task_weight", "completed_on", "progress"]
    )

    return tasks
    