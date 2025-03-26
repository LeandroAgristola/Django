// Wait for the DOM to be fully loaded before executing the functions
document.addEventListener('DOMContentLoaded', function() {
  // Attach events to the buttons in the interface to load different views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Load the inbox view by default when the page loads
  load_mailbox('inbox');
});

// Function to show the compose new email view
function compose_email() {
  // Hide the email list and detail view, and display the compose view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear the form fields in the compose view
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Define the behavior when the compose form is submitted
  document.querySelector('#compose-form').onsubmit = function(event) {
    // Prevent the default form submission
    event.preventDefault();

    // Get the values of the form fields
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // Send a POST request to the server with the email data
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({ recipients, subject, body }),
      headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(result => {
      // Check if the email was sent successfully
      if (result.message === "Email sent successfully.") {
        alert("Email sent successfully.");
        // Load the 'sent' mailbox after sending the email
        load_mailbox('sent');
      } else {
        alert("Error sending the email: " + result.error);
      }
    })
    .catch(error => console.error("Error:", error));
  };
}

// Function to load a specific mailbox (inbox, sent, archive)
function load_mailbox(mailbox) {
  // Hide the compose and detail views, and show the email list view
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Set the title of the mailbox view
  document.querySelector('#emails-view').innerHTML = `
    <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
    <div id="emails-list"></div>
  `;

  // Fetch emails from the server for the selected mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      const emailsList = document.querySelector('#emails-list');
      emailsList.innerHTML = '';

      // Loop through each email and create an element to display it
      emails.forEach(email => {
        const emailItem = document.createElement('div');
        emailItem.className = 'email-item';

        // Mark the email as read or unread based on its status
        if (email.read) {
          emailItem.classList.add('read');
        } else {
          emailItem.classList.add('unread');
        }

        // Set the content of the email item
        emailItem.innerHTML = `
          <strong>${email.sender}</strong> - ${email.subject} 
          <span class="timestamp">${email.timestamp}</span>
        `;

        // Attach an event to open the email when clicked
        emailItem.addEventListener('click', () => view_email(email.id));
        emailsList.append(emailItem);
      });
    })
    .catch(error => console.error('Error:', error));
}

// Function to view a specific email's details
function view_email(email_id) {
  // Hide the email list and compose views, and display the email detail view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';

  // Fetch the email details from the server
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Mark the email as read if it's not already marked as read
      if (!email.read) {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({ read: true }),
          headers: { "Content-Type": "application/json" }
        });
      }

      // Set the content of the email detail view
      document.querySelector('#email-detail-view').innerHTML = `
        <h3>${email.subject}</h3>
        <p><strong>From:</strong> ${email.sender}</p>
        <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
        <p><strong>Timestamp:</strong> ${email.timestamp}</p>
        <hr>
        <p>${email.body}</p>
      `;

      // Add an archive or unarchive button if the email is not sent
      if (!email.sent) {
        const archiveButton = document.createElement('button');
        archiveButton.className = 'btn btn-secondary';
        archiveButton.innerHTML = email.archived ? 'Unarchive' : 'Archive';
        archiveButton.addEventListener('click', () => {
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({ archived: !email.archived }),
            headers: { "Content-Type": "application/json" }
          })
          .then(() => load_mailbox('inbox'));
        });
        document.querySelector('#email-detail-view').appendChild(archiveButton);
      }

      // Add a reply button that pre-fills the compose form with the email details
      const replyButton = document.createElement('button');
      replyButton.className = 'btn btn-primary ml-2';
      replyButton.innerHTML = 'Reply';
      replyButton.addEventListener('click', () => {
        compose_email();
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
        document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;
      });

      // Add a delete button to delete the email
      const deleteButton = document.createElement('button');
      deleteButton.className = 'btn btn-danger ml-2';
      deleteButton.innerHTML = 'Delete';
      deleteButton.addEventListener('click', () => {
        fetch(`/emails/${email_id}`, {
          method: 'DELETE',
          headers: { "Content-Type": "application/json" }
        })
        .then(() => load_mailbox('inbox'));
      });

      document.querySelector('#email-detail-view').append(replyButton, deleteButton);
    })
    .catch(error => console.error('Error:', error));
}
