// Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Task Import", {
	refresh: function(frm) {
		subscribeRealtime(frm);
		updateStatus(frm);
	}
});

function subscribeRealtime(frm) {
    if (frm._realtime_registered) return;

    frm._realtime_registered = true;

    frm.dashboard.clear_headline();
    frappe.realtime.on("task_sync_progress", async (data) => {
        if (data.docname !== frm.doc.name) return;

        frm.dashboard.clear_headline();
        frm.dashboard.set_headline(
            __(
                "⏳ Updating task in background... {0}% ({1}/{2})",
                [data.progress, data.completed, data.total]
            )
        );

        // selesai
        if (data.progress >= 100) {
            frappe.show_alert({
                message: __("Task synchronized"),
                indicator: "green"
            });

            // reload sekali saja
            await frm.reload_doc();

            // tampilkan headline final
            frm.dashboard.clear_headline();
            frm.dashboard.set_headline(
                __("✅ Data synchronized")
            );
        }
    });
}

function updateStatus(frm) {
    let total = frm.doc.detail.length;
    let completed = 0;

    frm.doc.detail.forEach(d => {
        if (d.task)
            completed++;
    });

	frm.dashboard.clear_headline();
    if (completed < total) {
        const progress = Math.round((completed / total) * 100);

        frm.dashboard.set_headline(
            __(
                "⏳ Updating realization in background... {0}% ({1}/{2})",
                [progress, completed, total]
            )
        );
    } else {
        frm.dashboard.set_headline(
            __("✅ Data synchronized")
        );
    }
}
