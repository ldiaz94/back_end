# Project Readme

## This back-end project should meet the following requirements:

* On a GET request to the / path, it displays an HTML form with two fields. One field is where you put the long URI you want to shorten. The other is where you put the short name you want to use for it. Submitting this form sends a POST to the server. -----**PENDING**----

* On a POST request, the server looks for the two form fields in the request body. If it has those, it first checks the URI with requests.get to make sure that it actually exists (returns a 200). -----**PENDING**----

  * If the URI exists, the server stores a dictionary entry mapping the short name to the long URI, and returns an HTML page with a link to the short version. -----**PENDING**----

  * If the URI doesn't actually exist, the server returns a 404 error page saying so. -----**PENDING**----

  * If either of the two form fields is missing, the server returns a 400 error page saying so. -----**PENDING**----

* On a GET request to an existing short URI, it looks up the corresponding long URI and serves a redirect to it. -----**PENDING**----