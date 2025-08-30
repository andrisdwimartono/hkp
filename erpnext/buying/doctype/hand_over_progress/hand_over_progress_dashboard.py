from frappe import _


def get_data():
	return {
		"fieldname": "hand_over_progress",
		"transactions": [
			{"label": _("Slip Pembayaran Subkon"), "items": ["Slip Pembayaran Subkon"]},
			{"label": _("Hand Over Progress"), "items": ["Hand Over Progress"]},
		],
	}
