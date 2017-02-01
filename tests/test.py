import lxml.etree as etree

x = etree.parse("filename")
print etree.tostring(x, pretty_print = True)



