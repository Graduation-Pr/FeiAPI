from django.test import TestCase


def initiate_pyament(amount, email, redirect_url):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {"Authorization": f"Bearer {settings.FLW_SEC_KEY}"}

    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "EGP",
        "redirect_url": redirect_url,
        "meta": {"consumer_id": 23, "consumer_mac": "92a3-912ba-1192a"},
        "customer": {
            "email": email,
            "phonenumber": "080****4528",
            "name": "Yemi Desola",
        },
        "customizations": {
            "title": "Pied Piper Payments",
            "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png",
        },
    }

    try:
        response = requests.post(url=url, headers=headers, json=data)
        response_data = response.json
        return Response(response_data)
    except requests.exceptions.ReqeustException as err:
        print("Payment Went Wrong")
        return Response({"Error": str(err)}, status=500)
