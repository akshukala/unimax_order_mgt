def address_as_json(address):
    address= address
    name = ""
    if address.farmer.first_name:
        name += str(address.farmer.first_name)
    if address.farmer.middle_name:
        name += ' ' + str(address.farmer.middle_name)
    if address.farmer.last_name:
        name += ' ' + str(address.farmer.last_name)

    if address.village:
        village = str(address.village)
    else:
        village = ""

    if address.taluka:
        taluka = str(address.taluka)
    else:
        taluka = ""

    if address.post_office:
        post_office = str(address.post_office)
    else:
        post_office = ""

    if address.other_taluka:
        other_taluka = str(address.other_taluka)
    else:
        other_taluka = ""

    if address.street.strip():
        street = str(address.street)
    else:
        street = "--"

    mobiles = []
    if address.farmer.mobile_1:
        mobiles.append(str(address.farmer.mobile_1))
    if address.farmer.mobile_2:
        mobiles.append(str(address.farmer.mobile_2))
    if address.farmer.mobile_3:
        mobiles.append(str(address.farmer.mobile_3))

    mobile = " , ".join(mobiles[:2])

    if address.country:
        country = address.country
    else:
        country = "IN"

    if address.pin_code:
        pin_code = str(address.pin_code)
    else:
        pin_code = ""

    if address.district:
        district = str(address.district)
    else:
        district = ""

    address_line_one = street
    address_line_two = village + " - " + post_office + " - " + taluka
    if other_taluka:
        address_line_two += " - " + other_taluka

    return dict(
        City=district, Name=name, Country=country,
        Pincode=pin_code, Phone=mobile,
        State=str(address.state), AddressLine1=address_line_one,
        AddressLine2=address_line_two
    )