# translator
化学描述自动合成语言

#测试

from synthreader import text_to_xdl

s = 'Acetic acid (125 mL) was added with stirring and the mixture heated at 87 °C for 15 hours.'

xdl = text_to_xdl(s)
print(xdl)
