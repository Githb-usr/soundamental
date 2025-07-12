// Déduit data-subfolder depuis la valeur brute de la catégorie sélectionnée

document.addEventListener("DOMContentLoaded", function () {
    const categorieField = document.querySelector("#id_categorie_principale");
    const contenuField = document.querySelector("textarea.richtext");

    if (!categorieField || !contenuField) return;

    const updateSubfolder = () => {
        const value = categorieField.value || "illustrations";
        contenuField.dataset.subfolder = value;
    };

    updateSubfolder();
    categorieField.addEventListener("change", updateSubfolder);
});

