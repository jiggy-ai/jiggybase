from typing import List
from .org import Org
from .collection import Collection
from .models.user import User, ApiKey
from .gptg_session import GPTGSession

    

class GPTGateway():

    def __init__(self):
        self.session = GPTGSession()     
        
    def orgs(self) -> List[Org]:
        """
        return all Orgs that the user is a member of
        """
        resp = self.session.get('/orgs')
        return [Org(self.session, **i) for i in resp.json()]

    def get_org(self, name_or_id) -> Org:
        """
        get org by name or id
        raises Exception if an exact match for name is not found
        """
        orgs = [t for t in self.session.get('/orgs').json() if t['name'] == name_or_id or t['id'] == name_or_id]
        if len(orgs):
            return Org(self.session, **orgs[0])
        raise Exception(f'Org "{name_or_id}" not found')


    def api_keys(self) -> List[ApiKey]:
        """
        return user's api keys
        """
        return [ApiKey(**i) for i in self.session.get('/apikey').json()]


    def authenticated_user(self) -> User:
        """
        return the authenticated user's User object
        """
        return User(**self.session.get("/users/current").json())


    def create_org(self, name : str) -> Org:
        """
        create an Org
        """
        resp = self.session.post("/orgs", json={"name":name})
        return Org(self.session, **resp.json())

    def collections(self) -> List[Collection]:
        """
        return all Collections in all Orgs that the user is a member of
        """
        collections = []
        for org in self.orgs():
            for collection in org.collections():
                collections.append(collection)
        return collections
