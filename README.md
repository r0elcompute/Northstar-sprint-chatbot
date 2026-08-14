##Northstar Sprint Chatbot
A support Deflection MVP chatbot built for Northsta Retail Co. The bot handles common customer support request automatically, reducing the number of tickets that need a human agent.
##Core capability of the project
The chatbot handles three key customers questions
**Stock availability**-informs customers if an item is in stock.
**Order status**-Checking where a customers order is
**Return & refunds**-helping customers understand or start a return
##Project Structure
'config/'-app configuration and setting
'docs/'-project documentation
'support/'-core chatbot logic(stock checks, returns, order status)
'init-db. py'-sets up the database
'seed. py'-loads sample/test data into the database
'manage. py' - project management script
'requirements. txt'-list of python packages needed to run the project
##Tech Stack
Backend:Python
Database: MySQL(hosted on Railway)
Frontend:HTML
API:Rest endpoint at 'Post /api/v1/chat/'
##team
Backend:Rodgers Fanuel
Frontend: Constance Mukenyi
AI automation:Christine Wanja
Database: Rachael Hinga
Integration, QA &Documentation: Didymus Kiai
## Getting Started
Clone the repository
Install dependencies: 'pip install -requirements. txt'
Set up the database :'python init_db. py'
Load sample data: 'python seed. py'
##Status
This is an active mvp built as part of PLP project lool at 'GO-LIVE.md' for current known issue and what's left to do before launch
