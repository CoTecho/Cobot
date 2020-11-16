import json
def getConf(confFile):
	fd=open(confFile,"r")
	#print(fd.read())
	configs=json.loads(fd.read())
	#print(configs)
	#fd.write(json.dumps(configs))
	fd.close()
	return configs

def writeConf(confFile,key,value):
	configs=getConf(confFile)
	fd=open(confFile,"w+")
	configs[key]=value
	fd.write(json.dumps(configs))
	fd.close()
	return configs
