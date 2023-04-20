# Jiggy Client

import os
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3 import Retry
from requests.adapters import HTTPAdapter
import requests
from .login import window_open

GPTG_HOST     = 'https://api.gpt-gateway.com'

GPTG_KEY_FILE = os.path.expanduser('~') + '/.gptg'   # local file to store user entered apikey 


class ClientError(Exception):
    """
    API returned 4xx client error
    """

class ServerError(Exception):
    """
    API returned 5xx Server error
    """

    
class GPTGSession(requests.Session):
    def __init__(self, gptg_api='gpt-gateway-v1', gptg_host=GPTG_HOST, *args, **kwargs):
        """
        Extend requests.Session with common GPTG authentication, retry, and exceptions.

        gptg_api:  The gptg api & version to use.
        
        gptg_host: The url host prefix of the form "https:/api.gpt-gateway.com"
                    if gptg_host arg is not set, will use 
                    GPTG_HOST environment variable or "api.gpt-gateway.com" as final default.
        
        final url prefix are of the form "https:/{gptg_host}/{gptg_api}"
        """
        super(GPTGSession, self).__init__(*args, **kwargs)
        self.host = gptg_host
        self.prefix_url = f"{gptg_host}/{gptg_api}"
        test_url = f"{self.prefix_url}/docs"
        if requests.head(test_url).status_code != 200:
            raise Exception(f"Invalid or unreachable api: {self.prefix_url}")
            
        self.bearer_token = None
        super(GPTGSession, self).mount('https://',
                                        HTTPAdapter(max_retries=Retry(connect=5,
                                                                      read=5,
                                                                      status=5,
                                                                      redirect=2,
                                                                      backoff_factor=.001,
                                                                      status_forcelist=(500, 502, 503, 504))))

    def _set_bearer(self, jwt):
        self.bearer_token = jwt
        print(jwt)
        self.headers['Authorization'] = f"Bearer {jwt}"

    def _getjwt(self, key):        
        resp = requests.post(f"{self.host}/gpt-gateway-v1/auth", json={'key': key})
        if resp.status_code == 200:
            self._set_bearer(resp.json()['jwt'])
        elif resp.status_code == 401:
            raise ClientError("Invalid API Key")
        else:
            raise ServerError(resp.content)

    def _auth(self):
        if 'GPTG_API_KEY' in os.environ:
            self._getjwt(os.environ['GPTG_API_KEY'])
        elif os.path.exists(GPTG_KEY_FILE):
            self._getjwt(open(GPTG_KEY_FILE).read())
        else:
            while True:
                window_open("https://gpt-gateway.com/authorize")
                key_input = input("Enter your gpt-gateway.com API Key: ")
                if key_input[:4] == "jgy-":
                    # try using the key to see if it is valid
                    try:
                        self._getjwt(key_input)
                        # key validated, save to key file
                        open(GPTG_KEY_FILE, 'w').write(key_input)
                        os.chmod(GPTG_KEY_FILE, 0o600)  # -rw-------
                        break
                    except:
                        pass
                print("Invalid API Key")

        
    def request(self, method, url, *args, **kwargs):
        if not self.bearer_token:
            self._auth()
        url = self.prefix_url + url
        #print("~~~~~~~~~~~~~~~~~~~~~~~~\n", method, url)
        # support 'model' (pydantic BaseModel) arg which we convert to json parameter
        if 'model' in kwargs:
            kwargs['data'] = kwargs.pop('model').json()
        resp =  super(GPTGSession, self).request(method, url, *args, **kwargs)
        if resp.status_code == 401:
            self.bearer_token = None
            del self.headers['Authorization']
            self._auth()
            resp =  super(GPTGSession, self).request(method, url, *args, **kwargs)
        if resp.status_code in [500, 502, 503, 504]:
            pass # TODO: retry these cases        
        if resp.status_code >= 500:
            raise ServerError(resp.content)
        if resp.status_code >= 400:
            raise ClientError(resp.content)
        return resp

