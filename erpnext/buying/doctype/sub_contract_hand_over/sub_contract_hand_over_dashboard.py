from frappe import _


def get_data():
	return {
		"fieldname": "sub_contract_hand_over",
		"transactions": [
			{"label": _("Hand Over Progress"), "items": ["Hand Over Progress"]},
		],
	}
