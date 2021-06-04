SOURCE_NAMING_EXCEPTION_MESSAGE = """
Each variable is required to have a source. 
The source naming is the normal variable name plus _SOURCE

An example for a correct class:

class ExampleObj:
    number: int
    question: bool

    NUMBER_SOURCE = "data-number"
    QUESTION_SOURCE = "data-question"


If the variable NUMBER_SOURCE would change to NUMBER_
"""


class TestObj:
    number: int
    question: bool

    NUMBER_SOURCE = "data-number"  # dict source
    QUESTION_SOURCE = "data-question"  # dict source
    QUESTION_TYPE_ERROR = Exception  # when the source does not exist
    NUMBER_DOES_NOT_EXIST = None


dict_input_test = {
    "data": {
        "number": 123,
        "question": True
    }
}


class SpecialDictModel:

    def __init__(self, input_class, input_data):
        self.input_class = input_class
        self.class_attr = self.input_class.__dict__
        self.class_annotations = self.class_attr.get('__annotations__')
        self.input_data = input_data

    def run(self):
        self.validate_usages_in_class()
        self.insert_values_to_class()
        return self.input_class

    def insert_values_to_class(self):
        for variable_name in self.class_annotations:
            variable_input = self.get_input_from_source(variable_name)
            if type(variable_input) is self.class_annotations[variable_name]:
                setattr(self.input_class, variable_name, variable_input)
            else:
                setattr(self.input_class, variable_name, None)

    def get_input_from_source(self, variable_name):
        source = self.class_attr.get(f"{variable_name.upper()}_SOURCE")
        split_source = source.split('-')
        data = self.input_data
        for part in split_source:
            data = data.get(part)
        return data

    # Usages Validations

    def validate_usages_in_class(self):
        self.is_valid_variable_names()

    def is_valid_variable_names(self):
        for name in self.class_annotations:
            if f"{name.upper()}_SOURCE" not in self.class_attr:
                raise Exception(SOURCE_NAMING_EXCEPTION_MESSAGE)
        return True


def test():
    test_obj: TestObj = SpecialDictModel(TestObj, dict_input_test).run()
    print(test_obj.number, test_obj.question)
