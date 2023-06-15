// To enable form scripting of lead doctype
frappe.ui.form.on('Lead', {
    //Call function after save.
	refresh:function(frm) {




            {
            cur_frm.fields_dict['board_name'].get_query = function(doc) {
                return {
                    filters: {
                        "customer_group": "A3sola"
                    }
                 }
                }
            }



            //TESTT


if (!cur_frm.doc.__islocal){
    cur_frm.add_custom_button(__("Call"), function() {
        console.log("hello")
        var childTable = cur_frm.add_child("lead_tracking");
        childTable.date_and_time=frappe.datetime.nowdate()
        childTable.user=frappe.session.user_fullname
        cur_frm.refresh_fields("lead_tracking");
      

        let d = new frappe.ui.Dialog({
            title: 'Select Phone Number',
          //Add fields to fetch items
                        fields: [
              {
                label: 'Phone Numbers',
                fieldname: 'ph',
                fieldtype: 'Select',
                options: [frm.doc.number_to_be_contacted,frm.doc.whatsapp_number]

              }],
              primary_action_label: 'Confirm',


              primary_action(values) {
                frappe.call({
                    // specify the server side method to be called.
                    //dotted path to a whitelisted backend method
                    method: "a3sola_solar_management.doc_events.lead_events.call",
                    //Passing variables as arguments with request
                    args: {
                        doc:frm.doc.name,
                        num:values.ph
                    },
                  
        
                    });
              }
              
            })
            d.show();

     
        
      


    })
}


//TESTT
if (!cur_frm.doc.__islocal){
    cur_frm.add_custom_button(__("Whatsapp"), function() {
        // frappe.msgprint("Custom Information");
        var api_url="https://api.whatsapp.com/send?phone="
        var phone_number=frm.doc.whatsapp_number
        
        
        var complete_url=api_url.concat(phone_number)
        var complete_url=complete_url.concat("&text=Congratulations Mr/Mrs ",frm.doc.lead_name,`%0A%0A`,"%20%20 Thank you for expressing interest in working with ",frm.doc.company," we are excited at the prospect of working together on this project. Thank you.")
       
        window.open(complete_url, "_blank");

            //Add confirmation

    })
}











        //Add a custom button
        if (!cur_frm.doc.__islocal){
        cur_frm.add_custom_button(__("Confirm"), function() {
            // frappe.msgprint("Custom Information");

                //Add confirmation

                    //Set dialog box to fetch items
					let d = new frappe.ui.Dialog({
						title: 'Select Item',
					//Add fields to fetch items
                        fields: [
							{
								label: 'Item',
								fieldname: 'Item',
								fieldtype: 'Link',
								options: 'Product Bundle'
							},
                        // Add fields to enter quantity of items
                            {
                                label:"Quantity",
                                fieldname:"Qty",
                                fieldtype:"Int"
                            },

						],
                        // On confirming Call  server side methods
						primary_action_label: 'Confirm',
						primary_action(values) {
						console.log(values)
            // To access server side methods
		    frappe.call({
            // specify the server side method to be called.
            //dotted path to a whitelisted backend method
            method: "a3sola_solar_management.doc_events.lead_events.on_update",
            //Passing variables as arguments with request
            args: {
                doc:frm.doc.name,
                val:values.Item,
                qn:values.Qty,
                with_items:1
            },
            //Function passed as an argument to above function.
            callback: function(r) {
            //To show message


            frappe.msgprint("Opportunity Created Successfully")
                   },

            });
            d.hide();
        }
    })
     d.show();
        })
    }

   








},
district_name:function(frm) {

    

        cur_frm.fields_dict['taluk_name'].get_query = function(doc) {
            return {
                filters: {
                    "district": frm.doc.district_name
                }
             }
            }
        

},

after_save:function (frm) {


          

    frappe.call({
        // specify the server side method to be called.
        //dotted path to a whitelisted backend method
        method: "a3sola_solar_management.doc_events.lead_events.aftersavefetch",
        //Passing variables as arguments with request
        args: {
            ld:frm.doc.name,
            
        },


  })

}


});
