# CS50W-Project0-Wiki

Design a Wikipedia-like online encyclopedia.

## Technologies

* [Django](https://www.djangoproject.com/)

## Installation & Setup

1. Clone the repo
  
```shell
git clone https://github.com/DragonKnightMax/CS50W-Wiki.git
```

2. Create and activate python virtual environment

```bash
python -m venv venv
venv/Scripts/activate
```

3. Install all dependencies.

```shell
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

Heroku Local

```shell
heroku local -f Procfile.windows
heroku local -e .env
heroku local -p 7000. If you don’t specify a port, 5000 is used.
```

## Specification

* [X] **Entry Page**: Visiting `/wiki/TITLE`, where `TITLE` is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
  * The view should get the content of the encyclopedia entry by calling the appropriate util function.
  * If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
  * If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.

* [X] **Index Page**: Update `index.html` such that, instead of merely listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page.

* [X] **Search**: Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
  * If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
  * If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were ytho, then Python should appear in the search results.
  * Clicking on any of the entry names on the search results page should take the user to that entry’s page.

* [X] **New Page**: Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.
  * Users should be able to enter a title for the page and, in a `textarea`, should be able to enter the Markdown content for the page.
  * Users should be able to click a button to save their new page.
  * When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
  * Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.

* [X] **Edit Page**: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
  * The `textarea` should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the `textarea`).
  * The user should be able to click a button to save the changes made to the entry.
  Once the entry is saved, the user should be redirected back to that entry’s page.

* [X] **Random Page**: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.

* [X] **Markdown to HTML Conversion**: On each entry’s page, any Markdown content in the entry file should be converted to HTML before being displayed to the user. You may use the `python-markdown2` package to perform this conversion, installable via `pip3 install markdown2`.
  * Challenge for those more comfortable: If you’re feeling more comfortable, try implementing the Markdown to HTML conversion without using any external libraries, supporting headings, boldface text, unordered lists, links, and paragraphs. You may find using regular expressions in Python helpful.

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

* [CS50’s Web Programming with Python and JavaScript 2020 (Project 1: Wiki)](https://cs50.harvard.edu/web/2020/projects/1/wiki/)

* [Django Favicon Setup (including Admin)](https://automationpanda.com/2017/12/17/django-favicon-setup-including-admin/)

* [Hosting a Django Project on Heroku](https://realpython.com/django-hosting-on-heroku/)

* [Django static files cannot find the path specified](https://stackoverflow.com/questions/63595840/django-static-files-cannot-find-the-path-specified)

* [How can I get a favicon to show up in my django app?](https://stackoverflow.com/questions/21938028/how-can-i-get-a-favicon-to-show-up-in-my-django-app)

* [Django SECRET_KEY protection VS allow anyone to run project locally](https://stackoverflow.com/questions/69506915/django-secret-key-protection-vs-allow-anyone-to-run-project-locally)
