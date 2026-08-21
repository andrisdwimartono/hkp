frappe.ui.form.on('Laporan Monitoring RAP', {
    refresh(frm) {
        subscribeRealtime(frm);
        updateStatus(frm);
    }
});

function subscribeRealtime(frm) {
    if (frm._realtime_registered) return;

    frm._realtime_registered = true;

    frappe.realtime.on("rap_sync_progress", async (data) => {
        if (data.docname !== frm.doc.name) return;

        frm.dashboard.set_headline(
            __(
                "⏳ Updating realization in background... {0}% ({1}/{2})",
                [data.progress, data.completed, data.total]
            )
        );

        // selesai
        if (data.progress >= 100) {
            frappe.show_alert({
                message: __("Synchronization completed"),
                indicator: "green"
            });

            // reload sekali saja
            await frm.reload_doc();

            // tampilkan headline final
            frm.dashboard.set_headline(
                __("✅ Data synchronized")
            );
        }
    });
}

function updateStatus(frm) {
    let total = frm.doc.detail.length + 1;
    let completed = 0;

    if (frm.doc.is_synchronized)
        completed++;

    frm.doc.detail.forEach(d => {
        if (d.is_synchronized)
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
    setAccumulation(frm);
}

function setAccumulation(frm){
    let total_income = "<tr><td>Total Income </td><td>:</td><td><span class='text-bold'>" + fmtMoney(frm.doc.income_final_realization) + "</span></td></tr>";

    let costs_total = 0;
    for(let i = 0; i < frm.doc.detail.length; i++){
        costs_total += frm.doc.detail[i].final_realization;
    }
    let costs_total_html = "<tr><td> Total Cost</td><td>:</td><td><span class='text-bold'>" + fmtMoney(costs_total) + "</span></td></tr>";

    let prof_loss_val = frm.doc.income_final_realization - costs_total;
    let is_profit = prof_loss_val > 0;

    let profit_loss_html = "";
    if (is_profit){
        profit_loss_html = "<tr><td class='text-success'>Profit</td><td>:</td><td><span class='text-bold'>" + fmtMoney(prof_loss_val) + "</span></td></tr>";
    } else {
        profit_loss_html = "<tr><td class='text-danger'>Loss</td><td>:</td><td><span class='text-bold'>" + fmtMoney(prof_loss_val) + "</span></td></tr>";
    }

    $("div[data-fieldname='accumulation']").html("<table>" + total_income + costs_total_html + profit_loss_html + "</table>");

}

function fmtMoney(value){
    return "Rp. " + value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}