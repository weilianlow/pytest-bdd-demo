Feature: get age

  Scenario Outline: get age by name
    When the following http curl response is saved as res1:
      curl -X GET https://api.agify.io/?name=<name>
    Then the status code for res1 should be 200
    Then the JSONPath $.name value for res1 should match ['<name>']
    Then the JSONPath $.age value for res1 should match [<age>]
    Then the JSONPath $.count value for res1 should match ['<expression>']
    Examples:
      | name      | age | expression |
      | Adam      | 36  | >0         |
      | Betty     | 60  | >0         |
      | Catherine | 68  | >0         |
      | 3         |     | ==0        |