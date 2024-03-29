# Project Readme

## UPDATE:
An updated version can be seen live at:
[Basic python bookmarking/URI shortening server](https://shortyuri.herokuapp.com/)

## This back-end project should meet the following requirements:

* On a GET request to the / path, it displays an HTML form with two fields. One field is where you put the long URI you want to shorten. The other is where you put the short name you want to use for it. Submitting this form sends a POST to the server. 

* On a POST request, the server looks for the two form fields in the request body. If it has those, it first checks the URI with requests.get to make sure that it actually exists (returns a 200). 

  * If the URI exists, the server stores a dictionary entry mapping the short name to the long URI, and returns an HTML page with a link to the short version.

  * If the URI doesn't actually exist, the server returns a 404 error page saying so. -----**UPDGRADED**----

  * If either of the two form fields is missing, the server returns a 400 error page saying so. -----**UPGRADED**----

* On a GET request to an existing short URI, it looks up the corresponding long URI and serves a redirect to it.
