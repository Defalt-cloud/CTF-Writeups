#! usr/bin/env python3
import requests


url ="http://10.10.17.235/th1s_1s_h1dd3n/?secret="

for i in range(0,100):
	response=requests.get(url+str(i))
	
	if("That is wrong!" in response.text):
		continue
	else:
		print("correct secret :",i)
		break
