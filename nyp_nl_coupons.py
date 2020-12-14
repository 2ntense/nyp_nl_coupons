from bs4 import BeautifulSoup

import requests


def new_session():
    session = requests.session()
    session.get("https://www.newyorkpizza.nl")
    return session


def set_store(zip_code, session):
    request_url = "https://www.newyorkpizza.nl/Order/SetStoreOnOrder"
    payload = {
        "DeliveryType": "Delivery",
        "ZipCode": zip_code,
        "IsReceiptForm": "False",
        "ZipCodeDeliveryOrPickup": "Delivery",
        "X-Requested-With": "XMLHttpRequest"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    session.post(request_url, data=payload, headers=headers)


def add_item(product_id, option_id, quantity, session):
    request_url = "https://www.newyorkpizza.nl/Order/AddProductToCurrentOrder"
    payload = {
        "productId": product_id,
        "optionId": option_id,
        "quantity": quantity
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    session.post(request_url, data=payload, headers=headers)


def add_pizza(session):
    # 25 cm brooklyn style
    add_item(93, 1, 1, session)


def add_coke(session):
    add_item(111, 6, 1, session)


def show_receipt(session):
    request_url = "https://www.newyorkpizza.nl/Menu/_ReceiptPartial"
    payload = {
        "isCheckoutPage": "false"
    }
    response = session.post(request_url, data=payload)
    return response.text


def add_coupon(code: str, session):
    request_url = "https://www.newyorkpizza.nl/CheckOut/AddCouponCodeToCurrentOrder"
    payload = {
        "couponCode": code
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    response = session.post(request_url, data=payload, headers=headers)
    return response.json()["succeeded"]


def remove_coupon(cid: str, session):
    request_url = "https://www.newyorkpizza.nl/Order/RemoveCouponFromCurrentOrder"
    payload = {
        "couponIdentifier": cid,
        "alsoRemoveProducts": False
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    session.post(request_url, data=payload, headers=headers)


def show_coupons(session):
    request_url = "https://www.newyorkpizza.nl/Checkout/_PromotionPartial"
    response = session.get(request_url)
    return response.text


def get_coupon_details(session):
    soup = BeautifulSoup(show_receipt(session), 'html.parser')
    coupon_div = soup.find(class_="nyp-coupon-product")
    if coupon_div is None:
        soup = BeautifulSoup(show_coupons(session), 'html.parser')
        coupon_id = soup.find(class_="remove-coupon")["data-coupon-identifier"]
        coupon_desc = soup.find(class_="nyp-discount-decoration").text.strip()
    else:
        coupon_desc = coupon_div.find(class_="h3").text.strip()
        coupon_id = coupon_div.find(class_="nyp-receipt-remove")["data-identifier"]
    return coupon_id, coupon_desc


def write_to_file(dict):
    with open("coupons.txt", "w") as fp:
        for k, v in dict.items():
            fp.write(f"{k} - {v}\n")


def scenario_5(session):
    coupon_dict = {}
    add_item(83, 102, 2, session)
    add_item(111, 6, 2, session)
    add_item(430, 132, 1, session)
    add_item(54, 121, 1, session)
    add_item(314, 117, 1, session)
    add_item(43, 118, 1, session)
    add_item(45, 34, 1, session)
    add_item(48, 17, 1, session)
    add_item(454, 21, 1, session)
    add_item(62, 22, 1, session)
    add_item(61, 21, 1, session)
    add_item(59, 21, 1, session)
    add_item(236, 12, 1, session)
    add_item(64, 12, 1, session)
    add_item(275, 100, 1, session)
    add_item(434, 91, 1, session)
    add_item(189, 76, 1, session)
    add_item(63, 12, 1, session)
    add_item(72, 12, 1, session)
    add_item(75, 12, 1, session)
    add_item(93, 1, 10, session)
    for i in range(100, 1000):
        print(f"Checking {i}")
        if add_coupon(str(i), session):
            coupon_details = get_coupon_details(session)
            coupon_dict[str(i)] = coupon_details[1]
            remove_coupon(coupon_details[0], session)
    write_to_file(coupon_dict)


# 5x 25 cm non-promo pizza + coke
def scenario_4(session):
    coupon_dict = {}
    add_pizza(session)
    add_pizza(session)
    add_pizza(session)
    add_pizza(session)
    add_pizza(session)
    add_coke(session)
    for i in range(100, 1000):
        print(f"Checking {i}")
        j = add_coupon(str(i), session)
        if j["succeeded"]:
            coupon_details = get_coupon_details(session)
            coupon_dict[str(i)] = coupon_details[1]
            remove_coupon(coupon_details[0], session)
    print(coupon_dict)


# 2x 25 cm non-promo pizza + coke
def scenario_3(session):
    coupon_dict = {}
    add_pizza(session)
    add_pizza(session)
    add_coke(session)
    for i in range(100, 1000):
        print(f"Checking {i}")
        if add_coupon(str(i), session):
            coupon_details = get_coupon_details(session)
            coupon_dict[str(i)] = coupon_details[1]
            remove_coupon(coupon_details[0], session)
    print(coupon_dict)


# 2x 25 cm non-promo pizza
def scenario_2(session):
    coupon_dict = {}
    add_pizza(session)
    add_pizza(session)
    for i in range(100, 1000):
        print(f"Checking {i}")
        if add_coupon(str(i), session):
            coupon_details = get_coupon_details(session)
            coupon_dict[str(i)] = coupon_details[1]
            remove_coupon(coupon_details[0], session)
    print(coupon_dict)


# 1x 25 cm non-promo pizza
def scenario_1(session):
    coupon_dict = {}
    add_pizza(session)
    for i in range(100, 1000):
        print(f"Checking {i}")
        if add_coupon(str(i), session):
            coupon_details = get_coupon_details(session)
            coupon_dict[str(i)] = coupon_details[1]
            remove_coupon(coupon_details[0], session)
    print(coupon_dict)


# verifies coupons 100 to 999. will not show on what kind of order it applies to exactly
# currently broken
# def scenario_0(session):
#     coupon_dict = {}
#     for i in range(100, 999 + 1):
#         print(f"Checking {i}")
#         j = add_coupon(str(i), session)
#         if j["error"] != "CouponCodeInvalid":
#             coupon_dict[str(i)] = j["error"]
#     pprint(coupon_dict)


def main():
    session = new_session()
    set_store("", session)

    # scenario_0(session)
    # scenario_1(session)
    # scenario_2(session)
    # scenario_3(session)
    # scenario_4(session)
    scenario_5(session)


if __name__ == '__main__':
    main()
