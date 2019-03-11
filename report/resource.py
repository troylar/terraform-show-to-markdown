
class Resource:
    def __init__(self, **kwargs):
        self.data = kwargs.get('Data')

    def id(self):
        if 'arn' in self.data.keys():
            return self.data['arn']
        if 'id' in self.data.keys():
            return self.data['id']