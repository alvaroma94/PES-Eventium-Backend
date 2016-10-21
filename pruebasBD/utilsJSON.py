import json

#info es un gateway de cualquier tipo, todos los gateways tendran q implementar el metodo toTuple
def tupleToJson(info): 
	return json.dumps(info.toTuple())

#tuple es un cjt. gateway de cualquier tipo, todos los gateways tendran q implementar el metodo toTuple
def tuplesToJson(tuples):
	ret = []
	for t in tuples:
		ret.append(t.toTuple())
	return json.dumps(ret)