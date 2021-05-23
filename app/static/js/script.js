//scroll

window.addEventListener("scroll", function() {
    var ele = document.querySelector(".cd-header");
    ele.classList.toggle("sticky", window.scrollY > 0);
})

//nav

var app = function() {
    var body = undefined;
    var menu = undefined;
    var menuItems = undefined;

    var init = function init() {
        body = document.querySelector('body');
        menu = document.querySelector('.menu-icon');
        menuItems = document.querySelectorAll('.nav__list-item');
        applyListeners();
    };

    var applyListeners = function applyListeners() {
        menu.addEventListener('click', function() {
            return toggleClass(body, 'nav-active');
        });
    };


    var toggleClass = function toggleClass(element, stringClass) {
        if (element.classList.contains(stringClass)) element.classList.remove(stringClass);
        else element.classList.add(stringClass);
    };
    init();
}();


//accordion
var acc = document.getElementsByClassName('accordion');
for (var i = 0; i < acc.length; i++) {

    acc[i].addEventListener('click', function() {

        this.classList.toggle('open');
        var panel = this.nextElementSibling;
        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
        } else {
            panel.style.maxHeight = panel.scrollHeight + 'px';
        }

    })
}