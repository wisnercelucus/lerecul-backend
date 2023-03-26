class IncorrectDateRangeError(Exception):
    def __init__(self, message="Incorrect Date Range."):
        self.message = message
        super().__init__(self.message)


class NonRelatedParentError(Exception):
    def __init__(self, message="The selected project does not exist on the program selected."):
        self.message = message
        super().__init__(self.message)


class InvalidComponentError(Exception):
    def __init__(self, message="A component should either be associated with a program or a project."):
        self.message = message
        super().__init__(self.message)


class InvalidIndicatorError(Exception):
    def __init__(self, message="An indicator should either be associated with an activity, an output, an outcome, a project or all."):
        self.message = message
        super().__init__(self.message)


class InvalidDisaggregatedOptionField(Exception):
    def __init__(self, message="A disagreggated option field must be associated with a a disaggregated option."):
        self.message = message
        super().__init__(self.message)


class ExtensionNotAcceptableError(Exception):
    """
        Raise an exception error if a selected file extension
        is not allowed/acceptable.
        Attributes:
            ext -- input (string) extension which caused the error.
            error_msg -- explanation of the error.
    """

    def __init__(self, ext, error_msg="not acceptable."):
        self.ext = ext
        self.error_msg = error_msg
        super().__init__(self.error_msg)

    def __str__(self):
        return f'File of type {self.ext} is {self.error_msg}'