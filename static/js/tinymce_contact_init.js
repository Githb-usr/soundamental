document.addEventListener("DOMContentLoaded", function () {
  if (typeof tinymce === "undefined") {
    console.warn("TinyMCE non chargé : script contact ignoré.");
    return;
  }

  tinymce.init({
    selector: 'textarea.richtext-contact',
    language: 'fr_FR',
    language_url: '/static/js/tinymce/langs/fr_FR.js',

    // Plugins activés
    plugins: 'image link lists code fullscreen media table',

    toolbar:
    'code | undo redo | formatselect fontselect fontsizeselect | ' +
    'bold italic underline strikethrough | forecolor backcolor | ' +
    'alignleft aligncenter alignright alignjustify | ' +
    'bullist numlist outdent indent | ' +
    'link image media table | fullscreen preview',

    menubar: false,
    statusbar: false,
    branding: false,

    // Protection : on n’autorise que les balises sûres
    valid_elements: 'a[href|target=_blank],strong/b,em/i,u,s,strike,span[style],ul,ol,li,p,br,span,' +
                    'h1,h2,h3,h4,h5,h6,table,tr,td,th,thead,tbody,tfoot,img[src|alt|title|width|height],code,pre',
    extended_valid_elements: 'u,s,strike,span[style]',
    content_css: 'default',
    formats: {
        underline: { inline: 'u' },
        strikethrough: { inline: 's' },
    }
  });
});
