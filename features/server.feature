Feature: Server APIs basic functions
  Tests whether all the APIs respond and the server is healthy

  Scenario: server starts and passed health checks
    Given server is running
    When querying the health endpoint
    Then server responds with pong