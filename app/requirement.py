class Requirement:

    def __init__(self, *, id, text):
        # These attributes are a part of the OpenReq JSON Standard: <Link to OpenReq JSON Standard>

        ## Required by this API ##
        # The unique identifier of a Requirement. Not a null value or an empty string.
        self.id = id
        # The textual description or content of a Requirement.
        self.text = text


    def __str__(self):
        return f'{{' \
            f'\n\tself.id = {self.id}'\
            f'\n\tself.text = {self.text}'\
            f'\n}}'
