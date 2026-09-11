document.addEventListener("DOMContentLoaded", function () {

    /* ========================================
       DELETE CONFIRMATION
       ======================================== */

    const deleteForms = document.querySelectorAll(
        ".delete-form"
    );

    deleteForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const message = form.dataset.confirm;

            if (message) {

                const confirmed = confirm(message);

                if (!confirmed) {
                    event.preventDefault();
                }

            }

        });

    });


    /* ========================================
       IMAGE FILE SELECTION
       ======================================== */

    const fileInputs = document.querySelectorAll(
        'input[type="file"]'
    );

    fileInputs.forEach(function (input) {

        input.addEventListener("change", function () {

            if (input.files.length > 0) {

                const label = input.closest(
                    ".file-label"
                );

                if (label) {

                    label.childNodes[0].textContent =
                        "📷 " +
                        input.files[0].name +
                        " ";

                }

            }

        });

    });


    /* ========================================
       DARK MODE
       ======================================== */

    const themeToggle = document.getElementById(
        "theme-toggle"
    );

    function updateThemeButton() {

        if (!themeToggle) {
            return;
        }

        if (document.body.classList.contains("dark-mode")) {

            themeToggle.textContent = "☀️ Light Mode";

        } else {

            themeToggle.textContent = "🌙 Dark Mode";

        }

    }


    const savedTheme = localStorage.getItem(
        "socialconnect-theme"
    );

    if (savedTheme === "dark") {

        document.body.classList.add("dark-mode");

    }


    updateThemeButton();


    if (themeToggle) {

        themeToggle.addEventListener("click", function () {

            document.body.classList.toggle(
                "dark-mode"
            );


            if (
                document.body.classList.contains(
                    "dark-mode"
                )
            ) {

                localStorage.setItem(
                    "socialconnect-theme",
                    "dark"
                );

            } else {

                localStorage.setItem(
                    "socialconnect-theme",
                    "light"
                );

            }


            updateThemeButton();

        });

    }

    /* ========================================
       PROFILE PICTURE FILE NAME
       ======================================== */

    const profilePictureInput = document.getElementById(
        "profile-picture-input"
    );

    const profileFileText = document.getElementById(
        "profile-file-text"
    );

    if (profilePictureInput && profileFileText) {

        profilePictureInput.addEventListener(
            "change",
            function () {

                if (profilePictureInput.files.length > 0) {

                    profileFileText.textContent =
                        profilePictureInput.files[0].name;

                } else {

                    profileFileText.textContent =
                        "Change Profile Picture";

                }

            }
        );

    }

});