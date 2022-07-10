Feature: Server APIs basic functions
  Tests whether all the APIs respond and the server is healthy

  Scenario: server starts and passed health checks
    Given server is running
    When querying the health endpoint
    Then server responds with pong

  Scenario: withdrawing 1$ returns 1$ coin
      Given server is running
      When withdrawing 1$
      Then receiving 1$ coin