import json
from curl_cffi import Session
from curl_cffi.requests import RetryStrategy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time, gzip
from datetime import datetime

output_file = gzip.open("crexi_crawled_output.json.gz", "at+")

request_headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.8',
    'cache-control': 'no-cache',
    'client-timezone-offset': '0.0',
    'content-type': 'application/json',
    # 'mixpanel-distinct-id': 'blocked',
    'origin': 'https://www.crexi.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.crexi.com/',
    'schema-mode': 'Searchable',
    # 'search-id': '1787416585139933',
    'sec-ch-ua': '"Not=A?Brand";v="99", "Brave";v="151", "Chromium";v="151"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    # 'traceparent': '00-72eb40837d202555f41efa1c0609f4cc-2dbd496191f7d699-01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    # 'x-session-id': '7496968531263623169',
    # 'x-skip-interceptor': 'true',
}

print("Welcome to crawl crexi website for realestate details.")

def get_input():
    crawl_type = input("What kind of scrapping you need: \nType 'GET' for Requests \nType 'EXIT' to Terminate \n")
    return crawl_type

def requests_extraction(resp):
    loop_items = resp.get("items", [])
    print(f"we get total of {len(loop_items)} in this extraction batch.")
    for item in range(len(loop_items)):
        crawl_date = datetime.now().strftime("%Y%m%d")
        crawl_time = datetime.now().strftime("%H%M%S%f")
        count = resp.get("totalCount", "0")
        single_item = loop_items[item]
        description = single_item.get("description", "")
        sale_id = single_item.get("id", "")
        last_updated = single_item.get("updatedOn", "")
        doc_type = single_item.get("documentType", "")
        property_price  = single_item.get("propertyPrice", {})
        total_price_asked = property_price.get("total", "")
        price_per_square_feet = property_price.get("perSqft", "")
        price_per_acre = property_price.get("perAcre", "")
        financial_details = single_item.get("financials", {})
        asking_price_per_item = financial_details.get("askingPricePerItem", "")
        cap_rate_percent = financial_details.get("capRatePercent", "")
        net_operating_income = financial_details.get("netOperatingIncome", "")
        property_details = single_item.get("propertyAttributes", {})
        building_square_feet = property_details.get("buildingSqft", "")
        building_count = property_details.get("buildingsCount", "")
        story_count = property_details.get("storiesCount", "")
        dock_high_door_count = property_details.get("dockHighDoorsCount", "")
        loading_dock_count = property_details.get("loadingDocksCount", "")
        building_type = property_details.get("type", "")
        building_subtype = property_details.get("subType", "")
        building_class_type = property_details.get("classType", "")
        built_year = single_item.get("constructionYear", {}).get("built", "")
        renovated_year = single_item.get("constructionYear", {}).get("renovated", "")
        acre_size = single_item.get("lotAttributes", {}).get("sizeAcre", "")
        record_type = single_item.get("recordType", {})
        is_sales_comp = record_type.get("isSalesComp", "")
        is_public_sales_comp = record_type.get("isPublicSalesComp", "")
        is_broker_reported_saless_comp = record_type.get("isBrokerReportedSalesComp", "")
        is_lease_comp = record_type.get("isLeaseComp", "")
        gallery_items = single_item.get("gallery", {})
        image_count = gallery_items.get("imageCount", "")
        video_count = gallery_items.get("videoCount", "")
        thumbnail_url = gallery_items.get("thumbnailUrls", [])
        has_virtual_tour = gallery_items.get("hasVirtualTour", "")
        starting_bid = single_item.get("auction", {}).get("startingBid", "")
        minimum_bid = single_item.get("auction", {}).get("minimumBid", "")
        broker_info = single_item.get("brokers", [])
        broker_global_id, broker_thumbnail_url, broker_name, brokerage = list(), list(), list(), list()
        for broker_detail in broker_info:
            broker_global_id.append(broker_detail.get("globalId", ""))
            broker_thumbnail_url.append(broker_detail.get("thumbnailUrl", ""))
            broker_name.append(broker_detail.get("name", ""))
            brokerage.append(broker_detail.get("brokerage",""))
        sale_attributes = single_item.get("listingAttributes", {})
        status = sale_attributes.get("status", "")
        has_sale_on = sale_attributes.get("hasSalesOm", "")
        has_sale_flyer = sale_attributes.get("hasSalesFlyer", "")
        ha_lease_flyer = sale_attributes.get("hasLeaseFlyer", "")
        date_activated = sale_attributes.get("dateActivated", "")
        date_updated = sale_attributes.get("dateUpdated", "")
        is_broker_agent_coop = sale_attributes.get("isBrokerAgentCoOp", "")
        crexi_flyer = single_item.get("hasCrexiFlyer", "")
        property_name = single_item.get("propertyName", "")
        url_slug = single_item.get("urlSlug", "")
        address_details = single_item.get("address", [])
        addres_state_code, address_state_name, full_address, street_address, zipcode, city, county, slug, latitude, longitude = list(), list(), list(), list(), list(), list(), list(), list(), list(), list()
        for address in address_details:
            addres_state_code.append(address.get("stateCode", ""))
            address_state_name.append(address.get("stateName", ""))
            full_address.append(address.get("fullAddress", ""))
            street_address.append(address.get("streetAddress", ""))
            zipcode.append(address.get("zip", ""))
            city.append(address.get("city"))
            county.append(address.get("county", ""))
            slug.append(address.get("slug", ""))
            latitude.append(address.get("location", {}).get("lat", ""))
            longitude.append(address.get("location", {}).get("lon", ""))
        single_output_data = {
            "crawl_date": crawl_date,
            "crawl_time": crawl_time,
            "count": count,
            "description": description,
            "sale_id": sale_id,
            "last_updated": last_updated,
            "doc_type": doc_type,
            "total_price_asked":total_price_asked,
            "price_per_square_feet": price_per_square_feet,
            "price_per_acre": price_per_acre,
            "asking_price_per_item": asking_price_per_item,
            "cap_rate_percent": cap_rate_percent,
            "net_operating_income": net_operating_income,
            "building_square_feet": building_square_feet,
            "building_count": building_count,
            "story_count": story_count,
            "dock_high_door_count": dock_high_door_count,
            "loading_dock_count":  loading_dock_count,
            "building_type": building_type,
            "building_subtype": building_subtype,
            "building_class_type": building_class_type,
            "built_year": built_year,
            "renovated_year": renovated_year,
            "acre_size": acre_size,
            "is_sales_comp": is_sales_comp,
            "is_public_sales_comp": is_public_sales_comp,
            "is_broker_reported_saless_comp": is_broker_reported_saless_comp,
            "is_lease_comp": is_lease_comp,
            "image_count": image_count,
            "video_count": video_count,
            "thumbnail_url":thumbnail_url,
            "has_virtual_tour": has_virtual_tour,
            "starting_bid": starting_bid,
            "minimum_bid": minimum_bid,
            "broker_global_id": broker_global_id,
            "broker_thumbnail_url": broker_thumbnail_url,
            "broker_name": broker_name,
            "brokerage": brokerage,
            "addres_state_code": addres_state_code,
            "address_state_name": address_state_name,
            "full_address": full_address,
            "street_address": street_address,
            "zipcode": zipcode,
            "city": city,
            "county": county,
            "slug": slug,
            "latitude": latitude,
            "longitude": longitude,
            "status": status,
            "has_sale_on": has_sale_on,
            "has_sale_flyer": has_sale_flyer,
            "ha_lease_flyer": ha_lease_flyer,
            "date_activated": date_activated,
            "date_updated": date_updated,
            "is_broker_agent_coop": is_broker_agent_coop,
            "crexi_flyer": crexi_flyer,
            "property_name": property_name,
            "url_slug": url_slug
        }
        json.dump(single_output_data, output_file)
        output_file.write("\n")

def requests_method_complete(max_retry = 3):
    increase_size = 100
    json_data = {
        'boundingBox': None,
        'excludeFilters': [],
        'excludeSort': [],
        'filters': {
            'searchAttributes.status': {
                'mode': 'Include',
                'structuredValues': [
                    'On-Market',
                    'Auction',
                    'Highest & Best',
                    'Call For Offers',
                ],
                'type': 'Plain',
                'values': [],
            },
        },
        'from': 0,
        'ids': [],
        'searchTypes': [
            'Sales',
        ],
        'size': increase_size,
        'sorting': {},
    }

    strategy = RetryStrategy(count=max_retry, delay=0.2, jitter=0.1, backoff="exponential")
    with Session(retry=strategy, timeout=10) as session:
        count_request = session.post('https://api.crexi.com/universal-search/v2/search', headers=request_headers, json=json_data)
    if count_request.status_code == 200:
        total_count = count_request.json().get("totalCount", "0")
        print(f"The total number of records found for the entire US is {total_count}.")
    else:
        print(f"We are getting blocked with status code {count_request.status_code}")

    for start_size in range(0, total_count,100):
        json_data['from'] = int(start_size)
        print(f"started crawling from {start_size} with the increment items of {increase_size}")
        strategy = RetryStrategy(count=max_retry, delay=0.2, jitter=0.1, backoff="exponential")
        with Session(retry=strategy, timeout=10) as session:
            resp = session.post('https://api.crexi.com/universal-search/v2/search', headers=request_headers, json=json_data)
            if resp.status_code == 200:
                print(f"We get status code of {resp.status_code} for the item {start_size} to {start_size + increase_size}")
                resp_json_data = resp.json()
                if resp_json_data:
                    requests_extraction(resp=resp_json_data)
                else:
                    print(f"We are getting empty json content. \n{resp.content}")
            else:
                print(f"We are getting blocked with status code {resp.status_code}")

def requests_method_location(location = "albany", max_retry = 3):
    increase_size = 100
    json_data = {
        'boundingBox': None,
        'excludeFilters': [],
        'excludeSort': [],
        'filters': {
            'searchAttributes.status': {
                'mode': 'Include',
                'structuredValues': [
                    'On-Market',
                    'Auction',
                    'Highest & Best',
                    'Call For Offers',
                ],
                'type': 'Plain',
                'values': [],
            },
            'keywords': {
                'mode': 'Include',
                'structuredValues': [
                    location,
                ],
                'type': 'Plain',
                'values': [],
            },
        },
        'from': 0,
        'ids': [],
        'searchTypes': [
            'Sales',
        ],
        'size': increase_size,
        'sorting': {},
    }

    strategy = RetryStrategy(count=max_retry, delay=0.2, jitter=0.1, backoff="exponential")
    with Session(retry=strategy, timeout=10) as session:
        count_request = session.post('https://api.crexi.com/universal-search/v2/search', headers=request_headers, json=json_data)
    if count_request.status_code == 200:
        total_count = count_request.json().get("totalCount", "0")
        print(f"The total number of records found for the entire US is {total_count}.")
    else:
        print(f"We are getting blocked with status code {count_request.status_code}")

    for start_size in range(0, total_count,100):
        json_data['from'] = int(start_size)
        print(f"started crawling from {start_size} with the increment items of {increase_size}")
        strategy = RetryStrategy(count=max_retry, delay=0.2, jitter=0.1, backoff="exponential")
        with Session(retry=strategy, timeout=10) as session:
            resp = session.post('https://api.crexi.com/universal-search/v2/search', headers=request_headers, json=json_data)
            if resp.status_code == 200:
                print(f"We get status code of {resp.status_code} for the item {start_size} to {start_size + increase_size}")
                resp_json_data = resp.json()
                if resp_json_data:
                    requests_extraction(resp=resp_json_data)
                else:
                    print(f"We are getting empty json content. \n{resp.content} \nPlease check that the given location is valid and present in US.")
            else:
                print(f"We are getting blocked with status code {resp.status_code}")

def process_input(crawl_type):
    if crawl_type in ["GET", "get", "Get"]:
        print("Request Crawl has been Initiated.")
        get_specific = input("press '1' to get complete data. \npress '2' to get data for specific location.\n")
        if get_specific in ['1', 1]:
            requests_method_complete(max_retry=2)

        elif get_specific in ['2', 2]:
            location = input("Please provide keyword Location in US to serch for: ")
            requests_method_location(location=location)

        else:
            print("The provided input is wrong please try again.")
            process_input(crawl_type=crawl_type)

    elif crawl_type in ["Exit", "EXIT", "exit"]:
        print("Process Terminated")
        print("Thank you.")

    else:
        print(f"The given input '{crawl_type}' is invalid. Please give proper input: ")
        crawl_type = get_input()
        process_input(crawl_type=crawl_type)

if __name__ == "__main__":
    crawl_type = get_input()
    process_input(crawl_type=crawl_type)