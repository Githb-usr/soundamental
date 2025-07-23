document.addEventListener("DOMContentLoaded", function () {
  // Vérifie que TinyMCE est bien chargé
  if (typeof tinymce === "undefined") {
    console.warn("TinyMCE non chargé : richtext_init.js ignoré.");
    return;
  }

  // Initialisation de TinyMCE avec la configuration ADMIN
  tinymce.init({
    selector: '#id_contenu, textarea.richtext', // Cible les champs de contenu enrichi
    language: 'fr_FR',
    language_url: '/static/js/tinymce/langs/fr_FR.js',
    height: 400,
    width: '100%',
    plugins: [
      'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview', 'anchor',
      'searchreplace', 'visualblocks', 'code', 'fullscreen', 'insertdatetime', 'media',
      'table', 'help', 'wordcount'
    ],
    toolbar:
      'undo redo | formatselect fontselect fontsizeselect | ' +
      'bold italic underline strikethrough | forecolor backcolor | ' +
      'alignleft aligncenter alignright alignjustify | ' +
      'bullist numlist outdent indent | ' +
      'link image media table | browseImage uploadImageFromSite | code fullscreen preview',
    menubar: 'file edit view insert format tools table help',
    statusbar: true,
    content_style: "body { font-family: Arial,Helvetica,sans-serif; font-size:14px }",
    fontsize_formats: "8pt 10pt 12pt 14pt 16pt 18pt 24pt 36pt 48pt",
    valid_elements:
      "p,br,ul,ol,li,div,span[style],b,strong,i,em,u,sup,sub," +
      "h1,h2,h3,h4,h5,h6,blockquote,pre,code," +
      "a[href|title|target|rel]," +
      "img[src|alt|title|width|height|style]," +
      "table,tr,td,th,thead,tbody,tfoot," +
      "hr",
    extended_valid_elements:
      "a[href|title|target|rel],img[src|alt|title|width|height|style],span[style],div[style]",
    valid_styles: {
      '*': 'float,width,height,margin,margin-top,margin-bottom,margin-left,margin-right,padding,padding-top,padding-bottom,padding-left,padding-right,display,border,border-radius,background,background-color,background-image,text-align,vertical-align,position,top,left,right,bottom,font-size,font-family,color',
    },

    // Upload d’image par copier/coller ou glisser-déposer
    images_upload_url: "/medias/upload/blog/",
    automatic_uploads: true,
    file_picker_types: 'image',

    // Upload d’image via le bouton "Parcourir" ou sélection manuelle
    file_picker_callback: function (callback, value, meta) {
      if (meta.filetype === 'image') {
        const input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');

        input.onchange = function () {
          const file = this.files[0];
          const formData = new FormData();
          formData.append('image', file);

          // Récupération dynamique du sous-dossier depuis le champ actif
          const activeEditor = tinymce.activeEditor;
          const textarea = activeEditor?.getElement();
          const sousDossier = textarea?.dataset?.subfolder || 'autres';

          formData.append('subfolder', sousDossier);

          // Récupération du token CSRF
          const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

          fetch('/medias/site/', {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrfToken,
            },
            body: formData
          })
            .then(response => response.json())
            .then(data => {
              callback(data.location);
            })
            .catch(() => {
              alert("Échec de l’upload.");
            });
        };

        input.click();
      }
    },

    // Boutons custom pour images
    setup: function (editor) {
      editor.ui.registry.addButton('browseImage', {
        text: 'Insérer img bibliothèque',
        icon: 'browse',
        onAction: function () {
          window.open(
            '/medias/insert/',
            'ImageBrowser',
            'width=900,height=600,resizable=yes,scrollbars=yes'
          );
        }
      });

      editor.ui.registry.addButton('uploadImageFromSite', {
        text: 'Uploader une image',
        icon: 'upload',
        onAction: function () {
          const textarea = editor.getElement();
          const section = textarea?.dataset?.section || 'site';
          window.open(
            `/medias/${section}/upload/`,
            'ImageUploader',
            'width=600,height=400,resizable=yes,scrollbars=yes'
          );
        }
      });

      editor.on('change', function () {
        editor.save();
      });
    }
  });
});
