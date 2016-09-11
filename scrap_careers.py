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

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    # Python3: sys already set to UTF-8 Encoding
    pass

NEW_XLS = 0  # To write into new file, change to '1'
TEMP = False  # Just a debug variable meant to be removed, It turns off pie-ug pie-pg and courses offered

PAGE_OFFSET = 0
ENTRY_OFFSET = 0
GLOBAL_OFFSET = 0
OUTPUT_FILE=os.path.join(os.path.dirname(__file__),"output",'data_careers_1_100.xls')
CHECKPOINT = open('checkpoint.dat', 'r+')
HEADER = ['Name', 'Type', 'Phone1', 'Phone2', 'Phone3', 'Phone4', 'Phone5', 'Logo URL', 'Also Known As', 'Location', 'Estd.', 'Website', 'Mail', 'Ownership', 'Approved By', 'Affiliated to', 'Link-Affiliated to', 'Facilities', 'State Rank', 'Facebook',
          'Twitter', 'Youtube', 'Wikipedia', 'Total Faculty', 'Ratio-Student:Faculty', 'UG Pie Chart', 'PG Pie Chart', 'Notable Alumni', 'Top Following States', 'Admission Mode', 'Gender Ratio', 'Avg. Age', 'Geometric Insights',
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
    except NoSuchElementException:
        print(xpath, "was not found!!")
        return ""
    if attrib:
        return element.get_attribute(attrib)
    return element.text


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
    # time.sleep(6)############################IF CLOUDFLARE PROBLEM or use
    # By. dynamic ele

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

        phones_nos = ''
        phone1 = ''
        phone2 = ''
        phone3 = ''
        phone4 = ''
        phone5 = ''

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

        facilities = '< '
        for x in driver.find_elements_by_xpath("//div[@class='facilitylist']//li"):
            y = x.get_attribute('innerHTML')
            facilities += y[y.find('</i>'):].replace('</i>', ' # ')
        facilities += ' >'
        print('Facilities:', facilities)

        #stu_to_fact = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/span")
        # print(stu_to_fact)##########################################format

        state_rank = ''

        state_rank = safe_get_xpath(
            "/html/body/div/div/div/div[3]/div/div/div/div[3]/div/div/div/span")
        if 'A' not in state_rank:
            state_rank = ''
        print('College Grade:', state_rank)  # PG KYUN

        #no_courses = driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div[4]/div/h4").text
        #no_courses = int(no_courses[no_courses.find(':'):].replace(':',''))
        # print(no_courses)

        facebook = driver.find_element_by_xpath(
            "/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li/a").get_attribute('href')
        if 'javascript' in str(facebook):
            facebook = ''
        print(facebook)

        twitter = driver.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li[2]/a').get_attribute('href')
        if 'javascript' in str(twitter):
            twitter = ''
        print(twitter)

        youtube = driver.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li[3]/a').get_attribute('href')
        if 'javascript' in str(youtube):
            youtube = ''
        print(youtube)

        wiki = driver.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/div/div/div[2]/ul/li[4]/a').get_attribute('href')
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

        if check_exists_by_xpath("//div[@id='chart_div_ug']") and TEMP:

            pie_temp = driver.find_element_by_xpath(
                "//div[@id='chart_div_ug']/div/div/div")
            #/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div
            #/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div/div/div/div/svg/g/g
            #/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div/div/div/div/svg/g/g/circle
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

        str_ug_pie = ''
        for x in range(len(pie_name_li)):
            str_ug_pie += '< ' + pie_name_li[x] + \
                ' : ' + pie_intake_li[x] + ' >'

        # pg_PIE
        pie2_color_li = []
        pie2_name_li = []
        pie2_intake_li = []

        if check_exists_by_xpath("//div[@id='chart_div_pg']") and TEMP:
            pie_temp = driver.find_element_by_xpath(
                "//div[@id='chart_div_pg']/div/div/div")
            #/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div
            #/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div/div/div/div/svg/g/g
            #/html/body/div/div/div/div[3]/div/div/div/div[4]/div/div[2]/div/div/div/div/div/svg/g/g/circle
            block_li = pie_temp.find_elements_by_xpath(
                ".//*[local-name() = 'svg']/*[local-name() = 'g']/*[local-name() = 'g']")
            for y in block_li:
                # print(y.get_attribute('outerHTML'))
                # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
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

        # print(pie2_color_li)
        print(pie2_name_li)
        print(pie2_intake_li)

        str_pg_pie = ''
        for x in range(len(pie2_name_li)):
            str_pg_pie += '< ' + \
                pie2_name_li[x] + ' : ' + pie2_intake_li[x] + ' >'

        # Notable alumni
        str_alumni = ''
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
                    str_alumni += '< ' + 'Photo Link : ' + alumni_img + ' # Name : ' + alumni_name + ' # Designation : ' + \
                        alumni_designation + ' # Company : ' + alumni_company + \
                        ' # LinkedIn Link : ' + alumni_linked_in + ' >'
                except NoSuchElementException:
                    continue
        print('Notable alumni : ')
        print(str_alumni)

        # admission
        str_mode = ''
        gender_ratio = ''
        avg_age = ''
        temp_mode = driver.find_elements_by_xpath(
            "//div[@id='mCSB_1_container']/table/tbody/tr")
        for x in temp_mode:
            mode_exam_name = safe_get_xpath('.//td[1]/a', parent=x)
            mode_type = safe_get_xpath('.//td[2]', parent=x)
            mode_level = safe_get_xpath('.//td[3]', parent=x)
            str_mode += '< ' + 'Exam : ' + mode_exam_name + ' # Type : ' + \
                mode_type + ' # Level : ' + mode_level + ' >'
            print(mode_exam_name + ' | ' + mode_type + ' | ' + mode_level)
            print(str_mode)

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
            avg_age = driver.find_element_by_xpath("//div[@id='block-college-college-insight-data']").find_element_by_xpath(
                ".//div[@class='countBlockRight']/div/p").get_attribute('innerHTML').replace('<span class="clearfix"></span>', ' ')
            print('Avg. Age : ')
            print(avg_age)  # FORMAT
        except NoSuchElementException:
            print('-')

        # insights_geo
        print('Insights geo : ')
        in_name_li = []
        in_color_li = []
        in_data_li = []

        if check_exists_by_xpath("//div[@id='piechartgeo']") == True:
            temp_geo = driver.find_element_by_xpath("//div[@id='piechartgeo']")
            temp_g = temp_geo.find_elements_by_xpath(
                ".//*[local-name() = 'svg']/*[local-name() = 'g']")
            temp_blocks = temp_g[0].find_elements_by_xpath(
                ".//*[local-name() = 'g']")

            for x in temp_blocks[::2]:
                in_name_li.append(x.find_element_by_xpath(
                    ".//*[local-name() = 'text']").text)
                # print(in_name_li)
                # print(x.get_attribute('innerHTML'))
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
            print(in_name_li)
            print(in_data_li)

        str_in_geo = ''
        for x in range(len(in_name_li)):
            str_in_geo += '< ' + in_name_li[x] + ' : ' + in_data_li[x] + ' >'

        # top_following_states
        str_top_states = ''
        if check_exists_by_xpath("//div[@class='college-chart-common-div']/ul") == True:
            for x in driver.find_elements_by_xpath("//div[@class='college-chart-common-div']/ul/li/div"):
                str_top_states += '< ' + x.find_element_by_xpath(
                    './/h5').text + ' : ' + x.find_element_by_xpath(".//span").text + " >"
        print(str_top_states)

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

        courses = driver.find_element_by_xpath(
            "/html/body/div/div/div/div[3]/div/div/div/div/div/div/h4").text.replace('Number of Courses Available:', '')
        print(courses)
        pg_exists = 0
        if check_exists_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/div") == True:
            tot_ug = driver.find_element_by_xpath(
                "/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/div").text.replace('UG (', '').replace(')', '')
        print('UG : ' + tot_ug)
        if check_exists_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/span") == True:
            pg_exists = 1
            tot_pg = driver.find_element_by_xpath(
                "/html/body/div/div/div/div[3]/div/div/div/div/div/div/div/div/span").text.replace('PG (', '').replace(')', '')
        print('PG : ' + tot_pg)

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
                


                #all_courses = driver.find_elements_by_xpath("/html/body/div/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[2]/div")
                
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

        while(True):

            all_courses = driver.find_elements_by_xpath(
                "/html/body/div/div/div/div[3]/div/div/div/div/div[2]/div[2]/div[2]/div")

            i = 0
            for x in range(len(all_courses) // 2):
                i += 1
                if i > 2 and not TEMP:
                    break

                print(
                    '######################################################################')
                # print(all_courses[i].find_element_by_xpath(".//a[@class='apply_btn']").get_attribute('outerHTML'))

                clink = all_courses[i].find_element_by_xpath(
                    ".//a[@class='apply_btn']").get_attribute('href')
                #clink = 'http://www.engineering.careers360.com/colleges/pes-university-bangalore/courses/m-tech-digital-electronics-and-communications-systems'
                driver.find_element_by_tag_name(
                    "body").send_keys(Keys.CONTROL + 't')
                #driver = webdriver.Firefox()
                try:
                    driver.get(clink)
                except:
                    break

                cname = safe_get_xpath(
                    "/html/body/div/div/div/div[3]/div/div/div/div/h2")
                print(cname)

                eligibility = ''
                #eligibility = driver.find_element_by_xpath("//span[@class='more-eligibility']").get_attribute('innerHTML').replace('<span class="readless-eligibility" style="color:blue; cursor:pointer;">...See Less</span>','')

                print('Eligibility : ')
                if check_exists_by_xpath("//span[@class='more-eligibility']") == True:
                    eligibility = driver.find_element_by_xpath("//span[@class='more-eligibility']").get_attribute('innerHTML').replace(
                        '<span class="readless-eligibility" style="color:blue; cursor:pointer;">...See Less</span>', '')
                elif check_exists_by_xpath("//div[@class='default-elig']") == True:
                    eligibility = driver.find_element_by_xpath(
                        "//div[@class='default-elig']").text
                print(eligibility)

                all_cdet = driver.find_elements_by_xpath(
                    "//div[@class='coursesPageLableInnerSec']")

                str_temp = ''
                for y in all_cdet:
                    str_temp += ' # ' + \
                        y.find_element_by_xpath(
                            ".//strong").text + ' : ' + y.find_element_by_xpath(".//p").text
                    print(y.find_element_by_xpath(".//strong").text + ' : ' +
                          y.find_element_by_xpath(".//p").text)  # CSV TAKE CARE

                det = ''
                if check_exists_by_xpath("//span[@class='moreCourseDetails']") == True:
                    det = driver.find_element_by_xpath("//span[@class='moreCourseDetails']").get_attribute('innerHTML').replace(
                        '<span class="readlessCourseDetails" style="color:blue; cursor:pointer;">...See Less</span>', '')
                elif check_exists_by_xpath("//div[@class='coursesPageLableDetail']") == True:
                    detail = driver.find_element_by_xpath(
                        "//div[@class='coursesPageLableDetail']")
                    print(detail.find_element_by_xpath(".//strong").text +
                          ' : ' + detail.find_element_by_xpath(".//div").text)
                    det = detail.find_element_by_xpath(".//div").text
                print(det)

                i += 1

                str_courses += ('< ' + 'Course Name : ' + cname + ' # Eligibility : ' +
                                eligibility + str_temp + ' # Details : ' + det + ' >')

                driver.find_element_by_tag_name(
                    "body").send_keys(Keys.CONTROL + 'w')
                time.sleep(0.5)
                #driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL
            if check_exists_by_xpath("//a[@title='Go to next page']") and TEMP == False:
                break
            else:
                clink_nxt_page = safe_get_xpath(
                    "//a[@title='Go to next page']", attrib='href')
                if not clink_nxt_page:
                    break

                time.sleep(0.5)
                #driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.TAB)
                driver.get(clink_nxt_page)
                print(
                    '\n!!!!!!!!!!!!!!!!!!!!!!!!NEXT!!!PAGE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')

        str_images = ''
        for x in li_images:
            str_images += '< ' + x + ' >'

        str_vids = ''
        for x in li_vids:
            str_vids += '< ' + x + ' >'

        name = name.replace(',', '$')
        typeofcoll = typeofcoll.replace(',', '$')
        also_known_as = also_known_as.replace(',', '$')
        location = location.replace(',', '$')
        ownership = ownership.replace(',', '$')
        approved_by = approved_by.replace(',', '$')
        affiliated_to_text = affiliated_to_text.replace(',', '$')
        str_alumni = str_alumni.replace(',', '$')
        avg_age = avg_age.replace(',', '$')
        courses = courses.replace(',', '$')
        str_courses = str_courses.replace(',', '$')

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
            str_top_states,
            str_mode,
            gender_ratio,
            avg_age,
            str_in_geo,
            str_images,
            str_vids,
            courses,
            tot_ug,
            tot_pg,
            str_courses

        ]
        for col, data in enumerate(entry):
            ws.write(GLOBAL_OFFSET, col, data)
            if not data:
                continue
            wid = min(len(data) * 380, 9000)
            if ws.col(col).width < wid:
                ws.col(col).width = wid
        wb.save(OUTPUT_FILE)

        driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'w')
        time.sleep(0.5)
        driver.find_element_by_tag_name(
            "body").send_keys(Keys.CONTROL + Keys.TAB)
        print('\n--------------------------------------------\n')
    count_coll += 1
print('All DONE')
driver.close()
