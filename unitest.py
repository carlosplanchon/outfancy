import outfancy

m = outfancy.render.Chart()

start = -20
end = 10000
dataset = [[x, x] for x in range(start, end)]

render = m.line(dataset, 'f(x) = x²', color=True)

print(render)
print(len(render))

#inc = 100
#tot = int(len(render)/inc)
#for x in range(0,tot):
	#print(render[x*inc:(x+1)*inc])