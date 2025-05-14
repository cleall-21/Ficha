document.addEventListener('DOMContentLoaded', function () {
    var tabs = document.querySelectorAll('.nav-link');
    var tabContents = document.querySelectorAll('.tab-pane');

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function (event) {
            event.preventDefault();
            var target = document.querySelector(tab.getAttribute('href'));

            tabs.forEach(function (item) {
                item.classList.remove('active');
            });

            tabContents.forEach(function (content) {
                content.classList.remove('active');
            });

            tab.classList.add('active');
            target.classList.add('active');
        });
    });
});
