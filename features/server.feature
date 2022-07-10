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

Scenario: withdrawing 20$ should return bills
  Given server is running
  When withdrawing 20$
  Then receiving 20$ bill

  Scenario: withdrawing more money than loaded
    Given server is running
    And is loaded with 1000$
    When withdrawing 1200$
    Then error 409 and max amount is returned

    Scenario: withdrawing with too small decimal will be floored
      Given server is running
      When withdrawing 20.00001$
      Then receiving 20$ bill

      Scenario: withdrawing is limited to 2000$
        Given server is running
        When withdrawing 3000$
        Then receiving only 2000$