# sherlock-django

A Django JSON REST API for [Sherlock 1.4.3](https://github.com/sherlock-project/sherlock).

<a href="https://render.com/deploy?repo=https://github.com/turian/sherlock-django">
<img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" />
</a>

## Motivation

We wrote this because [sherlock-project/api](https://github.com/sherlock-project/api) is full of gaping security holes.

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

Those are the only parameters supported. We are open to PRs adding other arguments (e.g. proxies) that sherlock supports.

## Contributing

Each and every contribution is greatly valued!

But if you love Sherlock, it's even better if you contribute to [their repo](https://github.com/sherlock-project/sherlock).

