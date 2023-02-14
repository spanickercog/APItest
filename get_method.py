import requests
from requests.structures import CaseInsensitiveDict

url = "https://cog-ams-control.pxsuite.app/api/public/1a8e44c8-3213-4287-8c70-289c40e20493/presentations/active/scenes"

headers = CaseInsensitiveDict()
headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NjY2OTk0MTcsImlzcyI6ImNvZy1hbXMiLCJleHAiOjE2NjY3MDk0MTd9.CeTpOq8jtnfzcBWTYm-0fIgkF9a4ypbdGOXPuVg-Hdg"
headers["Content-Type"] = "application/json"


resp = requests.post(url, headers=headers)

print(resp.status_code)