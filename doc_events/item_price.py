import frappe


def validate(doc,methods):
  
    if doc.selling==1:

        item=frappe.get_doc("Item",doc.item_code)
        item.standard_rate=doc.price_list_rate
        item.save()
    
