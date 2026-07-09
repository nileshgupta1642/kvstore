'''
Tiny persistent key-value store
'''
class KVStore:
    def __init__(self):
        self.kv_store = {}


    def set(self, key: str, val: str) -> bool:
        '''
        Sets key,val in kv store
        '''
        self.kv_store[key] = val
        return True

    def get(self, key: str) -> str | None:
        '''
        Returns val for key in kv store
        None if not found
        '''
        if key not in self.kv_store:
            return None
        return self.kv_store[key]

    def delete(self, key: str) -> str | None:
        '''
        Deletes key if it exists and returns it
        Returns None if doesn't exist
        '''
        if key not in self.kv_store:
            return None
        ret = self.kv_store[key]
        del self.kv_store[key]
        return ret


    def list_keys(self):
        '''
        Prints list of keys in kv_store
        '''
        print(self.kv_store.keys())
