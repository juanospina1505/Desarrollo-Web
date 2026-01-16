import requests

response = requests.get("https://opttime.proalnet.com/")

propiedades = {"status": response.status_code,
               "content/body": response.text,
               "headers": response.headers,
               "cookies": response.cookies}

print(f"Respuesta al metodo get de la petición a: {response.url} \n")
print(f"status: {propiedades['status']} \n")
print(f"HTML: {propiedades['content/body']} \n")
print(f"Headers: {propiedades['headers']} \n")
print(f"Cookies: {propiedades['cookies']} \n")
