import requests
import rdflib
import secrets
import hashlib
from base64 import urlsafe_b64encode

oidcIssuer_query = """
SELECT ?oidcIssuer 
WHERE {
    ?s <http://www.w3.org/ns/solid/terms#oidcIssuer> ?oidcIssuer .
}"""

def encode_string(secret_string: str):
    ascii = secret_string.encode('ascii')
    m = hashlib.sha256()
    m.update(ascii)
    result = m.digest()
    text = urlsafe_b64encode(result).rstrip(b'=')
    return str(text, encoding='utf-8')

def get_oidc_issuer(web_id: str):
    g = rdflib.Graph()
    g.parse(web_id, format="turtle")
    # for s, p, o in g.triples((None, None, None)):
    #     print(f'{s}, {p}, {o}')
    result = g.query(oidcIssuer_query)
    for row in result:
        oidc_issuer = row[0]
    return oidc_issuer

def get_auth_endpoint(oidc_issuer: str):
    openid_config = str(oidc_issuer) + "/.well-known/openid-configuration"
    response = requests.get(openid_config)
    data = response.json()
    authorization_endpoint = data['authorization_endpoint']
    return (data, authorization_endpoint)
