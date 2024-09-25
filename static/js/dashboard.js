(() => {
    const addActivityButtons = document.querySelectorAll(".activities__container__card.card--adding"),
    modal = document.querySelector(".modal--activity"),
    fileInput = document.querySelector("#image"),
    fakeButtonFile = document.querySelector(".file-button");

    if (fileInput && fakeButtonFile) {
        fakeButtonFile.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            fileInput.click();
        })
    }

    addActivityButtons && addActivityButtons.forEach(addActivityButton => {
        addActivityButton.addEventListener("click", () => {
            modal.classList.toggle("active");
        });
    }) 
})();
