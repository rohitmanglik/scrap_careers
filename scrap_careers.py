#When I wrote this, only God and I understood what I was doing 
#Now, God only knows :D


from selenium import *
from selenium import webdriver
from selenium import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import csv
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

dont_print = 0 #a-0;w-1

with open('data_careers_1_100.csv','a') as mycsv:################################################'w'
#with open('/home/bitnami/aakash/data/data_careers_1-1000.csv','w') as mycsv:
#with open('/home/aakash/data/data_careers_1-1000.csv','w') as mycsv:
	c = csv.writer(mycsv, dialect='mydialect')
	if dont_print == 1:
		c.writerow(['Name','Type','Phone1','Phone2','Phone3','Phone4','Phone5','Logo URL','Also Known As','Location','Estd.','Website','Mail','Ownership','Approved By','Affiliated to','Link-Affiliated to', 'Facilities', 'State Rank', 'Facebook',
	'Twitter', 'Youtube', 'Wikipedia', 'Total Faculty', 'Ratio-Student:Faculty', 'UG Pie Chart','PG Pie Chart', 'Notable Alumni','Top Following States', 'Admission Mode', 'Gender Ratio', 'Avg. Age','Geometric Insights',
	'Images','Videos', 'Total Courses', 'Total UG','Total PG','Courses'])

	print(sys.argv)
	
	count_coll = 3#int(sys.argv[0])#0###############################################INITIAL PAGE NO.
	while count_coll <= 10:#int(sys.argv[1]):#####################################FINAL PAGE NO. - EACH PAGE 10 College

		url = 'http://www.engineering.careers360.com/colleges/list-of-engineering-colleges-in-India?page='+str(count_coll)
		print('Launch...')

		#driver = webdriver.PhantomJS()
		driver = webdriver.Firefox()
		#driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX, command_executor='http://127.0.0.1:4444/wd/hub')
		
		print('Navigate.')
		driver.get(url)
		print('Wait.....')
		#time.sleep(6)############################IF CLOUDFLARE PROBLEM or use By. dynamic ele
		count_coll += 1



		temp_count = 0
		while(temp_count == 0):
			temp_count = 1
			if check_exists_by_xpath("//a[@title='Go to next page']") == False : break
			else:
				colls_url = driver.find_elements_by_xpath("//div[@class='content-box f-right']")

				for coll in colls_url:


					name = ''
					coll_url =''
					typeofcoll = ''
					phones = ''

					name = coll.find_element_by_xpath(".//div[@class='title']/a").text
					print(name)
					
					coll_url = coll.find_element_by_xpath(".//div[@class='title']/a").get_attribute('href')
					#coll_url = 'http://www.engineering.careers360.com/cmr-institute-technology-hyderabad'
					print(coll_url)
					'''url+='/branches'
					#url.split('/')[3] = ''
					#''.join(url)
					print(url)
					print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
					driver.get(url)'''

					#if 'http://www.engineering.careers360.com/colleges/vivekananda-global-university-jaipur' in str(coll_url) or 'http://www.engineering.careers360.com/galaxy-global-educational-trust%E2%80%99s-group-institutions-faculty-engineering-and-technology-ambala' in str(coll_url) or 'http://www.engineering.careers360.com/colleges/dr-kn-modi-university-tonk' in str(coll_url) or 'http://www.engineering.careers360.com/colleges/world-college-of-technology-and-management-gurgaon' in str(coll_url) or 'http://www.engineering.careers360.com/colleges/iec-college-of-engineering-and-technology-greater-noida' in str(coll_url) : continue
					
					typeofcoll = coll.find_element_by_xpath(".//div[@class='clg-type clgAtt']").text
					if 'Type: ' in typeofcoll : 
						typeofcoll = typeofcoll.replace('Type: ','')
					else : 
						typeofcoll = ''
					print(typeofcoll)
					
					phones_nos = ''
					phone1='';phone2='';phone3='';phone4='';phone5=''

					phones = coll.find_element_by_xpath(".//div[@class='clg-contact clgAtt']").text.replace('Contact: ','')
					phone=['','','','','']
					temp_phones = phones.split(',')
					for x in range(5):
						if x < len(temp_phones):
							phone[x] = temp_phones[x]
						else: break
					print(phones)

					url = coll_url
					#url = 'http://www.engineering.careers360.com/colleges/pes-university-bangalore'
					driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
					#driver = webdriver.Firefox()
					driver.get(url)
					#time.sleep(6)

					also_known_as = ''
					if check_exists_by_xpath("//div[@class='infoQuestion']") == True:
						also_known_as = driver.find_element_by_xpath("//div[@class='infoQuestion']/span").text
					print('Also Known as : '+also_known_as)

					logo = ''
					logo = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div/div/img").get_attribute('src')
					print('logo : '+logo)

					location = ''
					location = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul/li").text
					print(location)

					estd = ''
					estd = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul/li[2]/span").text
					print(estd)

					website = ''
					website = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul/li[3]").text
					print(website)

					mail = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul/li[4]/span").text
					print(mail)

					ownership = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul[2]/li[2]/span").text
					print(ownership)

					approved_by = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul[2]/li[3]/span").text
					print(approved_by)

					affiliated_to_text = ''
					if check_exists_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul[2]/li[4]/a") == True:
						affiliated_to_text =  driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul[2]/li[4]/a").text
					print(affiliated_to_text)


					affiliated_to_link = ''
					if check_exists_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul[2]/li[4]/a") == True:
						affiliated_to_link =  driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/ul[2]/li[4]/a").get_attribute('href')
					print(affiliated_to_link)

					facilities = '< '
					for x in driver.find_elements_by_xpath("//div[@class='facilitylist']//li"):
						y =  x.get_attribute('innerHTML')
						facilities += y[y.find('</i>'):].replace('</i>',' # ')
					facilities += ' >'
					print(facilities)

					#stu_to_fact = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/span")
					#print(stu_to_fact)##########################################format

					state_rank = ''
					if check_exists_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div[3]/div/div/div/span"):
						state_rank = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div[3]/div/div/div/span").text
						if 'A' not in state_rank : state_rank = '' 
					print(state_rank)###################################################################################################################################PG KYUN

					#no_courses = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div[4]/div/h4").text
					#no_courses = int(no_courses[no_courses.find(':'):].replace(':',''))
					#print(no_courses)

					
					facebook = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li/a").get_attribute('href')
					if 'javascript' in str(facebook) : facebook = ''
					print(facebook)

					twitter = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li[2]/a').get_attribute('href')
					if 'javascript' in str(twitter) : twitter = ''
					print(twitter)

					youtube = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li[3]/a').get_attribute('href')
					if 'javascript' in str(youtube) : youtube = ''
					print(youtube)

					wiki = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li[4]/a').get_attribute('href')	
					if 'javascript' in str(wiki) : wiki = ''
					print(wiki)

					#faculty
					print('Faculty : ')
					tot_faculty = ''
					if check_exists_by_xpath("//div[@id='faculty']//h4[@class='blockSubHeading']") == True:
						tot_faculty = driver.find_element_by_xpath("//div[@id='faculty']//h4[@class='blockSubHeading']").text
						tot_faculty = tot_faculty[tot_faculty.find(':'):].replace(':','').lstrip()
					print('Total Factuly : '+tot_faculty)

					stu_to_fact = ''
					if check_exists_by_xpath("//div[@id='faculty']//div[@class='countBlockRayco']/span") == True:
						stu_to_fact = driver.find_element_by_xpath("//div[@id='faculty']//div[@class='countBlockRayco']/span").get_attribute('innerHTML').replace('<span class="paddingMiddle">:</span>',' : ')
					print('Factuly to Stud Ratio : '+stu_to_fact)#format
					#print(stu_to_fact.text)

					#ug_PIE
					pie_color_li = []; pie_name_li = []; pie_intake_li = []

					if check_exists_by_xpath("//div[@id='chart_div_ug']") == True :
						pie_temp = driver.find_element_by_xpath("//div[@id='chart_div_ug']/div/div/div")
						#/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div
						#/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div/div/div/div/svg/g/g
						#/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div/div/div/div/svg/g/g/circle
						block_li = pie_temp.find_elements_by_xpath(".//*[local-name() = 'svg']/*[local-name() = 'g']/*[local-name() = 'g']")
						for y in block_li:
							#print(y.get_attribute('outerHTML'))
							#print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
							pie_color_li.append(y.find_element_by_xpath(".//*[local-name() = 'circle']").get_attribute('fill'))
							k = y.find_elements_by_xpath(".//*[local-name() = 'text']")
							k1 = ''
							for x in k:
								k1 += x.text+' '
							pie_name_li.append(k1)
							pie_intake_li.append('')
						
						print(pie_name_li)
						print(pie_color_li)
						temp_li = pie_temp.find_elements_by_xpath(".//*[local-name() = 'svg']/*[local-name() = 'g']")
						for x in range(1,len(temp_li)-1):
							#print(pie_intake_li)
							try:
								pie_intake_li[pie_color_li.index(temp_li[x].find_element_by_xpath(".//*[local-name() = 'path']").get_attribute('fill'))] = temp_li[x].find_element_by_xpath(".//*[local-name() = 'text']").text
							except NoSuchElementException:
								continue

					#print(pie_color_li)
					print(pie_name_li)
					print(pie_intake_li)

					str_ug_pie = ''
					for x in range(len(pie_name_li)):
						str_ug_pie += '< '+pie_name_li[x] + ' : '+pie_intake_li[x] + ' >'

					#pg_PIE
					pie2_color_li = []; pie2_name_li = []; pie2_intake_li = []

					if check_exists_by_xpath("//div[@id='chart_div_pg']") == True :
						pie_temp = driver.find_element_by_xpath("//div[@id='chart_div_pg']/div/div/div")
						#/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div
						#/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div/div/div/div/svg/g/g
						#/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div/div/div/div/svg/g/g/circle
						block_li = pie_temp.find_elements_by_xpath(".//*[local-name() = 'svg']/*[local-name() = 'g']/*[local-name() = 'g']")
						for y in block_li:
							#print(y.get_attribute('outerHTML'))
							#print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
							pie2_color_li.append(y.find_element_by_xpath(".//*[local-name() = 'circle']").get_attribute('fill'))
							k = y.find_elements_by_xpath(".//*[local-name() = 'text']")
							k1 = ''
							for x in k:
								k1 += x.text+' '
							pie2_name_li.append(k1)
							pie2_intake_li.append('')
					
						temp2_li = pie_temp.find_elements_by_xpath(".//*[local-name() = 'svg']/*[local-name() = 'g']")
						for x in range(1,len(temp2_li)-1):
							try :
								pie2_intake_li[pie2_color_li.index(temp2_li[x].find_element_by_xpath(".//*[local-name() = 'path']").get_attribute('fill'))] = temp2_li[x].find_element_by_xpath(".//*[local-name() = 'text']").text
							except NoSuchElementException:
								continue

					#print(pie2_color_li)
					print(pie2_name_li)
					print(pie2_intake_li)

					str_pg_pie = ''
					for x in range(len(pie2_name_li)):
						str_pg_pie += '< '+pie2_name_li[x] + ' : '+pie2_intake_li[x] + ' >'


					#Notable alumni
					str_alumni = ''
					if check_exists_by_xpath("//div[@class='custom-slider-alumni']"):
						alumni_temp = driver.find_element_by_xpath("//div[@class='custom-slider-alumni']")
						all_alumni = alumni_temp.find_elements_by_xpath(".//div[@class='sliderPadding']")
						for x in all_alumni:
							try:
								#print(x.get_attribute('outerHTML'))
								alumni_img = x.find_element_by_xpath(".//div[@class='alumni_img']/img").get_attribute('src')
								#print(alumni_img)
								alumni_name = x.find_element_by_xpath(".//div[@class='alumni_Info']/div[1]").text
								#print(alumni_name)
								alumni_designation =  x.find_element_by_xpath(".//div[@class='alumni_Info']/div[2]").text
								#print(alumni_designation)
								alumni_company =  x.find_element_by_xpath(".//div[@class='alumni_Info']/div[3]").text
								#print(alumni_company)
								alumni_linked_in = x.find_element_by_xpath(".//div[@id='social-platforms']//a").get_attribute('href')
								#print(alumni_linked_in)
								str_alumni += '< ' + 'Photo Link : ' + alumni_img + ' # Name : ' + alumni_name + ' # Designation : ' + alumni_designation + ' # Company : ' + alumni_company + ' # LinkedIn Link : '+ alumni_linked_in + ' >'
							except NoSuchElementException:
								continue
					print('Notable alumni : ')
					print(str_alumni)


					#admission
					str_mode = ''
					gender_ratio  = '';avg_age = ''
					temp_mode = driver.find_elements_by_xpath("//div[@id='mCSB_1_container']/table/tbody/tr")
					for x in temp_mode:
						mode_exam_name = x.find_element_by_xpath('.//td[1]/a').text
						mode_type = x.find_element_by_xpath('.//td[2]').text
						mode_level = x.find_element_by_xpath('.//td[3]').text
						str_mode += '< ' +'Exam : '+mode_exam_name+' # Type : ' +mode_type+' # Level : '+mode_level+ ' >'
						print(mode_exam_name+' | ' + mode_type + ' | '+ mode_level)
						print(str_mode)

					#insights
					try:
						temp_insights = driver.find_element_by_xpath("//div[@id='block-college-college-insight-data']")
						gender_ratio = temp_insights.find_element_by_xpath(".//div[@class='countBlockLeft dividerRight']/div/span[2]").get_attribute('innerHTML').replace('<span class="paddingMiddle">:</span>',' : ')
						print('Gender Ratio : '+gender_ratio)
					except NoSuchElementException:
						print('-')
					try:
						avg_age =  driver.find_element_by_xpath("//div[@id='block-college-college-insight-data']").find_element_by_xpath(".//div[@class='countBlockRight']/div/p").get_attribute('innerHTML').replace('<span class="clearfix"></span>',' ')
						print('Avg. Age : ')
						print(avg_age)###############################################################FORMAT
					except NoSuchElementException:
						print('-')

					#insights_geo
					print('Insights geo : ')
					in_name_li = []; in_color_li = []; in_data_li = []

					if check_exists_by_xpath("//div[@id='piechartgeo']") == True:
						temp_geo = driver.find_element_by_xpath("//div[@id='piechartgeo']")
						temp_g = temp_geo.find_elements_by_xpath(".//*[local-name() = 'svg']/*[local-name() = 'g']")
						temp_blocks = temp_g[0].find_elements_by_xpath(".//*[local-name() = 'g']")

						for x in temp_blocks[::2]:
							in_name_li.append(x.find_element_by_xpath(".//*[local-name() = 'text']").text)
							#print(in_name_li)
							#print(x.get_attribute('innerHTML'))
							in_color_li.append(x.find_element_by_xpath(".//*[local-name() = 'circle']").get_attribute('fill'))
							in_data_li.append('')
						print(in_color_li)
						print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

						for x in temp_g[1:]:
							#print(x.get_attribute('innerHTML'))
							#print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
							try:
								in_data_li[in_color_li.index(x.find_element_by_xpath(".//*[local-name() = 'path']").get_attribute('fill'))] = x.find_element_by_xpath(".//*[local-name() = 'text']").text
							except NoSuchElementException:
								continue
							#print(in_data_li)
						print(in_name_li)
						print(in_data_li)

					str_in_geo = ''
					for x in range(len(in_name_li)):
						str_in_geo += '< '+in_name_li[x] + ' : '+in_data_li[x] + ' >'

					#top_following_states
					str_top_states = ''
					if check_exists_by_xpath("//div[@class='college-chart-common-div']/ul") == True:
						for x in driver.find_elements_by_xpath("//div[@class='college-chart-common-div']/ul/li/div"):
							str_top_states += '< '+x.find_element_by_xpath('.//h5').text + ' : ' + x.find_element_by_xpath(".//span").text + " >"
					print(str_top_states)


					#gallery
					print('Gallery : ')
					url = driver.find_element_by_link_text("Gallery").get_attribute('href')
					print(url)
					driver.get(url)

					gall_images = [];gall_vids = []
					li_images = [];li_vids = []

					print('\nImages : ')
					gall_images = driver.find_elements_by_xpath("//div[@id='coleges-gallery-photos']/div/a")########################################################################################
					#print(gall_images)
					for x in gall_images:
						print(x.get_attribute('data-big'))
						li_images.append(x.get_attribute('data-big'))
						#print('---------------------------------')
						#print(x.get_attribute('outerHTML'))

					print('\nVIDEOS : ')
					gall_vids = driver.find_elements_by_xpath("//div[@id='college-gallery-video']/div/a")
					for x in gall_vids:
						print(x.get_attribute('href'))
						li_vids.append(x.get_attribute('href'))

					

					#courses
					print('\nCourses : ')
					#url+='/branches'
					#url = url.replace("/colleges",'')#immutable
					url = driver.find_element_by_link_text("Courses").get_attribute('href')
					print(url)
					driver.get(url)

					courses = ''
					courses = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/h4").text.replace('Number of Courses Available:','')
					print(courses)

					tot_ug = ''
					tot_pg = ''
					pg_exists = 0
					if check_exists_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/div") == True:
						tot_ug = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/div").text.replace('UG (','').replace(')','')
					print('UG : '+tot_ug)
					if check_exists_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/span") == True:
						pg_exists = 1
						tot_pg = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/span").text.replace('PG (','').replace(')','')
					print('PG : '+tot_pg)
					'''
					#ug_pie
					if check_exists_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div[2]/div/div/div/div/div/svg/g") == True:
						count_ug = len(driver.find_elements_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div[2]/div/div/div/div/div/svg/g"))
						ug_pie_data = driver.find_elements_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div[2]/div/div/div/div/div/svg/g")
						for x in ug_pie_data:
							print(x.text)

					#pg_pie
					if check_exists_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div[3]/div/div/div/div/div/svg/g") == True:
						count_pg = len(driver.find_elements_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div[3]/div/div/div/div/div/svg/g"))
						pg_pie_data = driver.find_elements_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div[3]/div/div/div/div/div/svg/g")
						for x in pg_pie_data:
							print(x.text)
					'''


					#all_courses = driver.find_elements_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[2]/div")
					'''
					i=0
					for x in range(len(all_courses)//2):
						course_logo = all_courses[i].find_element_by_xpath(".//span[@class='accordion_course_image']/img").get_attribute('src')
						print(course_logo)
						
						i+=1
						eligibility = all_courses[i].find_element_by_xpath(".//div[@class='match-interest-eligibillity']").text
						print(eligibility)

						temp = all_courses[i].find_elements_by_xpath("div[@class='degree relDiv']")
						for x in temp:
							print(x.get_attribute('outerHTML'))
						degree = temp[0].find_element_by_xpath(".//span").text
						print(degree)

						duration = temp[1].find_element_by_xpath(".//span").text
						print(duration)

						mode = temp[2].find_element_by_xpath(".//span").text
						print(mode)
						'''


					str_courses = ''

					while(True):

						all_courses = driver.find_elements_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[2]/div")

						i=0
						for  x in range(len(all_courses)//2):
							i+=1

							print('######################################################################')
							#print(all_courses[i].find_element_by_xpath(".//a[@class='apply_btn']").get_attribute('outerHTML'))
								
							clink = all_courses[i].find_element_by_xpath(".//a[@class='apply_btn']").get_attribute('href')
							#clink = 'http://www.engineering.careers360.com/colleges/pes-university-bangalore/courses/m-tech-digital-electronics-and-communications-systems'	
							driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
							#driver = webdriver.Firefox()
							driver.get(clink)

							cname = ''
							cname = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/h2").text
							print(cname)

							eligibility = ''
							#eligibility = driver.find_element_by_xpath("//span[@class='more-eligibility']").get_attribute('innerHTML').replace('<span class="readless-eligibility" style="color:blue; cursor:pointer;">...See Less</span>','')
							
							print('Eligibility : ')
							if check_exists_by_xpath("//span[@class='more-eligibility']") == True:
								eligibility = driver.find_element_by_xpath("//span[@class='more-eligibility']").get_attribute('innerHTML').replace('<span class="readless-eligibility" style="color:blue; cursor:pointer;">...See Less</span>','').encode('utf8')
							elif check_exists_by_xpath("//div[@class='default-elig']") == True:
								eligibility = driver.find_element_by_xpath("//div[@class='default-elig']").text
							print(eligibility)

							all_cdet = driver.find_elements_by_xpath("//div[@class='coursesPageLableInnerSec']")

							str_temp = ''
							for y in all_cdet:
								str_temp += ' # '+y.find_element_by_xpath(".//strong").text+' : '+y.find_element_by_xpath(".//p").text
								print(y.find_element_by_xpath(".//strong").text+' : '+y.find_element_by_xpath(".//p").text)################CSV TAKE CARE

							det = ''
							if check_exists_by_xpath("//span[@class='moreCourseDetails']") == True:
								det = driver.find_element_by_xpath("//span[@class='moreCourseDetails']").get_attribute('innerHTML').replace('<span class="readlessCourseDetails" style="color:blue; cursor:pointer;">...See Less</span>','')
							elif check_exists_by_xpath("//div[@class='coursesPageLableDetail']") == True:
								detail = driver.find_element_by_xpath("//div[@class='coursesPageLableDetail']")
								print(detail.find_element_by_xpath(".//strong").text +' : '+detail.find_element_by_xpath(".//div").text)
								det = detail.find_element_by_xpath(".//div").text
							print(det)

							i+=1

							str_courses += ('< ' +'Course Name : ' + cname + ' # Eligibility : ' + eligibility + str_temp  +' # Details : '+det+' >').encode('utf8')
							
							driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'w')
							time.sleep(0.5)
							#driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.TAB)############################################
						if check_exists_by_xpath("//a[@title='Go to next page']") == False:break
						else:
							clink_nxt_page = driver.find_element_by_xpath("//a[@title='Go to next page']").get_attribute('href')
							time.sleep(0.5)#############################################################################################################
							#driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.TAB)
							driver.get(clink_nxt_page)
							print('\n!!!!!!!!!!!!!!!!!!!!!!!!NEXT!!!PAGE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')

					str_images = ''
					for x in li_images:
						str_images += '< '+x+' >'

					str_vids = ''
					for x in li_vids:
						str_vids += '< '+x+' >'

					name = name.replace(',','$')
					typeofcoll = typeofcoll.replace(',','$')
					also_known_as = also_known_as.replace(',','$')
					location = location.replace(',','$')
					ownership = ownership.replace(',','$')
					approved_by = approved_by.replace(',','$')
					affiliated_to_text = affiliated_to_text.replace(',','$')
					str_alumni = str_alumni.replace(',','$')
					avg_age = avg_age.replace(',','$')
					courses = courses.replace(',','$')
					str_courses = str_courses.replace(',','$')




					c.writerow([
						name.encode('utf8'),
						typeofcoll.encode('utf8'),
						phone[0].encode('utf8'),
						phone[1].encode('utf8'),
						phone[2].encode('utf8'),
						phone[3].encode('utf8'),
						phone[4].encode('utf8'),
						logo.encode('utf8'),
						also_known_as.encode('utf8'),
						location.encode('utf8'),
						estd.encode('utf8'),
						website,
						mail.encode('utf8'),
						ownership.encode('utf8'),
						approved_by.encode('utf8'),
						affiliated_to_text.encode('utf8'),
						affiliated_to_link.encode('utf8'),
						facilities.encode('utf8'),
						state_rank.encode('utf8'),
						facebook.encode('utf8'),
						twitter.encode('utf8'),
						youtube.encode('utf8'),
						wiki.encode('utf8'),
						tot_faculty.encode('utf8'),
						stu_to_fact.encode('utf8'),
						str_ug_pie.encode('utf8'),
						str_pg_pie.encode('utf8'),
						str_alumni.encode('utf8'),
						str_top_states.encode('utf8'),
						str_mode.encode('utf8'),
						gender_ratio.encode('utf8'),
						avg_age.encode('utf8'),
						str_in_geo.encode('utf8'),
						str_images.encode('utf8'),
						str_vids.encode('utf8'),
						courses.encode('utf8'),
						tot_ug.encode('utf8'),
						tot_pg.encode('utf8'),
						str_courses.encode('utf8')
					
					 ])
						
					
				#http://www.engineering.careers360.com/vit-university-vellore/branches
				#http://www.engineering.careers360.com/colleges/list-of-engineering-colleges-in-India/branches

					driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'w')
					time.sleep(0.5)
					driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.TAB)


					


					



					print('\n--------------------------------------------\n')
		#/html/body/div/div/div[3]/div/div/ol/li/div[3]/div/a
		#/html/body/div/div/div[3]/div/div/ol/li[2]/div[3]/div/a
		print('All DONE')
		driver.close()
