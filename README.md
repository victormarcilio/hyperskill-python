# Hyperskill - python
This repository contains some of the assignments from Hyperskill's python courses

### [Simple Banking System](https://hyperskill.org/projects/109?track=30)
- A simple project to manage credit card accounts. The user can ask for creation of a new account, and log in to an existing account;
- Once logged in he has the option check the balance, add money, transfer money or close the account.
- Sqlite3 was used for persistence.
- Input validation not very picky (assumed that user will input integers and valid options for menus)
    - It validates card numbers with luhn's algorithm;
    - Checks if the account to receiver the transfer exists;
    - Checks if the receiving account is not the same that is doing the transfer;
    - Checks if the transfering account has enough funds for that.

### [Food Blog Backend](https://hyperskill.org/projects/167?track=30)
- A project that mixes SQL (SQLite3) and some python data structures and libraries
- SQL concepts/commands used:
    - TABLE CREATION
    - INSERT
    - SELECT
    - PRIMARY KEYS
    - FOREIGN KEYS
    - WHERE, LIKE, IN
    - JOIN
    - GROUP BY, HAVING
    - COUNT(*)
    
