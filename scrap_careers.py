# When I wrote this, only God and I understood what I was doing
# Now, God only knows :D

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
import xlwt
from xlutils.copy import copy
from xlrd import open_workbook
import sys
import os
from phpserialize import serialize


NEW_XLS = 1  # To write into new file, change to '1'


PAGE_OFFSET = 0
ENTRY_OFFSET = 0
GLOBAL_OFFSET = 0
OUTPUT_FILE=os.path.join(os.path.dirname(__file__),"output",'data_careers_1_100.xls')
CHECKPOINT = open('checkpoint.dat', 'r+')
HEADER = ['Name', 'Type', 'Phone1', 'Phone2', 'Phone3', 'Phone4', 'Phone5', 'Logo URL', 'Also Known As', 'Location', 'Estd.', 'Website', 'Mail', 'Ownership', 'Approved By', 'Affiliated to', 'Link-Affiliated to', 'Facilities', 'State Rank', 'Facebook',
          'Twitter', 'Youtube', 'Wikipedia', 'Total Faculty', 'Ratio-Student:Faculty', 'UG Pie Chart', 'PG Pie Chart', 'Notable Alumni', 'Top Following State#1', 'Top Following State#2', 'Admission Mode (Exam, Type, Mode)', 'Gender Ratio', 'Avg. Age Male',
          'Avg. Age Female', 'GeoInsights North', 'GeoInsights East', 'GeoInsights South', 'GeoInsights West', 'GeoInsights Central', 'GeoInsights NorthEast',
          'Images', 'Videos', 'Total Courses', 'Total UG', 'Total PG', 'Courses']


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def safe_get_xpath(xpath, attrib=None, parent=None):
    try:
        if parent:
            element = parent.find_element_by_xpath(xpath)
        else:
            element = driver.find_element_by_xpath(xpath)
        if attrib:
            return element.get_attribute(attrib)
        else:
            return element.text
    except:
        print(xpath, "was not found!!")
        return ""
    
    


def newCheckPoint(pages, entry_no):
    global GLOBAL_OFFSET
    global CHECKPOINT
    CHECKPOINT.seek(0)
    CHECKPOINT.truncate()
    CHECKPOINT.write(str(pages) + "\n")
    CHECKPOINT.write(str(entry_no) + "\n")
    CHECKPOINT.write(str(GLOBAL_OFFSET) + "\n")
    GLOBAL_OFFSET += 1
    CHECKPOINT.flush()


if NEW_XLS:

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Career Data')
    ulstyle = xlwt.easyxf('font: underline single')
    for col, head in enumerate(HEADER):
        ws.write(0, col, head, ulstyle)
        ws.col(col).width = min(len(head) * 380, 6000)

else:
    PAGE_OFFSET, ENTRY_OFFSET, GLOBAL_OFFSET = map(int, CHECKPOINT.readlines())

    wb = copy(open_workbook(OUTPUT_FILE))
    ws = wb.get_sheet(0)
    print("Found", GLOBAL_OFFSET, "entries completed")
    print("Resuming from page ", PAGE_OFFSET, "and entry no.:", ENTRY_OFFSET)


if len(sys.argv) > 1:
    init_page = sys.argv[0]  # INITIAL PAGE NO.
    count_coll = sys.argv[1]  # FINAL PAGE NO. - EACH PAGE 10 College

flag = True  # indicates zero loops
print('Launch...')
driver = webdriver.Firefox()
print('Navigate.')

count_coll = PAGE_OFFSET
while count_coll <= 10:

    url = 'http://www.engineering.careers360.com/colleges/list-of-engineering-colleges-in-India?page=' + \
        str(count_coll)

    #driver = webdriver.PhantomJS()
    #driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX, command_executor='http://127.0.0.1:4444/wd/hub')

    driver.get(url)
    print('Wait new URL: ....', url[40:])
    if flag:
        time.sleep(6)  # DDOS protection requires 5 sec. sleep for first get
        flag = False


    colls_url = driver.find_elements_by_xpath(
        "//div[@class='content-box f-right']")

    for entry_no, coll in enumerate(colls_url[ENTRY_OFFSET:]):

        newCheckPoint(count_coll, ENTRY_OFFSET + entry_no)

        # Create new Checkpoint, Processing resumes from this offset, if the
        # program breaks
        name = ''
        coll_url = ''
        typeofcoll = ''
        phones = ''

        title = coll.find_element_by_xpath(".//div[@class='title']/a")
        name = title.text
        print(name)

        coll_url = title.get_attribute('href')
        #coll_url = 'http://www.engineering.careers360.com/cmr-institute-technology-hyderabad'
        print(coll_url)

        typeofcoll = coll.find_element_by_xpath(
            ".//div[@class='clg-type clgAtt']").text
        if 'Type: ' in typeofcoll:
            typeofcoll = typeofcoll.replace('Type: ', '')
        else:
            typeofcoll = ''
        print(typeofcoll)


        phones = coll.find_element_by_xpath(
            ".//div[@class='clg-contact clgAtt']").text.replace('Contact: ', '') + ",,,,,"
        phone = phones.split(',')[:5]
        print(phones)

        '''url+='/branches'
                #url.split('/')[3] = ''
                #''.join(url)
                print(url)
                print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                driver.get(url)'''

        driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
        #driver = webdriver.Firefox()
        driver.get(coll_url)
        # time.sleep(6)

        also_known_as = safe_get_xpath("//div[@class='infoQuestion']/span")
        print('Also Known as : ' + also_known_as)

        logo = ''
        logo = driver.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div/div/div/div/img").get_attribute('src')
        print('logo : ' + logo)

        info = driver.find_elements_by_xpath(
            "//ul[@class='clg-info']/li") + ['', '', '', '', '', '', '', '']

        location = ''
        location = info[0].text
        print('location: ' + location)

        estd = safe_get_xpath(".//span", parent=info[1])
        print('Estd:', estd)

        website = ''
        website = info[2].text
        print('Website:', website)

        mail = safe_get_xpath(".//span", parent=info[3])
        print('Email:', mail)

        ownership = safe_get_xpath(".//span", parent=info[5])
        print('Ownership:', ownership)

        approved_by = safe_get_xpath(".//span", parent=info[6])
        print("Approved by:", approved_by)

        affiliated_to_text = safe_get_xpath(".//a", parent=info[7])
        print("Affiliated to:", affiliated_to_text)

        affiliated_to_link = safe_get_xpath(
            ".//a", attrib='href', parent=info[7])
        print("Affilited to Link:", affiliated_to_link)

        facilities_list = []
        for x in driver.find_elements_by_xpath("//div[@class='facilitylist']//li"):
            y = x.get_attribute('innerHTML')
            facilities_list.append( y[y.find('</i>')+4:])
        
        print('Facilities:', facilities_list)

        state_rank = ''

        state_rank = safe_get_xpath(
            "/html/body/div/div/div/div[3]/div/div/div/div[3]/div/div/div/span")
        if 'A' not in state_rank:
            state_rank = ''
        print('College Grade:', state_rank)

        #no_courses = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div[4]/div/h4").text
        #no_courses = int(no_courses[no_courses.find(':'):].replace(':',''))
        # print(no_courses)

        facebook = safe_get_xpath(
            "/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li/a",attrib='href')
        if 'javascript' in str(facebook):
            facebook = ''
        print(facebook)

        twitter = safe_get_xpath(
            '/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li[2]/a',attrib='href')
        if 'javascript' in str(twitter):
            twitter = ''
        print(twitter)

        youtube = safe_get_xpath(
            '/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li[3]/a',attrib='href')
        if 'javascript' in str(youtube):
            youtube = ''
        print(youtube)

        wiki = safe_get_xpath(
            '/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li[4]/a',attrib='href')
        if 'javascript' in str(wiki):
            wiki = ''
        print(wiki)

        # faculty
        print('Faculty : ')
        tot_faculty = safe_get_xpath(
            "//div[@id='faculty']//h4[@class='blockSubHeading']")
        tot_faculty = tot_faculty[
            tot_faculty.find(':'):].replace(':', '').lstrip()
        print('Total Factuly :', tot_faculty)

        stu_to_fact = ''

        stu_to_fact = safe_get_xpath("//div[@id='faculty']//div[@class='countBlockRayco']/span",
                                     attrib='innerHTML').replace('<span class="paddingMiddle">:</span>', ' : ')
        print('Factuly to Stud Ratio : ' + stu_to_fact)  # format
        # print(stu_to_fact.text)

        # ug_PIE
        pie_color_li = []
        pie_name_li = []
        pie_intake_li = []


        # Notable alumni
        str_alumni = ''
        alumni_list=[]
        if check_exists_by_xpath("//div[@class='custom-slider-alumni']"):
            alumni_temp = driver.find_element_by_xpath(
                "//div[@class='custom-slider-alumni']")
            all_alumni = alumni_temp.find_elements_by_xpath(
                ".//div[@class='sliderPadding']")
            for x in all_alumni:
                try:
                    # print(x.get_attribute('outerHTML'))
                    alumni_img = x.find_element_by_xpath(
                        ".//div[@class='alumni_img']/img").get_attribute('src')
                    # print(alumni_img)
                    alumni_name = x.find_element_by_xpath(
                        ".//div[@class='alumni_Info']/div[1]").text
                    # print(alumni_name)
                    alumni_designation = x.find_element_by_xpath(
                        ".//div[@class='alumni_Info']/div[2]").text
                    # print(alumni_designation)
                    alumni_company = x.find_element_by_xpath(
                        ".//div[@class='alumni_Info']/div[3]").text
                    # print(alumni_company)
                    alumni_linked_in = x.find_element_by_xpath(
                        ".//div[@id='social-platforms']//a").get_attribute('href')
                    # print(alumni_linked_in)
                    alumni_list.append({'photo' : alumni_img , 'name' : alumni_name , 'designation' : alumni_designation , 'company' : alumni_company ,'linkedin' : alumni_linked_in })
                except NoSuchElementException:
                    continue
        str_alumni = serialize(alumni_list).decode('utf8')
        print('Notable alumni : ')


        # admission
        admis_mode = []
        gender_ratio = ''
        avg_age = ''
        temp_mode = driver.find_elements_by_xpath(
            "//div[@id='mCSB_1_container']/table/tbody/tr")
        for x in temp_mode:
            mode_exam_name = safe_get_xpath('.//td[1]/a', parent=x)
            mode_type = safe_get_xpath('.//td[2]', parent=x)
            mode_level = safe_get_xpath('.//td[3]', parent=x)
            admis_mode.append( {'exam_name':mode_exam_name ,'exam_type' : mode_type ,'exam_level' : mode_level})
            
        str_mode=serialize(admis_mode).decode('utf8')

        # insights
        try:
            temp_insights = driver.find_element_by_xpath(
                "//div[@id='block-college-college-insight-data']")
            gender_ratio = temp_insights.find_element_by_xpath(".//div[@class='countBlockLeft dividerRight']/div/span[2]").get_attribute(
                'innerHTML').replace('<span class="paddingMiddle">:</span>', ' : ')
            print('Gender Ratio : ' + gender_ratio)
        except NoSuchElementException:
            print('-')
        try:
            t = driver.find_element_by_xpath("//div[@id='block-college-college-insight-data']").find_element_by_xpath(
                ".//div[@class='countBlockRight']/div/p").get_attribute('innerHTML').replace('<span class="clearfix"></span>', ' ').split('=')
            avg_ageM,avg_ageF=t[1][1:3],t[2][1:3]
            print('Avg. Age : M,F')
            print(avg_ageM,avg_ageF)
        except NoSuchElementException:
            print('-')

        # insights_geo
        print('Insights geo : ')
        in_name_li = []
        in_color_li = []
        in_data_li = []
        skip=False
        if check_exists_by_xpath("//div[@id='piechartgeo']"):
            try:
                driver.implicitly_wait(0.5)
                temp_geo = driver.find_element_by_xpath("//div[@id='piechartgeo']")
                temp_g = temp_geo.find_elements_by_xpath(
                    ".//*[local-name() = 'svg']/*[local-name() = 'g']")
                temp_blocks = temp_g[0].find_elements_by_xpath(
                    ".//*[local-name() = 'g']")
            except:
                skip=True
            driver.implicitly_wait(0)
            if not skip:
                for x in temp_blocks[::2]:
                    in_name_li.append(x.find_element_by_xpath(
                        ".//*[local-name() = 'text']").text)                
                    in_color_li.append(x.find_element_by_xpath(
                        ".//*[local-name() = 'circle']").get_attribute('fill'))
                    in_data_li.append('')
                print(in_color_li)
                print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

                for x in temp_g[1:]:
                    # print(x.get_attribute('innerHTML'))
                    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    try:
                        in_data_li[in_color_li.index(x.find_element_by_xpath(".//*[local-name() = 'path']").get_attribute(
                            'fill'))] = x.find_element_by_xpath(".//*[local-name() = 'text']").text
                    except NoSuchElementException:
                        continue
                    # print(in_data_li)
                print("name",in_name_li)
                print("data",in_data_li)

##        str_in_geo = ''
##        for x in range(len(in_name_li)):
##            str_in_geo += '< ' + in_name_li[x] + ' : ' + in_data_li[x] + ' >'

        # top_following_states
        top_states = []
        if check_exists_by_xpath("//div[@class='college-chart-common-div']/ul"):
            for x in driver.find_elements_by_xpath("//div[@class='college-chart-common-div']/ul/li/div"):
                top_states.append(serialize({ safe_get_xpath(
                    './/h5',parent=x) : safe_get_xpath(".//span",parent=x) }).decode('utf8'))
        print(top_states)

        # gallery
        print('Gallery : ')
        url = driver.find_element_by_link_text("Gallery").get_attribute('href')
        print(url)
        driver.get(url)

        gall_images = []
        gall_vids = []
        li_images = []
        li_vids = []

        print('\nImages : ')
        gall_images = driver.find_elements_by_xpath(
            "//div[@id='coleges-gallery-photos']/div/a")
        # print(gall_images)
        for x in gall_images:
            print(x.get_attribute('data-big'))
            li_images.append(x.get_attribute('data-big'))
            # print('---------------------------------')
            # print(x.get_attribute('outerHTML'))

        print('\nVIDEOS : ')
        gall_vids = driver.find_elements_by_xpath(
            "//div[@id='college-gallery-video']/div/a")
        for x in gall_vids:
            print(x.get_attribute('href'))
            li_vids.append(x.get_attribute('href'))

        # courses
        courses = ''
        tot_ug = ''
        tot_pg = ''
        str_courses = ''

        print('\nCourses : ')
        # url+='/branches'
        # url = url.replace("/colleges",'')#immutable
        try:
            url = driver.find_element_by_link_text(
                "Courses").get_attribute('href')
            print(url)
            driver.get(url)
        except:
            continue

        courses = safe_get_xpath(
            "/html/body/div/div/div/div[3]/div/div/div/div/div/div/h4").replace('Number of Courses Available:', '')
        print(courses)
        pg_exists = 0
        if check_exists_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/div"):
            tot_ug = driver.find_element_by_xpath(
                "/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/div").text.replace('UG (', '').replace(')', '')
        print('UG : ' + tot_ug)
        if check_exists_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/span"):
            pg_exists = 1
            tot_pg = driver.find_element_by_xpath(
                "/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/span").text.replace('PG (', '').replace(')', '')
        print('PG : ' + tot_pg)

        courses_list=[]
        while(True):

            all_courses = driver.find_elements_by_xpath(
                "/html/body/div/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[2]/div")

            
            for x in all_courses[1::2]:
                

                print(
                    '######################################################################')
                # print(all_courses[i].find_element_by_xpath(".//a[@class='apply_btn']").get_attribute('outerHTML'))

                clink = safe_get_xpath(
                    ".//a[@class='apply_btn']", parent = x , attrib='href')
                #clink = 'http://www.engineering.careers360.com/colleges/pes-university-bangalore/courses/m-tech-digital-electronics-and-communications-systems'
                if not clink:
                    continue
                driver.find_element_by_tag_name(
                    "body").send_keys(Keys.CONTROL + 't')
                #driver = webdriver.Firefox()
                try:
                    driver.get(clink)
                except:
                    continue

                course_dict = dict()
                course_dict['cname'] = safe_get_xpath(
                    "/html/body/div/div/div/div[3]/div/div/div/div/h2")
                if not course_dict['cname']:
                    continue

                eligibility = ''
                #eligibility = driver.find_element_by_xpath("//span[@class='more-eligibility']").get_attribute('innerHTML').replace('<span class="readless-eligibility" style="color:blue; cursor:pointer;">...See Less</span>','')

                print('Eligibility : ')
                
                eligibility = safe_get_xpath("//span[@class='more-eligibility']",attrib='innerHTML').replace(
                        '<span class="readless-eligibility" style="color:blue; cursor:pointer;">...See Less</span>', '')
                if not eligibility:
                    eligibility = safe_get_xpath(
                        "//div[@class='default-elig']")
                    
                course_dict['eligibility']=eligibility
                print(eligibility)

                all_cdet = driver.find_elements_by_xpath(
                    "//div[@class='coursesPageLableInnerSec']")

                
                for y in all_cdet:
                    course_dict[safe_get_xpath(".//strong",parent=y).lower()] =  safe_get_xpath(".//p",parent=y)
                    
                
                det = safe_get_xpath("//span[@class='moreCourseDetails']",attrib='innerHTML').replace(
                        '<span class="readlessCourseDetails" style="color:blue; cursor:pointer;">...See Less</span>', '')
                if check_exists_by_xpath("//div[@class='coursesPageLableDetail']") == True and not det:
                    detail = driver.find_element_by_xpath(
                        "//div[@class='coursesPageLableDetail']")
                    
                    det = safe_get_xpath(".//div",parent=detail)
                course_dict['details']=det
                print(det)

                

                courses_list.append(serialize(course_dict).decode('utf8'))

                driver.find_element_by_tag_name(
                    "body").send_keys(Keys.CONTROL + 'w')
                time.sleep(0.3)
                
                
                

            
            clink_nxt_page = safe_get_xpath(
                "//a[@title='Go to next page']", attrib='href')
            if not clink_nxt_page:
                break

            time.sleep(0.3)

            driver.get(clink_nxt_page)
            
            print(
                '\n!!!!!!!!!!!!!!!!!!!!!!!!NEXT!!!PAGE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        
        skip=False
        
        if check_exists_by_xpath("//div[@id='chart_div_ug']"):
            try:
                driver.implicitly_wait(2)
                pie_temp = driver.find_element_by_xpath(
                "//div[@id='chart_div_ug']/div/div/div")
                
            except:
                print("pie ug not found")
                skip=True
            driver.implicitly_wait(0)    
            if not skip:
                block_li = pie_temp.find_elements_by_xpath(
                    ".//*[local-name() = 'svg']/*[local-name() = 'g']/*[local-name() = 'g']")
                for y in block_li:
                    # print(y.get_attribute('outerHTML'))
                    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    pie_color_li.append(y.find_element_by_xpath(
                        ".//*[local-name() = 'circle']").get_attribute('fill'))
                    k = y.find_elements_by_xpath(".//*[local-name() = 'text']")
                    k1 = ''
                    for x in k:
                        k1 += x.text + ' '
                    pie_name_li.append(k1)
                    pie_intake_li.append('')

                print(pie_name_li)
                print(pie_color_li)
                temp_li = pie_temp.find_elements_by_xpath(
                    ".//*[local-name() = 'svg']/*[local-name() = 'g']")
                for x in range(1, len(temp_li) - 1):
                    # print(pie_intake_li)
                    try:
                        pie_intake_li[pie_color_li.index(temp_li[x].find_element_by_xpath(
                            ".//*[local-name() = 'path']").get_attribute('fill'))] = temp_li[x].find_element_by_xpath(".//*[local-name() = 'text']").text
                    except NoSuchElementException:
                        continue

        # print(pie_color_li)
        print(pie_name_li)
        print(pie_intake_li)

        str_ug_pie = serialize(dict(zip(pie_name_li,pie_intake_li))).decode('utf8')

        # pg_PIE
        pie2_color_li = []
        pie2_name_li = []
        pie2_intake_li = []
        skip = False
        if check_exists_by_xpath("//div[@id='chart_div_pg']"):
            try:
                driver.implicitly_wait(2)
                pie_temp = driver.find_element_by_xpath(
                "//div[@id='chart_div_pg']/div/div/div")
            except:
                skip=True
                
            driver.implicitly_wait(0)    
            
            if not skip:
                block_li = pie_temp.find_elements_by_xpath(
                    ".//*[local-name() = 'svg']/*[local-name() = 'g']/*[local-name() = 'g']")
                for y in block_li:
                    pie2_color_li.append(y.find_element_by_xpath(
                        ".//*[local-name() = 'circle']").get_attribute('fill'))
                    k = y.find_elements_by_xpath(".//*[local-name() = 'text']")
                    k1 = ''
                    for x in k:
                        k1 += x.text + ' '
                    pie2_name_li.append(k1)
                    pie2_intake_li.append('')

                temp2_li = pie_temp.find_elements_by_xpath(
                    ".//*[local-name() = 'svg']/*[local-name() = 'g']")
                for x in range(1, len(temp2_li) - 1):
                    try:
                        pie2_intake_li[pie2_color_li.index(temp2_li[x].find_element_by_xpath(
                            ".//*[local-name() = 'path']").get_attribute('fill'))] = temp2_li[x].find_element_by_xpath(".//*[local-name() = 'text']").text
                    except NoSuchElementException:
                        continue

        
        print(pie2_name_li)
        print(pie2_intake_li)

        str_pg_pie = serialize(dict(zip(pie2_name_li,pie2_intake_li))).decode('utf8')
        
        
        
        str_images = str(li_images)[1:-1].replace("'","")

        str_vids = str(li_vids)[1:-1].replace("'","")
        
        facilities = str(facilities_list)[1:-1].replace("'","")

        name = name.replace(',', '$')
        typeofcoll = typeofcoll.replace(',', '$')
        also_known_as = also_known_as.replace(',', '$')
        location = location.replace(',', '$')
        ownership = ownership.replace(',', '$')
        approved_by = approved_by.replace(',', '$')
        affiliated_to_text = affiliated_to_text.replace(',', '$')
        
        
        
        

        entry = [
            name,
            typeofcoll,
            phone[0],
            phone[1],
            phone[2],
            phone[3],
            phone[4],
            logo,
            also_known_as,
            location,
            estd,
            website,
            mail,
            ownership,
            approved_by,
            affiliated_to_text,
            affiliated_to_link,
            facilities,
            state_rank,
            facebook,
            twitter,
            youtube,
            wiki,
            tot_faculty,
            stu_to_fact,
            str_ug_pie,
            str_pg_pie,
            str_alumni,
            top_states[0],
            top_states[1],
            str_mode,
            gender_ratio,
            avg_ageM,
            avg_ageF,
            in_data_li[0],
            in_data_li[1],
            in_data_li[2],
            in_data_li[3],
            in_data_li[4],
            in_data_li[5],
            str_images,
            str_vids,
            courses,
            tot_ug,
            tot_pg,

        ]
        for col, data in enumerate(entry):
            ws.write(GLOBAL_OFFSET, col, data)
            if not data:
                continue
            wid = min(len(data) * 380, 12000)
            if ws.col(col).width < wid:
                ws.col(col).width = wid
        course_offset=len(entry)
        for col,data in enumerate(courses_list):
            ws.write(GLOBAL_OFFSET, col+course_offset, data)
            ws.col(col).width = 20000
            wb.save(OUTPUT_FILE)
        wb.save(OUTPUT_FILE)

        driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'w')
        time.sleep(0.2)
        driver.find_element_by_tag_name(
            "body").send_keys(Keys.CONTROL + Keys.TAB)
        print('\n--------------------------------------------\n')
    count_coll += 1
print('All DONE')
driver.close()
