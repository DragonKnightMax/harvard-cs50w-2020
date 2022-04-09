# CS50W-Mail

Design a front-end for an email client that makes API calls to send and receive emails.

## Installation

1. Clone the repo

   ```bash
   git clone https://github.com/DragonKnightMax/CS50W-Mail.git
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

## Specification

- [X] **Send Mail**: When a user submits the email composition form, add JavaScript code to actually send the email.

- You’ll likely want to make a POST request to /emails, passing in values for recipients, subject, and body.
- Once the email has been sent, load the user’s sent mailbox.

- [X] **Mailbox**: When a user visits their Inbox, Sent mailbox, or Archive, load the appropriate mailbox.

- You’ll likely want to make a GET request to `/emails/<mailbox>` to request the emails for a particular mailbox.
- When a mailbox is visited, the application should first query the API for the latest emails in that mailbox.
- When a mailbox is visited, the name of the mailbox should appear at the top of the page (this part is done for you).
- Each email should then be rendered in its own box (e.g. as a `<div>` with a border) that displays who the email is from, what the subject line is, and the timestamp of the email.
- If the email is unread, it should appear with a white background. If the email has been read, it should appear with a gray background.

- [X] **View Email**: When a user clicks on an email, the user should be taken to a view where they see the content of that email.

- You’ll likely want to make a GET request to `/emails/<email_id>` to request the email.
- Your application should show the email’s sender, recipients, subject, timestamp, and body.
- You’ll likely want to add an additional `div` to `inbox.html` (in addition to emails-view and compose-view) for displaying the email. Be sure to update your code to hide and show the right views when navigation options are clicked.  
- Once the email has been clicked on, you should mark the email as read. Recall that you can send a `PUT` request to `/emails/<email_id>` to update whether an email is read or not.

- [X] **Archive and Unarchive**: Allow users to archive and unarchive emails that they have received.

- When viewing an Inbox email, the user should be presented with a button that lets them archive the email. When viewing an Archive email, the user should be presented with a button that lets them unarchive the email. This requirement does not apply to emails in the Sent mailbox.
- Recall that you can send a `PUT` request to `/emails/<email_id>` to mark an email as archived or unarchived.
- Once an email has been archived or unarchived, load the user’s inbox.

- [X] **Reply**: Allow users to reply to an email.

- When viewing an email, the user should be presented with a “Reply” button that lets them reply to the email.
- When the user clicks the “Reply” button, they should be taken to the email composition form.
- Pre-fill the composition form with the recipient field set to whoever sent the original email.
- Pre-fill the `subject` line. If the original email had a subject line of `foo`, the new subject line should be `Re: foo`. (If the subject line already begins with `Re: `, no need to add it again.)
- Pre-fill the `body` of the email with a line like `"On Jan 1 2020, 12:00 AM foo@example.com wrote:"` followed by the original text of the email.

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

- [CS50’s Web Programming with Python and JavaScript 2020 (Project 3: Mail)](https://cs50.harvard.edu/web/2020/projects/3/mail/)
