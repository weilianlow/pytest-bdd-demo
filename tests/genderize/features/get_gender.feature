Feature: get age

  Scenario Outline: get gender by name
    When the following http curl response is saved as res1:
      curl -X GET https://api.genderize.io/?name=<name>
    Then the status code for res1 should be 200
    Then the JSONPath $.name value for res1 should match ['<name>']
    Then the JSONPath $.gender value for res1 should match [<gender>]
    Then the JSONPath $.probability value for res1 should match ['<probability>']
    Then the JSONPath $.count value for res1 should match ['<expression>']
    Examples:
      | name      | gender   | probability | expression |
      | Adam      | 'male'   | <1          | >0         |
      | Betty     | 'female' | <1          | >0         |
      | Catherine | 'female' | <1          | >0         |
      | 3         | None     | ==0         | ==0        |
