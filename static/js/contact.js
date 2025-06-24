// document.getElementById('contactForm').addEventListener('submit', function(event) {
//     event.preventDefault();

//     const name = document.getElementById('name').value;
//     const email = document.getElementById('email').value;
//     const message = document.getElementById('message').value;

//     if (name && email && message) {
//         alert(`Thank you, ${name}! Your message has been sent successfully.`);
//         document.getElementById('contactForm').reset();
//     } else {
//         alert('Please fill out all fields before submitting.');
//     }
// });


document.getElementById('contactForm').addEventListener('submit', function(event) {
    // Remove this line to allow the form to submit
    // event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    if (name && email && message) {
        // You can still show the alert before submitting
        alert(`Thank you, ${name}! Your message has been sent successfully.`);
        // Form will automatically submit now
    } else {
        alert('Please fill out all fields before submitting.');
        event.preventDefault(); // Only prevent if fields are empty
    }
});
