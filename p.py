import requests

url = "https://www.kletech.ac.in/belagavi/"
data = {
    "input_field_name": "<script>alert('XSS')</script>"
}

response = requests.post(url, data=data)
if "<script>alert('XSS')</script>" in response.text:
    print("Potential XSS detected!")
else:
    print("No XSS detected in response (safe check).")

