
class BaseResource:
    def __init__(self, **kwargs):
        data = kwargs.get('Data')
        self.name = kwargs.get('Name')
        for key, val in data.items():
            setattr(self, key, val)

    @property
    def resource(self):
        return self.name.split('.')[0]

    @property
    def has_role(self):
        return hasattr(self, 'role')

    @property
    def has_name(self):
        return hasattr(self, 'name')

    @property
    def has_policy(self):
        return hasattr(self, 'policy') or hasattr(self, 'policy_arn')

    @property
    def resource_policy(self):
        if not self.has_policy:
            return ''
        if hasattr(self, 'policy'):
            return self.policy
        if hasattr(self, 'policy_arn'):
            return self.policy_arn

    @property
    def properties(self):
        return self.__dict__


class Resource(BaseResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def u_id(self):
        ids = ['arn', 'certificate_arn', 'id']
        for id in ids:
            if id in self.__dict__.keys():
                return self.__dict__[id]


class ResourceManager:
    def __init__(self, **kwargs):
        self.data = kwargs.get('Data')

    def find_by_name(self, name):
        for res in self.data:
            if res.has_name and res.name == name:
                return res
