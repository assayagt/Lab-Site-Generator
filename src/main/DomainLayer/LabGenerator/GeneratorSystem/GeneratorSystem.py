class GeneratorSystem:
    _singleton_instance = None

    def __init__(self):
        if GeneratorSystem._singleton_instance is not None:
            raise Exception("This is a singleton class!")

    @staticmethod
    def get_instance():
        if GeneratorSystem._singleton_instance is None:
            GeneratorSystem._singleton_instance = GeneratorSystem()
        return GeneratorSystem._singleton_instance