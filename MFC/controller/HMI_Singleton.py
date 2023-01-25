
from interface.HMI_Interface import HMI_Interface


class SingletonInstance2:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance


class HMI_Interface_Singleton(HMI_Interface, SingletonInstance2):
    pass


TheHmi = HMI_Interface_Singleton.instance()
