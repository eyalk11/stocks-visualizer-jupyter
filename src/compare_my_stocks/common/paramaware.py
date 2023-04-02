import dataclasses

'''
Parameteres has many default values. Here we want to see what we changed explicitly. In order to be able to merge to parameters. 
'''

def paramaware(klass):
    orginit=klass.__init__
    orgset = klass.__setattr__
    # def __setstate__(self,state):
    #     return super(klass,self).__setstate__(state)
    def __setstate__(self,state):
        self._changed_keys = set(state.keys())
        for slot, value in state.items():
            object.__setattr__(self, slot, value)
    def __nsetattr__(self, name, value):
        if hasattr(self,'_changed_keys') and name in self.__dataclass_fields__.keys():
            self._changed_keys.add(name)
        return orgset(self,name,value)

    def newinit(self,*args,**kwargs):
        orginit(self,*args,**kwargs)
        self._changed_keys=set(kwargs.keys()).intersection(set(self.__dataclass_fields__.keys())) #TODO: take care of args.

    def update_from(self,another):
        dic= dataclasses.asdict(another)
        for k in another._changed_keys:
            setattr(self,k,dic[k])

    klass.__init__=newinit
    klass.__setattr__=__nsetattr__
    #klass.__orgsetstate__ = klass.__setstate__
    klass.__setstate__ = __setstate__

    klass.update_from=update_from

    return klass
