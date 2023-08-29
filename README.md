# World Of Humour App
#### Video Demo:  https://youtu.be/0RYcQ4_ow24
#### Description:A Personalized Web App returning jokes to the user

My idea was to help a bit with the long hours in coding, instead of going to social media for a quick distraction, I wanted to build something that didn't distact you in a way that its difficult to get back into your code space.

So I developed WORLD OF HUMOUR.

A web based app that return jokes and allows you to create a profile and adjusts according to certain details you entered, like gender and age. This web app enables you to select the categories of joke you want to receive, aswell as give you the option to choose restrictions on topics that should be avoided.


1 **LOGON PAGE**
The logon page is really simple. It creates an effect of unlocking the app and take you to the login page.

2 **LOGIN PAGE**
The login page consists of a form that animates into the viewport and give you an option to click the "Register Button" and go the register route.
The form has an action of post and goes the login route. The details entered here will be verified against the data in the database and will deny you access to the home page if you entered it incorrectly.

 3 **REGISTER PAGE**
The register page consists of a form where you will be filling in your details into the given fields. 
The data will be entered into a database after the "Resister" button is clicked and you will be taken to the login screen.

4 **INDEX PAGE**
Index page consists of a welcoming message and a header where you can click or hover on, to see a "Create Profile" button where you will be given the opportunity to create a profile.

5 **PROFILE PAGE**
Here you can enter the rest of your details and also add a profile picture that will show on your profile through out when your are using the app. 
Depending on the gender and age entered, the home screen and options to access certain topics will vary.

6 **HOME18 PAGE**
This page is for the younger audience. It defaults to hiding the options to access certain topics of jokes for example sexist, religious ect.
The background will also vary on the gender entered for example a male will have a different background image compared to a female.
This page consists of a few div boxes with some check boxes that can be selected and which values are passed to a function upon when the "Get Joke" button is pressed.
Here you will be able to select the categories of jokes you want to receive aswell as the ones that should be avoided. 
You can also choose different types of jokes, for example "two-part" or "single".

7 **HOME18+ PAGE**
This page is similiar than the HOME18 page except that this page has a few extra options because of the fact that you will be shown this page after entering an age above 18 years. Again the background will vary depending on the gender entered aswell.
The pages consists of a few div boxes with check boxes whose values are passed to a function when the "Get Joke" button is pressed.
Here you will be able to select the categories of jokes you want to receive, aswell as the ones that should be avoided. 
You can also choose different types of jokes example "twopart" or "single".

8 **JOKEHOME PAGE**
This page will display to you the two-part jokes. The values passed to the function via the check boxes will query the API and be diplayed in div boxes with a "Refresh" button beneath them, will still have the same background that was assigned according to the age and gender values.

9 **JOKEHOME1 PAGE**
This page will display to you the single jokes. The values passed to the function via the checkboxes will query the API and be diplayed in div boxes with a "Refresh" button beneath them and you will still have the same background that was asigned according to the age and gender values.

10 **LAY-OUT TEMPLATE**
This page just contains the structure and all the imported libraries and styling that was used in this Web App.

11 **STYLE.CSS**
This is just the styling for the web app to make it responsive and presentable. I used media queries to ensure all the elements align correctly when the screen sizes differ.
There are also a few animations that was used to make elements animate into the viewport.

12 **UPLOADS**
This file is where all the uploaded profile photos will be stored, opened and read as binary to insert it into the database.

13 **APP.PY**
This file is where all the functions are defined that will be followed when certain routes are accessed during the use of the app.
This file will also query the API, store your user id into a session variable and contain all the other logic and back-end libraries needed to make the Web-App.

This file will also be responsible to insert the data entered into the database using Sqlite3.
Because of the Web App and some image files being really large, this file will also contain a compress function where some contents will be compressed when it is larger than a certain size.
The rest is just sanitizing the data entered and validating correctnes of the data entered and return an output according to that.
This file also encodes the image files that will be queried form the database in binary format and then passed through Jinja to the template where it will be decoded and rendered.

**USERDATA.DB**
A database where the information will be stored that was entered. It consists of a few rows, one of them BLOB format, some TEXT format and the rest INTEGER formats, to store the uploaded image and the rest of the entered details.
