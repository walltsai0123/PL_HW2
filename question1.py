import urllib.request
import re
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

author = input("Input Author : ");
#author = "Ian Goodfellow"
author = author.replace(" ", "+")
start = 0
size = 50
url = "https://arxiv.org/search/?query=" + author + "&searchtype=author&size=" + str(size) + "&order=announced_date_first&start=" + str(start)
content = urllib.request.urlopen(url)
html_str = content.read().decode('utf-8')

pattern = 'of[\s\S]*?results for author: <span'
result = re.findall(pattern,html_str)
num_of_result = int(result[0].split("of ")[1].split(" results for author: <span")[0].strip())
#print(num_of_result)

pattern = 'originally announced[\s\S]*?</p>'
result = re.findall(pattern,html_str)
pattern2 = 'class=\"author[\s\S]*?</p>'
result2 = re.findall(pattern2,html_str)

year = []
freq = []
f = 0
print("[ Author: " + author + " ]")
while start < num_of_result:
	for i in range(0,len(result)):
		if result2[i].find(author.replace("+", " ")) >= 0:
			r = result[i]
			y_list = r.split();
			yr = y_list[3].strip(".")
			if yr in year:
				f += 1
			else:
				freq.append(f)
				f = 1
				year.append(yr)
	start += size
	url = "https://arxiv.org/search/?query=" + author + "&searchtype=author&size=" + str(size) + "&order=announced_date_first&start=" + str(start)
	content = urllib.request.urlopen(url)
	html_str = content.read().decode('utf-8')
	result = re.findall(pattern,html_str)
	result2 = re.findall(pattern2,html_str)
freq.append(f)
freq.pop(0)

y_pos = np.arange(len(year))
plt.bar(y_pos, freq, align='center', alpha=0.5)
plt.xticks(y_pos,year)
plt.show()
