# Django web app with PostgreSQL and vanilla frontend [Portfolio project]

## A fully functional Django web app for booking bus tickets

This project is a ticket purchase system for an imaginary bus business in Spain. In the web app, users can create a profile and book tickets for travels along the country. Some areas are enabled to make these transactions, as well as areas where you can manage your tickets, passes or personal information.

The necesary information for the creation of the travels, as well as user information, is stored in a PostgreSQL database.

## How to install
If you want to take a closer look at the project follow this steps.

1. Clone this repository.
2. Set up a virtual environment and install the dependencies running `pip install -r requirements.txt`.
3. Create an empty PostgreSQL database and connect it to the project in `mysite/mysite/settings.py`. If you are not used to Django, you can follow [this guide](https://docs.djangoproject.com/en/5.1/ref/databases/#postgresql-connection-settings).
4. Go to `mysite/` folder and run `python3 manage.py migrate` to generate all the necessary models in the datebase.

After a successful install, you can iniciate the developer server running `python3 manage.py runserver`. In adition, I recommend you to [create an admin user](https://docs.djangoproject.com/en/5.1/intro/tutorial02/#creating-an-admin-user) and play with the database.

## Find a bug?
If you found a issue or would like to make a suggestion, please use the issues section in the repository. You can also send me an email to pablogmdsoftware@gmail.com adding "Bus system issue" to the subject.