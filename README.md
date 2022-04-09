# CS50W-Project2-Commerce

Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Technologies Used

* [Django](https://www.djangoproject.com/)

## Installation

1. Clone the repo

   ```bash
   git clone https://github.com/DragonKnightMax/CS50W-Commerce.git
   ```

2. Create and activate python virtual environment

    ```bash
    python -m venv venv
    venv/Scripts/activate
    ```

3. Install all dependencies.

    ```bash
    pip install -r requirements.txt
    ```

4. Perform database migration

    ```bash
    python manage.py check
    python manage.py migrate
    ```

5. Run Development Server

    ```bash
    python manage.py runserver
    ```

## Usage

## Specification

* [X] **Models**: Your application should have at least three models in addition to the `User` model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.

* [X] **Create Listing**: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

* [X] **Active Listings Page**: The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).

* [X]Listing Page: Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
  * If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.
  * If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
  * If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
  * If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
  * Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.

* [X] **Watchlist**: Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.

* [X] **Categories**: Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

* [X] **Django Admin Interface**: Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Acknowledgments

* [Auto-create primary key used when not defining a primary key type warning in Django](https://stackoverflow.com/questions/66971594/auto-create-primary-key-used-when-not-defining-a-primary-key-type-warning-in-dja)

* [](https://stackoverflow.com/questions/32098797/how-can-i-check-database-connection-to-mysql-in-django)

* [Use SQLite for Django locally and Postgres on server](https://stackoverflow.com/questions/40687373/use-sqlite-for-django-locally-and-postgres-on-server)

* [Deploying Django App on Heroku with Postgres as Backend](https://medium.com/@hdsingh13/deploying-django-app-on-heroku-with-postgres-as-backend-b2f3194e8a43)

* [Deploying Django to Heroku: Connecting Heroku Postgres](https://bennettgarner.medium.com/deploying-django-to-heroku-connecting-heroku-postgres-fcc960d290d1)

* [CS50’s Web Programming with Python and JavaScript 2020 (Project 2: Commerce)](https://cs50.harvard.edu/web/2020/projects/2/commerce/)
