# Event aggregation service
## Brief description of the system
The goal is to create a website that allows organizers to enter events and collect entries for them. Any registered user can sign up. The website should also have events search engine (with several criteria) and an API, that will allow the presentation on other pages / services

Main system features
User registration and login.

Creating and editing events by organizers (user with a special role).

Commenting on events by a logged in users.

Signing up for events.

Events search engine.

API for other websites / services that want to present events.

General Guidelines
Website development using Django and Django REST Framework as an API.

Introducing the division into models, views and controllers in the application and placing the appropriate logic in each of them.

Securing access to the application and functionality by using django.contrib.auth

Functionalities
Home page

creating the first controller and a view file

creating files with style / script definitions (bootstrap + possible own), which will be attached to each subsequent page (include)

the site should have a name, log in and sign up buttons on the top section

User registration
registration form should have:

login (email) – checking if the e-mail is correct,

password – must consist of at least 8 characters but not more than 30 characters,

name to display – the field cannot be empty or contain white space only, and the maximum length is 50 characters.

emails used for registration can be used only once.

the user should have system roles associated with it, that will cover at least two cases: the organizer and the ordinary user. Every registered person automatically gets the "standard user" role.

the password is kept in a database in a form that prevents snooping / recover

User login
login form containing login and password.

login using django.contrib.auth (to create the appropriate configuration).

after a successful logging in, the user should be redirected to a home page, where instead of the login / Sign up buttons the following information will be displayed: "Logged in as: email

Adding a new event
the event must contain at least:

title – the field cannot be empty or contain only whitespace,

date from/to – mandatory (optional checking if the value is a future date),

description – minimum 20 characters.

the event must be associated with the user who added it

Event List
on the home page, in the central part, a list of all current events should be placed

each element of the list should contain:

highlighted headline with an event title,

event date from/to,

first 50 characters of a description.

events should be sorted from the nearest.

Event search engine
at the top of the home page you should add a form containing:

text box to enter a phrase,

optional (dropdown): future, ongoing and future, all,

"search" button.

the entered phrase is to be searched in the title.

search results should be on a separate page, in the same layout as on the home page.

the search results page should also contain the search form as on the home page, and its fields should be set according to the currently selected criteria.

Detailed view of the event
a separate page on which all event features will be visible: title, dates from / to, full description.

on the home page and on the search results page link the title so that when clicked it takes you to a specific event page.

Add comments to the event
under general information about an event add a comment form.

the comment can be up to 500 characters long.

only a logged in user can add a comment.

comments should be sorted from the most recent ones.

Signing up for an event
on the event page you should add the option (button) to subscribe to it, but only for a logged in users.

if the current user is already registered, instead of the button they will see the relevant information and optionally a button to unsubscribe from the event.

next to general information about the event, put a list of all currently registered users.

API for other websites - listing of events
The API should meet the REST recommendations.

the method should return a list of all future events.

optionally, it can additionally enable filtering of returned events to a date range.

Application displaying events downloaded from the API
you need to build a second application (Django) that will consume the event API and display the list in some of its views

optional: adding in the application the possibility of filtering events to a selected date range, using the filtering on the API side

Additional tasks and extensions:
Possibility to add a picture to the event
enable adding a graphic file to the add / edit event form.

saving the uploaded file to disk or to some external cloud storage service via API or to make such a service with your own API (advanced version)

serving files for displaying in the event details (plus possibly in other places)

Editing an event
additional page, that will allow you to edit the created event.

only the owner or administrator of an event can edit it (new role for the user).

editing should appear at least on the event details page.

My events
section for the logged in users, where they can see all events (owned and participating in)

owned ones should be able to switch to editing (mechanism from the previous task).

the list should allow filtering:

role:
all
organizer
participant
when:
future
ongoing and future
past
all
date (optional):
field from
field to
Additional requirements
it is necessary to ensure an aesthetic and functional way of presenting data

data collected from users should be pre-validated