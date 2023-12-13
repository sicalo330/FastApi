@movies @api
Feature: Movies
    As anplication developer, I want  to work with
    the movies Api, so that I can work with movies
    data.

    @tc_01 @functional @smoke
    Scenario: Search all the movies when there are no records
        when the users sends "GET" request to "/movies" endpoint
        then the response  status code should  be "200"
        And the response body should have "0" elements
        And the response should fit the following schema "get_movies_schema.json"