from typing import List
from .org import Org
from .collection import Collection
from .models.user import User, ApiKey
from .jiggybase_session import JiggyBaseSession

    

class JiggyBase():

    def __init__(self):
        self.session = JiggyBaseSession()     
        
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
        resp = self.session.get("/collections")
        return [Collection(self.session, **c) for c in resp.json()]
   
    def collection_names(self) -> List[Collection]:
        """
        return the unique collection name for all collections in all Orgs that the user is a member of
        """
        return [c.name for c in self.collections()]
            
    def collection(self, name : str) -> Collection:        
        """
        return a collection of the specified name
        """
        for collection in self.collections():
            if collection.name == name or collection.display_name.lower() == name.lower():
                return collection
        raise ValueError(f'Collection "{name}" not found')
