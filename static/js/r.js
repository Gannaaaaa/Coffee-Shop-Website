document.addEventListener('DOMContentLoaded', () => {
    const boxes = document.querySelectorAll('.products-container .box');
    
    boxes.forEach(box => {
        box.addEventListener('mouseover', () => {
            box.classList.add('hover');
        });
        
        box.addEventListener('mouseout', () => {
            box.classList.remove('hover');
        });
    });
});

document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', (event) => {
        event.preventDefault();
        alert('Item added to cart!');
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const headings = document.querySelectorAll('.heading');
    
    headings.forEach(heading => {
        heading.addEventListener('mouseover', () => {
            heading.classList.add('hover');
        });
        
        heading.addEventListener('mouseout', () => {
            heading.classList.remove('hover');
        });
    });
});