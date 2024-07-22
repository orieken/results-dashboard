Feature: Test HTTP POST request

  Scenario: Post payload and check response
    Given I have a url "http://0.0.0.0:5000/test/teams"
    And I have Headers
      | key | value |
      | foo | abc   |
      | bar | 1233  |
    And I POST a payload of "{ \"id\": 1, \"name\": \"team1\" }"
    Then I should get a "201" status code
    And the response body should be "{ \"job\": 112, \"name\": \"team1\" }"

  Scenario: Post payload and check response
    Given I have a url "http://0.0.0.0:5000/test/teams"
    And I have Headers
      | key | value |
      | bad | header   |
    And I POST a payload of "{ \"id\": 1, \"name\": \"team1\" }"
    Then I should get a "400" status code