from simple_zpl2 import ZPLDocument, Code128_Barcode

# Each label is built with a ZPLDocument object
zdoc = ZPLDocument()
zdoc.add_comment("Barcode and text")
zdoc.add_field_origin(20, 20)
code128_data = 'TEST BARCODE'
bc = Code128_Barcode(code128_data, 'N', 30, 'Y')
zdoc.add_barcode(bc)
print(zdoc.zpl_text)