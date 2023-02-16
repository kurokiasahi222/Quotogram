(function (window, document) {
    var menu = document.querySelector('.navigation-wrapper'),
        rollback,
        WINDOW_CHANGE_EVENT = ('onorientationchange' in window) ? 'orientationchange':'resize';

    function toggleHorizontal() {
        menu.classList.remove('closing');
        [].forEach.call(
            document.querySelector('.navigation-wrapper').querySelectorAll('.custom-can-transform'),
            function(el){
                el.classList.toggle('pure-menu-horizontal');
            }
        );
    };

    function toggleMenu() {
        // set timeout so that the panel has a chance to roll up
        // before the menu switches states
        if (menu.classList.contains('open')) {
            menu.classList.add('closing');
            rollBack = setTimeout(toggleHorizontal, 500);
        }
        else {
            if (menu.classList.contains('closing')) {
                clearTimeout(rollBack);
            } else {
                toggleHorizontal();
            }
        }
        menu.classList.toggle('open');
        document.querySelector('.navigation-custom-toggle').classList.toggle('x');
    };

    function closeMenu() {
        if (menu.classList.contains('open')) {
            toggleMenu();
        }
    }

    document.querySelector('.navigation-custom-toggle').addEventListener('click', function (e) {
        toggleMenu();
        e.preventDefault();
    });

    window.addEventListener(WINDOW_CHANGE_EVENT, closeMenu);
    })(this, this.document);
