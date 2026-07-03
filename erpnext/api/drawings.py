import frappe
from datetime import datetime

@frappe.whitelist()
def get_drawings_status_count(project=None):
    if project:
        return frappe.db.sql("""
            SELECT
                MAX(ddd.name) as name,
                dd.status,
                COUNT(dd.name) AS count_status
            FROM `tabDetail Design Drawing` AS ddd
            LEFT JOIN `tabDesign Detail` AS dd ON dd.parent = ddd.name AND dd.parenttype = 'Detail Design Drawing'
            WHERE ddd.project = %(project)s
            GROUP BY dd.status
        """, {"project": project}, as_dict=True)
    return None

@frappe.whitelist()
def get_drawings_last_5_updates(project=None):
    if project:
        # get data of versions
        versions = frappe.db.sql("""
            SELECT
                ver.creation,
                ver.data
            FROM `tabDetail Design Drawing` AS ddd
            LEFT JOIN `tabVersion` AS ver ON ver.ref_doctype = 'Detail Design Drawing' AND ver.docname = ddd.name
            WHERE ddd.project = %(project)s
            ORDER BY ver.creation ASC
        """, {"project": project}, as_dict=True)
        if versions:
            # merge all data (json) to one variable
            all_data = []
            for ver in versions:
                # convert ver.data to dict
                detail = frappe.parse_json(ver.data)
                data = {
                    "creation": ver.creation,
                    "detail": detail
                }
                # save list
                all_data.append(data)
            activities = get_last_activities(all_data)
            return activities
    return None

from copy import deepcopy

def get_last_activities(all_data, limit=5):
    # ---------------------------------------
    # Pass 1
    # Index seluruh row details dari "added"
    # ---------------------------------------
    detail_index = {}

    for version in all_data:
        detail = version.get("detail", {})

        for added in detail.get("added", []):
            if added[0] != "details":
                continue

            row = deepcopy(added[1])

            detail_index[row["name"]] = {
                "name": row.get("name"),
                "drawing": row.get("drawing"),
                "previous_status": row.get("status"),
                "status": row.get("status"),
                "owner": row.get("owner")
            }

    # ---------------------------------------
    # Pass 2
    # Generate activity
    # ---------------------------------------
    activities = []

    for version in all_data:
        detail = version.get("detail", {})

        #
        # Added
        #
        for added in detail.get("added", []):
            if added[0] != "details":
                continue

            row = added[1]

            activities.append({
                "type": "added",
                "name": row.get("name"),
                "drawing": row.get("drawing"),
                "previous_status": row.get("status"),
                "status": row.get("status"),
                "owner": row.get("owner"),
                "creation": version["creation"]
            })

        #
        # Row Changed
        #
        for row_changed in detail.get("row_changed", []):

            if row_changed[0] != "details":
                continue

            row_name = row_changed[2]

            row_info = detail_index.get(row_name)

            if not row_info:
                continue

            # Cari perubahan status saja
            for change in row_changed[3]:

                field = change[0]

                if field != "status":
                    continue

                activities.append({
                    "type": "row_changed",
                    "name": row_name,
                    "drawing": row_info["drawing"],
                    "previous_status": change[1],
                    "status": change[2],      # nilai baru
                    "owner": row_info["owner"],
                    "creation": version["creation"]
                })

                break

    # ---------------------------------------
    # Urutkan terbaru
    # ---------------------------------------
    activities.sort(
        key=lambda x: x["creation"],
        reverse=True
    )

    return activities[:limit]