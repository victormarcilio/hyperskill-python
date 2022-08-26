# Hyperskill - python
This repository contains some of the assignments from Hyperskill's python courses

### [Simple Banking System](https://hyperskill.org/projects/109)
- A simple project to manage credit card accounts. The user can ask for creation of a new account, and log in to an existing account;
- Once logged in he has the option check the balance, add money, transfer money or close the account.
- Sqlite3 was used for persistence.
- Input validation not very picky (assumed that user will input integers and valid options for menus)
    - It validates card numbers with luhn's algorithm;
    - Checks if the account to receiver the transfer exists;
    - Checks if the receiving account is not the same that is doing the transfer;
    - Checks if the transfering account has enough funds for that.

### [Food Blog Backend](https://hyperskill.org/projects/167)
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
    
### [Dominoes](https://hyperskill.org/projects/146)
- A domino Game to be played against a simple AI bot
- In each turn it will be presented the current status of the game and the player's hand
    - On player's turn he will asked to select a piece to play:
        - Negative numbers will put the desired card on the left side (If the move is valid)
        - Positive numbers will put the desired card on the right side (If the move is valid)
        - 0 will take one piece from the stock (If any available)
    - On AI's turn, the player will be informed of the status and asked to press ENTER to see the AI's next move.
- 3 Possible outcomes are considered:
    - Win, if player empties his hand
    - Loss, if AI empties its hand
    - Draw, if both player and AI still have pieces in their hands and there are no more moves available

### [To-Do List](https://hyperskill.org/projects/105)
- A simple application that uses Sqlalchemy to keep track of tasks and provides the following functionalities:
    - List Current day's tasks
    - List Week's tasks
    - List all tasks
    - List missed tasks
    - Add new task
    - Delete task  
