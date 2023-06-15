import frappe

def validate(doc,methods):

    doc.project_id=doc.project


def on_submit(doc,methods):
   
      customer=frappe.get_doc('Customer',doc.customer)
      if customer.is_installer:
            warehouse=frappe.get_doc('Warehouse',customer.warehouse)
            material_receipt=frappe.new_doc('Stock Entry')
            material_receipt.stock_entry_type='Material Receipt'
            # material_receipt.from_warehouse=doc.set_warehouse
            material_receipt.to_warehouse=customer.warehouse
            for i in doc.items:
                  item=frappe.get_doc('Item',i.item_code)
                  if item.is_stock_item:
                        material_receipt.append('items',{
                              'item_code':i.item_code,
                              'item_name':i.item_name,
                              
                              'qty':i.qty,
                        })
            if doc.packed_items:
                    for i in doc.packed_items:
                        material_receipt.append('items',{'item_code':i.item_code,'item_name':i.item_name,'qty':i.qty})
            material_receipt.save()
            material_receipt.submit()
            frappe.msgprint('Stock Entry for material transfer ' f'<a href="/app/stock-entry/{material_receipt.name}" target="blank">{material_receipt.name} </a> Created Successfully ')
           





@frappe.whitelist(allow_guest=True)
def test(doc,pro):

        project = frappe.get_doc('Project',pro)

        print(project.primary_address)
        print(project.customer)

        d={'customer':project.customer}

        # return frappe.db.sql(f"""SELECT *  FROM tabCustomer WHERE opportunity_name='CRM-OPP-2022-00002'""",as_dict=True)
        print(d)
        return d
