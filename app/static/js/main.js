// add form-control class to all input elements within ul elements with the class form-control
document.addEventListener("DOMContentLoaded", function() {
    const formControlLists = document.querySelectorAll("ul.form-control");
    
    formControlLists.forEach(function(ul) {
        const inputs = ul.querySelectorAll("input");
        
        inputs.forEach(function(input) {
            input.classList.add("form-control");
        });
    });
});