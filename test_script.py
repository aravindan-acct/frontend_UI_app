import requests

headers = {"api_key":"test",
               "Postman-Token":"6009e770-58ea-4081-8e7a-22ec012d8ed7"}

backend_url = "http://20.124.190.228:8080/api/petstore/1.0.0"

#all_pets_resp = requests.get(backend_url+"/store/inventory", headers=headers)

#print(all_pets_resp.text)

search_by_pet_id = requests.get(backend_url+"/pet/1?access_token=021af442-8972-4248-bb1e-4e59cdc464bc&token_type=bearer&state=345fabd0-2246-41bf-be1e-5c429c681aaa&expires_in=20", headers=headers)
print(search_by_pet_id.text)

