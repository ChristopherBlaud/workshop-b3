(() => {
    const modals = document.querySelectorAll(".modal"),
    activityModal = document.querySelector(".modal--activity"),
    activityJoinModal = document.querySelector(".modal--join"),
    activityModalButton = document.querySelector(".activities__container .activities__container__card.card--adding"),
    fileInput = document.querySelector("#image"),
    fileNameContainer = document.querySelector(".file-button__image-name"),
    fakeButtonFile = document.querySelector(".file-button"),
    activityCards = document.querySelectorAll(".activities__container__card:not(.card--adding)"),
    joinActivityButtons = document.querySelectorAll(".activity-informations__button-container .button--join"),
    header = document.querySelector(".header"),
    userInformationsContainer = document.querySelector(".header__user-informations"),
    userActivitiesList = document.querySelector(".header__user-informations__body");

    // Affiche les données dans la modal
    const showModalActivityInformations = (data) => {
        const container = document.querySelector(".activity-informations"),
            title = container.querySelector(".activity-informations__heading__text h2"),
            category = container.querySelector(".activity-informations__heading__text__category span"),
            description = container.querySelector(".activity-informations__body p");

            container.dataset.id = data.id;

            title.textContent = data.nom;

            category.classList.add(`${data.type}`);
            category.textContent = data.type === "physical" ? "Présentiel" : data.type === "remote" ? "À distance" : "Présentiel / À distance";

            description.textContent = data.description;
    };

    const joinActivity = async (activityID) => {
        try {
            const response = await fetch("http://127.0.0.1:5000/dashboard/join", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ activity_id: activityID})
            });

            const result = await response.json();

            if (response.ok) {
                window.location.reload();
            };
            
        } catch (error) {
            console.error(error);
        };        
    };

    // Fetch les données de l'activité dont l'id est passé en paramètre de l'url
    const getActivityInformations = async (activityID) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/dashboard/activity/${activityID}`);

            const result = await response.json();

            if (response.ok) {
                showModalActivityInformations(result);
            } else {
                console.error("Error", result)
            }

        } catch (error) {
            console.error(error);
        };
    };

    // Remplace le input file par un bouton stylisé et simule le clique dessus
    if (fileInput && fakeButtonFile) {
        fakeButtonFile.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            fileInput.click();
        });
    };

    // Ouvre et ferme les modals au clique
    modals && modals.forEach(modal => {
        const closeButton = modal.querySelector(".activities__container__card.card--adding");

        closeButton.addEventListener("click", () => {
            modal.classList.toggle("active")
        });
    });

    // Ouvre et ferme les modals au clique
    if (activityModal && activityModalButton) {
        activityModalButton.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();

            activityModal.classList.toggle("active");
        });
    };

    // Ouvre la modal des informations d'activité au clique
    activityCards && activityCards.forEach(activityCard => {
        activityCard.addEventListener("click", () => {
            const activityID = activityCard.dataset.id;

            activityID && getActivityInformations(activityID);
            activityJoinModal.classList.add("active");
        })
    });

    joinActivityButtons && joinActivityButtons.forEach(joinActivityButton => {
        
        joinActivityButton.addEventListener("click", () => {
            const activityID = Number(joinActivityButton.closest(".activity-informations").dataset.id);

            joinActivity(activityID);
        })
    })

    // Affiche le nom du fichier image
    fileInput.addEventListener("change", (e) => fileNameContainer.textContent = e.target.files[0].name);

    // Modifie le layout du header sur mobile
    window.innerWidth <= 768 && header.appendChild(userActivitiesList);

    window.addEventListener("resize", () => {
        if (window.innerWidth <= 768) {
            header.appendChild(userActivitiesList);
        } else {
            userInformationsContainer.appendChild(userActivitiesList)
        }
    })
})();