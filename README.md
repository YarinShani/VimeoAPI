# VimeoAPI

In this project I've created an App in Vimeo dashboard and used the api to post a comment on a video.
I've tested the result with selenium and checked if the comment is posted correctly.

I've created a test file to test my project with pytest.<br>
To run tests just type `pytest`in the cmd.

I've also used a config file for tokens, passwords, etc. <br>
Create a .env file and add it to the root folder, the file should contain:

> token<br>
> email<br>
> password<br>
> user_name


token (valid token with the relevant scope for api requests)<br>
email and password (user credentials to log in with selenium )<br>
user_name (or partially display name to look for in the comment section)

I've created requirements.txt file with pip freeze, the libraries I've installed are: pytest, selenium, requests and decouple
I'm using Python version 3.9.6, pip version 21.3.1 and ChromeDriver version 106