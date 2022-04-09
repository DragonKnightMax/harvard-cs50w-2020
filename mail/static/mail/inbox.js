
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // listen to form submission
  const form = document.querySelector('#compose-form');
  form.addEventListener('submit', (event) => {

    // prevent default form submission
    event.preventDefault();

    // call function to send email
    send_email();
  });
});

function compose_email(reply=false, email=null) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // for replying email
  if (reply && email !== null) {

    // get the user email
    const user = document.querySelector('#user-email').innerHTML;

    // pre-fill recipients field with original email sender, subject and body
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${user} wrote: ${email.body}`;
  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // send GET request to URL
  fetch(`/emails/${mailbox}`)
  .then(response => response.json()) // put response into json
  .then(emails => {
     // iterate through emails in mailbox
    emails.forEach(element => {
      // call function to list all emails in mailbox
      list_email(element);
    })
  })
  .catch(error => {
    // catch any error and log it to console
    console.log("Error:", error);
  });
}

function send_email() {

  // retrieve form data
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send POST request to URL
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    if (result.message) {
      // log the response message to console status code 201
      console.log("Message:", result.message);

      // display Sent mailbox to User after submitting form
      load_mailbox('sent');

    } else if (result.error) {
      // log error message to console status code 400
      console.log("Error:", result.error);
    }
  });
  return false;
}

function list_email(email) {

  // retrieve email data from JSON response
  const from = email.sender;
  const subject = email.subject;
  const timestamp = email.timestamp;

  // create a div to hold email data
  var div = document.createElement("div");
  div.innerHTML = `${from}  |  ${subject}  | ${timestamp}`;

  // white for unread and gray for read email
  if (email.read) {
    div.style.backgroundColor = "#ECECEC";
  } else {
    div.style.backgroundColor = "white";
  }
  // set black border
  div.style.border = "1px solid black";

  // listen to the click on email
  div.addEventListener('click', () => {
    // show email content
    show_email(email.id);

    // mark email as read
    mark_read(email.id);

  });

  // add the div as child to the email-views block
  document.querySelector('#emails-view').append(div);
}

function show_email(email_id) {

  // Show the content and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'block';

  // send GET request to URL
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // email not found status code 404
    if (email.error) {
      console.log(email.error);
      return
    }

    // retrieve email data from json
    const from = email.sender;
    const to = email.recipients;
    const subject = email.subject;
    const body = email.body;
    const timestamp = email.timestamp;

    const user = document.querySelector('#user-email').innerHTML;
    let sent = true;

    if (from !== user) {
      sent = false;
      var archive = false;

      // choose either archive or unarchive button is displayed
      if (email.archived) {
        var archive_unarchive = "Unarchive";
      } else {
        var archive_unarchive = "Archive";
        archive = true;
      }
    }

    // create a div tag to hold email content
    const div = document.createElement("div");
    div.innerHTML = `
      <div>From: ${from}</div>
      <div>To: ${to}</div>
      <div>Subject: ${subject}</div>
      <div>Timestamp: ${timestamp}</div>
      <div id="reply-archive-button">
        <button id="email-reply">Reply</button>
      </div>
      <hr>
      <div>${body}</div>
      `;

    // listen to click on reply button
    div.querySelector('#email-reply').addEventListener('click', () => {
      // load the composition form to reply the email
      compose_email(reply=true, email=email);
    });

    // if the email is not in sent mailbox, display archive button
    if (!sent) {

      // create archive button and append it near reply button
      const archive_button = document.createElement("button");
      archive_button.id = "email-archived-unarchived";
      archive_button.innerHTML = `${archive_unarchive}`;
      div.querySelector('#reply-archive-button').append(archive_button);

      // listen to click on archive button
      div.querySelector('#email-archived-unarchived').addEventListener('click', () => {
        // call function to mark archived or unarchived
        mark_archived(email.id, archive);
      });
    }

    // clear the email content page before append
    document.querySelector('#email-content').innerHTML = '';
    document.querySelector('#email-content').append(div);
  })
}

function mark_read(email_id, read=true) {
  // send PUT request to URL
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: read,
    })
  });
}

function mark_archived(email_id, archived=true) {
  // send PUT request to URL
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archived,
    })
  })
  // ensure PUT request is completed before proceed
  .then(() => {
    // load user inbox after archived or unarchived email
    load_mailbox('inbox');
  });
}
