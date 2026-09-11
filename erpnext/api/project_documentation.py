import frappe

@frappe.whitelist()
def get_project_documentation_by_project(project):
    if project:
        return frappe.db.sql("""
            SELECT
                docs.name,
                docs.creation,
                docs.modified,
                docs.owner,
                docs.date,
                docs.description,
                docs.file
            FROM `tabProject Documentation` AS parent
            LEFT JOIN `tabProject Documentation` AS docs ON docs.parent_project_documentation = parent.name
            WHERE parent.project = %(project)s
            ORDER BY docs.lft
        """, {"project": project}, as_dict=True)
    return None
