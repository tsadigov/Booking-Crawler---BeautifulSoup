# import itertools
import requests
import math
import time
import random
import string
import re
from bs4 import BeautifulSoup
from xlwt import Workbook

""" Column name lists in sheets """
col_name_list_hotel = ['ID','NAME','STAR','INFO_LINK','COORDITANES','IMAGE_LINK','REC_PRICE','RATE','ADDRESS','DESCRIPTION','JOINED_DATE','PROPERTY_TYPE']
col_name_list_review = ['ID','NAME','COUNTRY','RATE','DATE','TITLE','P_REVIEW','N_REVIEW','HOTEL_ID']
col_name_room_details = ['ID','SLEEPS','ROOM_TYPE','BED_TYPE','SIZE','HOTEL_ID']
#Review sheet row number
review_row_num = 1
room_row_num = 1

def check_empty(value):
    if value:
        return value.text.strip()
    else:
        return ""

def r_check_empty(value):
    if value:
        if len(value.text.split("·")) > 1:
            return value.text.split("·")[1].strip()
        return value.text.strip()
    else:
        return ""

def str_to_int(number):
    number = number.split(",")
    num = ""
    for n in number:
        num += n
    return int(num)

def request_url(url):
    """ Header of request """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',} # To handle OVERLOAD
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r

def create_sheet(workbook,sheet_name,col_name_list):
    """ Creating new sheet with given column names """
    sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)

    for column_name in col_name_list:
        col_index = col_name_list.index(column_name)
        sheet.col(col_index).width = 5000
        sheet.write(0,col_index,column_name)
    return sheet

def insert_sheet(sheet,row_num,data_list):
    col_index = 0
    for column_value in data_list:
        sheet.write(row_num,col_index,column_value)
        col_index += 1

def get_prop_num(url):

    r = request_url(url)
    soup = BeautifulSoup(r.content,'html5lib')

    '''
    Find property count in the first page for pagination purposes
    '''
    header = soup.find("div",attrs={"class":"sr_header"})

    head = header.find("h1")
    prop = head.text.split(" ")[1]

    return int(str_to_int(prop))

'''Create Workbook'''
wb = Workbook()
'''Add sheet'''
sheet1 = create_sheet(wb,"Hotels",col_name_list_hotel)
sheet2 = create_sheet(wb,"Reviews",col_name_list_review)
sheet3 = create_sheet(wb,"Rooms",col_name_room_details)

def scrape_hotel_reviews(page_name,review_count,hotel_id):
    '''Scrape Hotel Reviews'''
    global review_row_num
    print("page_name->",page_name," review->",review_count)
    # r_count = 0

    for p in range(0, math.ceil(review_count/10)):
        time.sleep(random.randint(0,1))
        urls = "https://www.booking.com/reviewlist.html?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaBGIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Aobe6e8FwAIB;cc1=az;dist=1;pagename="+page_name+";srpvid=7f8e530322ea0011;type=total&;offset="+str(p*10)+";rows=10"
        req = request_url(urls)
        soup = BeautifulSoup(req.content,'html5lib')

        blocks = soup.findAll("li",attrs={"class":"review_list_new_item_block"})

        for b in blocks:
            name = b.find("span",attrs={"class":"bui-avatar-block__title"})
            country = check_empty(b.find("span",attrs={"class":"bui-avatar-block__subtitle"}))
            rate = check_empty(b.find("div",attrs={"class":"c-guest-with-score__score"}))
            date = b.find("span",attrs={"class":"c-review-block__date"}).text.split(":")[1].strip()

            r_title = check_empty(b.find("h3",attrs={"class":"c-review-block__title"}))
            r_pos = r_check_empty(b.find("div",attrs={"class":"c-review__row"}))
            r_neg = r_check_empty(b.find("div",attrs={"class":"c-review__row lalala"}))

            # print(name.text,r_pos)
            review_list = [str(review_row_num),name.text,country,rate,date,r_title,r_pos,r_neg,hotel_id]
            insert_sheet(sheet2,review_row_num,review_list)
            # global review_row_num
            review_row_num += 1
        print("Page->",p)

        if p >= 1:
            break
        # wb.save("booking_scrape.xls")


def scrape_room_info(url, hotel_id):
    '''Scrape Room Info Table'''
    global room_row_num

    r = request_url(url)
    soup = BeautifulSoup(r.content,'html5lib')

    table = soup.find("table",attrs={"class":"roomstable"})
    body = table.find("tbody")
    rows = body.findAll("tr")

    for row in rows:

        sleeps = row.find("span",attrs={"class":"bui-u-sr-only"})
        roomtype = row.find("a",attrs={"class":"jqrt togglelink"})
        bed = row.find("td",attrs={"class":"ftd roomType"})

        if sleeps:
            s = ""
            beds = bed.findAll("li")
            for b in beds:
                b1 = check_empty(b.find("strong"))
                b2 = check_empty(b.find("span"))
                s += b1+" "+b2+"#"

            if roomtype:
                roomid = roomtype['href'][3:]

            # print(roomid," - ",sleeps.text," - ",roomtype.text.strip()," - ",s.strip()," - ",)
            temp_sleeps = sleeps.text
            temp_roomtype = roomtype.text.strip()
            temp_bedtype = s.strip()

            room_detail_list = [roomid,temp_sleeps,temp_roomtype,temp_bedtype,"No size yet",hotel_id]
            insert_sheet(sheet3,room_row_num,room_detail_list)
            wb.save("booking_scrape.xls")
            room_row_num += 1

def scrape_hotel_info(url,hotel_id):
    '''Scrape Detailed information about each Hotel'''
    soup = BeautifulSoup(request_url(url).content,'html5lib')

    rate = soup.find("div",attrs={"class":"bui-review-score__badge"})
    temp_rate = check_empty(rate)

    address = soup.find("span",attrs={"class":"hp_address_subtitle"})
    temp_address = check_empty(address)

    description = soup.find(attrs={"id":"property_description_content"})
    temp_description = check_empty(description)
    #Birdən boş olar deyə yoxla
    joined_date = soup.find("span",attrs={"class":"hp-desc-highlighted"}).text.split("since")[1][1:-2]

    if not rate: rate = ""

    hotel_name_tag = soup.find(attrs={"id":"hp_hotel_name"})
    property_type = hotel_name_tag.find("span").text

    #scrape rooms information from the given table
    scrape_room_info(url,hotel_id)

    # review_count = str_to_int(re.split('[()]',soup.find(attrs={"id":"show_reviews_tab"}).text)[1])

    #if there are reviews then scrape
    # if review_count:
    #     url_list = url.split("/")
    #     page_name = url_list[-1].split(".")[0]
    #     scrape_hotel_reviews(page_name,review_count,hotel_id)

    hotel_info_list = [temp_rate,temp_address,temp_description,joined_date,property_type]

    return hotel_info_list

def get_hotel_rows(hotel, temp_id, row_num):
    '''Get Hotel info from first page'''
    temp_name = hotel.find("span",attrs={"class":"sr-hotel__name"}).text

    star = hotel.find("i",attrs={"class":"bk-icon-stars"})
    if star:
        temp_star = star['title'][0]
    else:
        temp_star = ""

    link = "https://www.booking.com" + hotel.find("a",attrs={"class":"hotel_name_link"})['href'][1:]
    if link:
        temp_link = "https://www.booking.com" + hotel.find("a",attrs={"class":"hotel_name_link"})['href'][1:]
    else:
        temp_link = ""

    temp_coor = hotel.find("a",attrs={"class":"bui-link"})['data-coords']

    price = hotel.find("div",attrs={"class":"bui-price-display__value prco-inline-block-maker-helper"})
    temp_price = check_empty(price)

    imagelink = hotel.find("img",attrs={"class":"hotel_image"})['data-highres']
    temp_imagelink = imagelink

    hotel_list = [temp_id,temp_name,temp_star,temp_link,temp_coor,temp_imagelink, str(temp_price)]
    hotel_info_list = scrape_hotel_info(temp_link,temp_id)

    insert_sheet(sheet1,row_num,hotel_list + hotel_info_list)
    wb.save("booking_scrape.xls")

def scrape_hotels(url):
    '''Scrape Hotel Information in the first page'''
    hotel_id_list = []

    found_props = get_prop_num(url)
    print("Properties = ", found_props)

    page_offset = 0
    hotel_count = 0

    try:
        #row number in sheets
        row_num = 1
        '''Run through all pages'''
        while True:
            #Random time sleep between each request
            time.sleep(random.randint(0,2))
            #start scraping
            soup = BeautifulSoup(request_url(url+str(page_offset)).content,'html5lib')

            hotels = soup.findAll("div",attrs={"class":"sr_item"})

            print("Page : ",page_offset/25+1)
            print("------------------------------------------")
            #Scrape hotel infos from first page
            for hotel in hotels:
                hotel_id = hotel['data-hotelid']

                if hotel_id not in hotel_id_list:

                    get_hotel_rows(hotel, hotel_id, row_num)
                    print("Hotel -> ",row_num)
                    row_num+=1

                hotel_id_list += hotel_id
                hotel_count+=1
            # print("Hotel Count = ",hotel_count)
            wb.save("booking_scrape.xls")
            #Check if page exists
            page_offset+=25
            if hotel_count >= found_props:
                break
        # Save in excel file
        wb.save("booking_scrape.xls")
        print("Finished....")

    except Exception as ex:
        print(ex)
