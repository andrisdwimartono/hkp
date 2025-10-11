from frappe import _


def get_data():
	return {
		# dashboard connect to other doctype
		"fieldname": "hand_over_progress",
		"transactions": [
			{"label": _("Slip Pembayaran Subkon"), "items": ["Slip Pembayaran Subkon"]},
			
		],
	}
# dashboard connect by name/it self
# {"label": _("Hand Over Progress"), "items": ["Hand Over Progress"]},
