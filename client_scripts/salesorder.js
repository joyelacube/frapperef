frappe.ui.form.on('Sales Order', {

    onload: function (frm) {
		var prev_route = frappe.get_prev_route();
		
		console.log("hai")
		
		if (prev_route[1] === 'Quotation') {
	
			let source_doc = frappe.model.get_doc('Quotation', prev_route[2]);
			// Set project ID
			frm.set_value("project",source_doc.project_id);
			console.log("hello")
            frm.refresh_field('project');
        }
    }
})