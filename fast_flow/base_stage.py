class BaseStage(object):
    def __init__(self, name, output_directory, after=None):
        self.__name = name
        self.__output_dir = output_directory
        if after is not None:
            raise NotImplementedError("The `after` keyword is not yet supported for stages")

    @property
    def name(self):
        return self.__name

    @property
    def output_dir(self):
        return self.__output_dir

    def apply_description(self, **args):
        raise NotImplementedError

    def build(self):
        """
        Convert this stage to a list of reader collector pairs
        returns: a list of reader-collector pairs
        """
        raise NotImplementedError
