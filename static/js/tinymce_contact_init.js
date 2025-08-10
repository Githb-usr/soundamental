document.addEventListener("DOMContentLoaded", function () {
  if (typeof tinymce === "undefined") {
    console.warn("TinyMCE non chargé : script contact ignoré.");
    return;
  }

  tinymce.init({
    selector: 'textarea.richtext-contact',
    language: 'fr_FR',
    language_url: '/static/js/tinymce/langs/fr_FR.js',

    // Plugins strictement nécessaires (alignés avec la whitelist serveur)
    plugins: 'autolink link lists paste',

    // Toolbar minimale (pas de code, pas d’images/médias/tables/couleurs)
    toolbar:
    'bold italic underline bullist numlist link unlink removeformat ',
    menubar: false,
    statusbar: true,
    branding: false,

    // Génération HTML propre
    forced_root_block: 'p',
    paste_as_text: true, // colle en texte brut (évite les styles Word/HTML)

    // N'autoriser que quelques balises inoffensives
    valid_elements: 'a[href],strong/b,em/i,u,ul,ol,li,p,br',
    // Bloquer explicitement les éléments indésirables
    invalid_elements: 'img,video,audio,table,tr,td,th,thead,tbody,tfoot,pre,code,iframe,style,script,span',
    
    // Pas d’options de cible ni de titre sur les liens (réduit les risques)
    link_target_list: false,
    link_title: false
  });
});
