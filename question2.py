import urllib.request
import re

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

pattern = 'searchtype=author&amp;query[\s\S]*?</a>'
result = re.findall(pattern,html_str)

co_author = []
co_low = []
time = []
print("[ Author: " + author + " ]")
while start < num_of_result:
	for r in result:
		name = re.search(">[\s\S]*?<",r).group().strip("><")
		while name.startswith(" "):
			name = name[1:len(name)]
		if name.lower() in co_low:
			i = co_low.index(name.lower())
			time[i] += 1
		else:
			co_author.append(name)
			co_low.append(name.lower())
			time.append(1)
	start += size
	url = "https://arxiv.org/search/?query=" + author + "&searchtype=author&size=" + str(size) + "&order=announced_date_first&start=" + str(start)
	content = urllib.request.urlopen(url)
	html_str = content.read().decode('utf-8')
	result = re.findall(pattern,html_str)
co_author.sort()
for r in co_author:
	if r.lower() != author.replace("+", " ").lower():
		i = co_low.index(r.lower())
		print(r + ": " + str(time[i]) + " times")
