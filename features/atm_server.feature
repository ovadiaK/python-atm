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
    When withdrawing 2200$
    Then receiving only 2000$

  Scenario: too many coins will throw exception
    Given server is running
    And no bills left
    When withdrawing all coins
    Then too many coins exception is thrown

  Scenario: refill api responds with status 200
    Given server is running
    When refilling 20$ bill
    Then server responds with 200 status ok


Scenario: refill api can refill the atm money
  Given server is running
  And no bills left
  When refilling 20$ bill
  When withdrawing 20$
  Then receiving 20$ bill


  Scenario: refill empty atm with coins
    Given server is running
    And atm has only change left
    When refilling 4 5$ coins
    When withdrawing 20$
    Then receiving 4 5$ coins

    Scenario: refill with invalid bill
      Given server is running
      When refilling 250$ bill
      Then server responds with 400

  Scenario: refill with invalid coin
    Given server is running
    When refilling with 6$ coin
    Then server responds with 400