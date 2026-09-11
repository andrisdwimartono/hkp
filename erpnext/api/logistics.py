import frappe
from datetime import datetime, timedelta

@frappe.whitelist()
def get_logistics_counter(project=None):
    """
    Get logistics counter
    """
    po_count = []
    po_filter = ""
    if project is not None:
        po_filter = """AND po.project = '{project}'""".format(project=project)

    po_count = frappe.db.sql("""
        SELECT
            SUM(CASE WHEN po.docstatus = 1 THEN 1 ELSE 0 END) AS submitted_po_count,
            SUM(CASE WHEN po.docstatus = 0 THEN 1 ELSE 0 END) AS draft_po_count
        FROM `tabPurchase Order` AS po
        WHERE po.docstatus IN (0, 1)
        {po_filter}
    """.format(po_filter=po_filter), as_dict=True)

    material_on_site = frappe.db.sql("""
        SELECT
            COUNT(DISTINCT poi.item_code) AS count_item
        FROM `tabPurchase Order` AS po
        INNER JOIN `tabPurchase Order Item` AS poi ON poi.parent = po.name AND poi.parenttype = 'Purchase Order'
        WHERE po.docstatus = 1
        {po_filter}
        AND poi.status = 'Delivered'
    """.format(po_filter=po_filter), as_dict=True)

    shipment_in_transit = frappe.db.sql("""
        SELECT
            COUNT(DISTINCT poi.item_code) AS count_item
        FROM `tabPurchase Order` AS po
        INNER JOIN `tabPurchase Order Item` AS poi ON poi.parent = po.name AND poi.parenttype = 'Purchase Order'
        WHERE po.docstatus = 1
        {po_filter}
        AND poi.status = 'Delivering'
    """.format(po_filter=po_filter), as_dict=True)

    material_status = frappe.db.sql("""
        SELECT
            SUM(CASE WHEN DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) > 14 THEN 1 ELSE 0 END) AS green_count,
            SUM(CASE WHEN DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) > 7 AND DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) <=14 THEN 1 ELSE 0 END) AS yellow_count,
            SUM(CASE WHEN DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) <=7 THEN 1 ELSE 0 END) AS red_count
        FROM `tabPurchase Order` AS po
        WHERE po.docstatus = 1
        AND po.delivered_time_schedule IS NOT NULL
        AND DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) <= 30
        {po_filter}
        ORDER BY DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) DESC 
    """.format(po_filter=po_filter), as_dict=True)
    
    return {
        "submitted_po_count": po_count[0]["submitted_po_count"],
        "draft_po_count": po_count[0]["draft_po_count"],
        "material_on_site": material_on_site[0]["count_item"],
        "shipment_in_transit": shipment_in_transit[0]["count_item"],
        "potential_material_delays": material_status[0].red_count,
    }

@frappe.whitelist()
def get_table_material_po(project=None, search=None, status=None, page=1, limit=10):
    if project is not None:
        po_filter = "AND po.project = '{project}'".format(project=project)
    else:
        po_filter = ""
    if search is not None:
        search_filter = "AND (po.name LIKE '%{search}%' OR po.supplier_name LIKE '%{search}%' OR po.material_grouping LIKE '%{search}%')".format(search=search)
    else:
        search_filter = ""

    status_filter = ""
    if status is not None:
        if status == 'green':
            status_filter = "AND DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) > 14"
        elif status == 'yellow':
            status_filter = "AND DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) > 7 AND DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) <=14"
        elif status == 'red':
            status_filter = "AND DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) <=7"
    
    data = frappe.db.sql("""
    SELECT
        po.name AS po_no,
        po.supplier,
        po.supplier_name,
        po.material_grouping AS item_name,
        po.inspecting_time,
        po.delivered_time_schedule,
        po.delivered_time,
        DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) AS date_diff,
        CASE 
            WHEN DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) > 14 THEN 'green'
            WHEN DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) > 7 AND DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) <=14 THEN 'yellow'
            WHEN DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) <=7 THEN 'red'
        END AS status,
        podc.available_document_count,
        podc.not_available_document_count,
        podc.total_document_count,
        podc.document_list
    FROM `tabPurchase Order` AS po
    LEFT JOIN (
        SELECT
            podc.parent,
            SUM(CASE WHEN podc.available = 1 THEN 1 ELSE 0 END) AS available_document_count,
            SUM(CASE WHEN podc.available = 0 THEN 1 ELSE 0 END) AS not_available_document_count,
            COUNT(*) AS total_document_count,
            CONCAT(
                '[',
                GROUP_CONCAT(
                    JSON_OBJECT(
                        'check_list_name', podc.check_list_name,
                        'available', podc.available
                    )
                    SEPARATOR ','
                ),
                ']'
            ) AS document_list
        FROM `tabPurchase Order Document Checklist` AS podc
        WHERE podc.parenttype = 'Purchase Order'
        GROUP BY podc.parent
    ) AS podc ON podc.parent = po.name
    WHERE po.docstatus = 1
    AND po.delivered_time_schedule IS NOT NULL
        AND DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) <= 30
    {po_filter}
    {search_filter}
    {status_filter}
    ORDER BY DATEDIFF(po.delivered_time_schedule, COALESCE(po.delivered_time, CURDATE())) DESC
    LIMIT {limit} OFFSET {offset}
    """.format(limit=int(limit), offset=(int(page)-1)*int(limit), po_filter=po_filter, search_filter=search_filter, status_filter=status_filter), as_dict=True)

    return {
        "data": data,
        "page": page,
        "limit": limit,
        "po_filter": po_filter,
        "search_filter": search_filter,
    }

    
    
    