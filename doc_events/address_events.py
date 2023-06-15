import frappe
def validate(doc,methods):
    print("hellooo")
    if doc.links:
        for lin in doc.links:
            if lin.link_doctype=="Lead":
                print("haiiiiiiiiiiiiiiiii")
                leadexist=frappe.db.exists("Lead",lin.link_name)
                if leadexist:
                    print("Enddddddddddddddddddd")
                    lead=frappe.get_doc("Lead",lin.link_name)
                    print(lead)
                    addr=str(doc.address_title)
                    add=(addr.strip())
                    # addr=addr.replace(' ','')
                    s1=add+"-"+str(doc.address_type)
                    lead.address_link=(s1.strip())
                    lead.save()
           
          