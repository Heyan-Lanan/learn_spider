from lxml import etree
tree = etree.parse('jetbrains.html')
r = tree.xpath('/html/head/title')
print(r)
