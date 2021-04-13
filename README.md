# WORKOUT! Web-App
#### Video Demo: https://youtu.be/xHBzPLzAve8
#### Description:

This is a web-application with features such as,
BMI & Waist-Hip-ratio calculator to let users have some insight into their health status,
IntervalTimer for HIIT, Tabata and whatnot,
Stopwatch to keep track of time elapsed, AND
Workout plans which enable users to personalise.

The web-app is loosely based on CS50 Finance in terms of the use of Flask and some idea of styling.




**The Registering and Loging In**

The users are required to create at least a 8 characters password with letters and numbers only and at least a number.
The checking of inputs and password are done on the client-side, only the username is checked from database after submitted.


**The Home**

Home page can be redirected when the "WORKOUT!" is clicked. Both calculators stay here.

**The Interval Timer**

The users first set the duration, break and repetition. Essentially, the timer is ran with `setInterval()` methods in Javascript.
When the workout is completed, the workout info is sent to database through url.


**The Stopwatch**

When the workout is saved, the workout info is sent to database through url.


**The Workout Plan**

When a existing plan is choosen, the user is redirected to start.html.
When the workout is completed, the workout info is sent to database through url.

When the user chooses to create new plan, the user is redirected to createPlan.html, user could search for workout with asynchronous search bar and select dropdown for catogeries.
The user could adds, deletes, sets duration and break time to create a new plan. Besides, there is also feature for user to add new workout for more workout options when redirected to addExercise.html.


**The History**

Show users their workout history.




**Room for Improvement**
1. Publish in Heroku.
2. Sound effects, BGM and short description for workout
3. Back button for create plan and add exercise
