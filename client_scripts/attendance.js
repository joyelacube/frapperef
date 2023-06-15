// Copyright (c) 2023, Misma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance', {
	'before_submit': function(frm) {
        if (!cur_frm.doc.__islocal){
        frappe.call({
            // specify the server side method to be called.
            //dotted path to a whitelisted backend method
            method: "a3sola_solar_management.doc_events.attendance.test",
            //Passing variables as arguments with request
            args: {
                att:frm.doc.name,
                
     
            },
            callback: function(r) {
                //To show message
                console.log(r.message)

                console.log(r.message);
                if (r.message[0] != "no" && r.message[1] != "no"){
                   
                 cur_frm.set_value('employee_in_time',r.message[0]);
                 cur_frm.set_value('employee_out_time',r.message[1]);
                 cur_frm.refresh_field('employee_in_time');
                 cur_frm.refresh_field('employee_out_time');
                 var start = frm.doc.employee_in_time.split(":");
                 var end = frm.doc.employee_out_time.split(":");
                var date1 = new Date(2000, 0, 1,  start[0], start[1]); 
                var date2 = new Date(2000, 0, 1, end[0], end[1]); 

                var diff = date2 - date1;
                var msec = diff;
                var hh = Math.floor(msec / 1000 / 60 / 60);
                msec -= hh * 1000 * 60 * 60;
                var mm = Math.floor(msec / 1000 / 60);
                msec -= mm * 1000 * 60;
                var ss = Math.floor(msec / 1000);
                msec -= ss * 1000;
                
                frm.set_value('total_hours', hh+":"+mm+":"+ss);
                frm.refresh_field('total_hours');
	 


                
               

               
    


            }
        }

	})

}
    
}});
