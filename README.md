# sherlock-rest

A Django JSON REST API for [Sherlock 1.4.3](https://github.com/sherlock-project/sherlock).

## Deploy to Render for Free

<a href="https://render.com/deploy?repo=https://github.com/turian/sherlock-rest.git">
<img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" />
</a>

Note that the Render deploy is pure python, because I couldn't
figure out how to get the `render.yaml.Docker` version to work.

### Important to note:
This version of sherlock rest api has added support for some sites sherlock innnitially 
stop supporting and currently, this version only supports:
- Facebook        - Twitter      - Instagram
- Youtube Channel - Youtube User - Linktree
- Reddit          - Telegram     -Linkedin

In other to include more sites support, head over to the shelock's main directory at 
https://raw.githubusercontent.com/sherlock-project/sherlock/master/sherlock/resources/data.json, 
then search for any site you wish to support, copy the json entry for the site and include it in 
the `data.json` file located at `sherlock/resource/data.json` in this project, and make the add. 
An example json entry to support a site would look like this for `archive.org`:
```
"Archive.org": {
    "errorMsg": "cannot find account",
    "errorType": "message",
    "url": "https://archive.org/details/@{}",
    "urlMain": "https://archive.org",
    "username_claimed": "blue"
  }
 ```

To run or test this locally:
After cloning the repository, navigate to base `sherlock rest` directory and open it up in the terminal

1. Install all dependencies by running `pip install -r requirements.txt`
2. Create a `.env` file in the root directory of the project, the same directory as the `manage.py` file in the project
3. Include an entry for `DJANGO_SECRET_KEY` and `DEBUG` an example `.env` file would look like this:
 ```
 >> sherlock/.env
 DJANGO_SECRET_KEY=w90e-tu39408fjkoi0qj209ur0-qvjwi0jf2389-iq-9wf9jq0j
 DEBUG=True
```
4. Then, run `python manage.py runserver` to run the project locally.

Allowed method for requesting connection with the API is by sending a post request to `localhost:8000/api/v1/sherlock/`.
You can use postman to send this request and the request body would look something like this:
```
{
    "usernames": ["user1", "exampleuser","username"], 
    "site": ["facebook", "instagram", "linkedin"]
} 
```
If the site entry is left empty ie `"site":[]` sherlock would return an api json response of result of all supported site for each user.

Response example when it's run for an example username "USER":
```
{"result": [{"username": "user", "results": {"Twitter": {"url_main": "https://twitter.com/", "url_user": "https://twitter.com/user", "status": "Available", "http_status": 200}, "Youtube Channel": {"url_main": "https://www.youtube.com", "url_user": "https://www.youtube.com/c/user", "status": "Available", "http_status": 404}, "Facebook": {"url_main": "https://www.facebook.com/", "url_user": "https://www.facebook.com/user", "status": "Claimed", "http_status": 200}, "Youtube User": {"url_main": "https://www.youtube.com", "url_user": "https://www.youtube.com/user/user", "status": "Claimed", "http_status": 200}, "Linktree": {"url_main": "https://linktr.ee/", "url_user": "https://linktr.ee/user", "status": "Claimed", "http_status": 200}, "Reddit": {"url_main": "https://www.reddit.com/", "url_user": "https://www.reddit.com/user/user", "status": "Claimed", "http_status": 200}, "Telegram": {"url_main": "https://t.me/", "status": "Illegal", "url_user": "", "http_status": ""}, "Linkedin": {"url_main": "https://www.linkedin.com/", "url_user": "https://www.linkedin.com/in/user", "status": "Claimed", "http_status": 999}, "Instagram": {"url_main": "https://www.instagram.com/", "url_user": "https://www.instagram.com/user", "status": "Claimed", "http_status": 403}}}]}
```


## Motivation

We wrote this because [sherlock-project/api](https://github.com/sherlock-project/api) is full of gaping security holes:
* not sanitizing input to subprocess
* hard-coding the DJANGO_SECRET_KEY and never retrieving it from the environment
With that said, this API does no authentication and is open.

We had to make a few minor changes to `sherlock` to get it to work
through Django:
* Creating `sherlock.sherlock.run_sherlock` that contains
the functionality of `sherlock.sherlock.main`, which `sherlock.sherlock.main` now calls. (non-intrusive change)
* Disabling the use of `signals` in `sherlock.sherlock`, which allowed the user to gracefully Ctrl-C in an interactive environment. (an intrusive change which could be made optional)
If there is interest, we could push the changes upstream to `sherlock`
as options. We also wouldn't mind optionally disabling the super chatty colarama output of sherlock in the server logs.

We also remove some functionalities that are'nt relevant to communicatin with sherlock as a rest api, and this include:
- Removal of shelock auto creating a `.txt` file for each user a query is run on
- Removal of folder based output (cascading folders on folder)
- Removal of xml file creation output
- Removal of using the shelock's remote data.json file to list supported files.

## Contributing

Each and every contribution is greatly valued!

But if you love Sherlock, it's even better if you contribute to [their repo](https://github.com/sherlock-project/sherlock).
