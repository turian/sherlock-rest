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

## Testing locally

```
# clone the repo
git clone https://github.com/sherlock-project/sherlock.git

# create a secret key
export DJANGO_SECRET_KEY=`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

# build the docker image
docker build -t mysherlock-rest-image .

# run docker in debug mode
docker run -p 8000:8000 --rm -t -e DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY -e DJANGO_DEBUG=True mysherlock-rest-image
```

You can now query it as follows:
```
curl -X POST -H "Content-Type: application/json" -d '{"usernames": ["user1", "user2"], "site": ["reddit", "twitter"]}' http://localhost:8000/api/v1/sherlock/
```

Those are the only parameters supported.

Although you can batch the usernames and sites queried, we recommend
doing them one at a time so you can progressively load the results.

We are open to PRs adding other arguments (e.g. proxies) that sherlock supports.

Output:
```
{"result": [{"username": "user1", "results": {"Reddit": {"url_main": "https://www.reddit.com/", "url_user": "https://www.reddit.com/user/user1", "status": "Claimed", "http_status": 200}, "Twitter": {"url_main": "https://twitter.com/", "url_user": "https://twitter.com/user1", "status": "Claimed", "http_status": 200}}}, {"username": "user2", "results": {"Reddit": {"url_main": "https://www.reddit.com/", "url_user": "https://www.reddit.com/user/user2", "status": "Claimed", "http_status": 200}, "Twitter": {"url_main": "https://twitter.com/", "url_user": "https://twitter.com/user2", "status": "Claimed", "http_status": 200}}}]}⏎
```
We strip the full `response_text` because YAGNI.

## Contributing

Each and every contribution is greatly valued!

But if you love Sherlock, it's even better if you contribute to [their repo](https://github.com/sherlock-project/sherlock).
