import requests as r
from bs4 import  BeautifulSoup
import os
import urllib.parse
while True:
	try:
		form = int(input(' 1.form 2-4  2.form 3-4  3.form 5-6 \n'))
	except ValueError:
		print('pls input an integer not a float nor string')
	
subject = input('subject\n').split(',')

print('will u be using - or , for yrs')
yrs = input('enter a yr\n')
def split(yr):
	yr_list=[]
	if ','in yr:
		yr=yr.split(',')
		return yr
	elif '-'in yr:
		yr=yr.split('-')
		for i in range(int(yr[0]),int(yr[1])+1):
			yr_list.append(i)
		return yr_list
	else:
		return yr
def get_links(url,subject,form):
	yr_list=split(yrs)
	data=r.get(url)
	links_list=[]
	soup = BeautifulSoup(data.content,'html.parser')
	a = soup.find_all('a')
	for links in a:
		link = links.get('href')
		if link!=None:
			if '.pdf' in link:
				for s in subject:
					if s in link:
						for yr in yr_list:
							if str(yr) in link:
								links_list.append(link)
	return links_list
def create_files(links):
	for link in links:
		link = urllib.parse.unquote(link)
		name=link.split('/')[6]
		sub=link.split('/')[5]
		response=r.get(link)
		necta_dir=f'where u want the files to be stored (path)'
		if not os.path.exists(necta_dir):
			os.makedirs(necta_dir)
			file_path=os.path.join(necta_dir,name)
			with open(file_path,'wb') as f:
				f.write(response.content)
				print(name)
				progress_bar(response=response)
		else:
			fl_path=os.path.join(necta_dir,name)
			with open(fl_path,'wb')as f:
				f.write(response.content)
				print(name)
				progress_bar(response=response)
def progress_bar(response):
	file_size= int(response.headers.get('Content-Length'))
	print(file_size)
	chunk_size=1024 #1kb
	bytes_downloaded=0
	bar_width=50
	if file_size is None:
		pass
	else:
		for chunk in response.iter_content(chunk_size=chunk_size):
			bytes_downloaded+=len(chunk)
			progress=int(bytes_downloaded/file_size)*100
			filled_width = int(progress* bar_width / 100)
			remaining_width=progress-filled_width
			progressbar_ = "█" * filled_width + " " * remaining_width
			sys.stdout.write(f"\rProgress: [{progressbar_}] {progress:.2f}%")
			sys.stdout.flush()
		print('Download complete')
					
def download_link(form_):
	if form_==1:
		url= 'https://maktaba.tetea.org/resources/form-1-2/'
		links=get_links(url=url,subject=subject,form=form_)
		create_files(links=links)
	elif form_==2:
		url='https://maktaba.tetea.org/resources/form-3-4/'
		links=get_links(url=url,subject=subject,form=form_)
		create_files(links=links)
	elif form_==3:
		url='https://maktaba.tetea.org/resources/form-5-6/'
		links=get_links(url=url,subject=subject,form=form_)
		create_files(links=links)
if __name__=='__main__':
	download_link(form)
	
