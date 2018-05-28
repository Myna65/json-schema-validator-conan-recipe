#include <iostream>

#include "json-schema.hpp"

using nlohmann::json;
using nlohmann::json_uri;
using nlohmann::json_schema_draft4::json_validator;

// The schema is defined based upon a string literal
static json person_schema = R"(
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "A person",
    "properties": {
        "name": {
            "description": "Name",
            "type": "string"
        },
        "age": {
            "description": "Age of the person",
            "type": "number",
            "minimum": 2,
            "maximum": 200
        }
    },
    "required": [
                 "name",
                 "age"
                 ],
    "type": "object"
}

)"_json;

// The people are defined with brace initialization
static json bad_person = {{"age", 42}};
static json good_person = {{"name", "Albert"}, {"age", 42}};

int main(){

    /* json-parse the schema */

    json_validator validator; // create validator

    try {
        validator.set_root_schema(person_schema); // insert root-schema
    } catch (const std::exception &e) {
        std::cerr << "Validation of schema failed, here is why: " << e.what() << "\n";
        return EXIT_FAILURE;
    }

    /* json-parse the people */

    for (auto &person : {bad_person, good_person})
    {
        std::cout << "About to validate this person:\n" << std::setw(2) << person << std::endl;
        try {
            validator.validate(person); // validate the document
            std::cout << "Validation succeeded\n";
        } catch (const std::exception &e) {
            std::cerr << "Validation failed, here is why: " << e.what() << "\n";
        }
    }
    return EXIT_SUCCESS;
}
