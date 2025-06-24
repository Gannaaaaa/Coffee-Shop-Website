document.addEventListener("DOMContentLoaded", function() {

    const landingText = document.querySelector(".landing .text");

    
    landingText.style.opacity = 0;
    landingText.style.transition = "opacity 2s ease-out";

    
    setTimeout(() => {
        landingText.style.opacity = 1;
    }, 100);
});










