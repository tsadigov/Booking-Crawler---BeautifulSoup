import functions as f

url = "https://www.booking.com/searchresults.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaBGIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AtzNk_IFwAIB&sid=1c5ed2b9818024b41cee0129ad517f23&tmpl=searchresults&ac_click_type=b&ac_position=0&class_interval=1&dest_id=15&dest_type=country&dtdisc=0&from_sf=1&group_adults=3&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=2&postcard=0&raw_dest_type=country&room1=A&room2=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&src=index&src_elem=sb&srpvid=550a499f90db008c&ss=Azerbaijan&ss_all=0&ss_raw=az&ssb=empty&sshis=0&top_ufis=1&rows=25&offset="

# url = "https://www.booking.com/hotel/az/qafqaz-tufandag-mountain-resort.html?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaBGIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Aobe6e8FwAIB;sid=9d873b3cc4ce4be633a473d9e3d1c60a;age=12;dest_id=15;dest_type=country;dist=0;group_adults=2;group_children=1;hapos=7;hpos=7;no_rooms=1;req_adults=2;req_age=12;req_children=1;room1=A%2CA%2C12;sb_price_type=total;sr_order=popularity;srepoch=1580820338;srpvid=0d9f59b905b70038;type=total;ucfs=1&#hotelTmpl"

price_url = "https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaBGIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AvGEivIFwAIB&sid=9d873b3cc4ce4be633a473d9e3d1c60a&tmpl=searchresults&checkin_month=2&checkin_monthday=15&checkin_year=2020&checkout_month=2&checkout_monthday=16&checkout_year=2020&city=-2705195&class_interval=1&dest_id=-2705195&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=searchresults&src_elem=sb&srpvid=85c74d9a5c6f01bf&ss=Baku&ss_all=0&ssb=empty&sshis=0&ssne=Baku&ssne_untouched=Baku&top_ufis=1&rows=25&offset="

f.scrape_hotels(url)
