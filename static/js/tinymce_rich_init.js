document.addEventListener("DOMContentLoaded", function () {
  // Vérifie que TinyMCE est bien chargé
  if (typeof tinymce === "undefined") {
    console.warn("TinyMCE non chargé : richtext_init.js ignoré.");
    return;
  }

  // Initialisation de TinyMCE avec configuration complète
  tinymce.init({
    selector: '#id_contenu, textarea.richtext',  // Cible les champs de contenu enrichi
    language: 'fr_FR',
    height: 400,
    width: '100%',
    plugins: [
      'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview', 'anchor',
      'searchreplace', 'visualblocks', 'code', 'fullscreen', 'insertdatetime', 'media',
      'table', 'code', 'help', 'wordcount'
    ],
    toolbar:
    'undo redo | formatselect fontselect fontsizeselect | ' +
    'bold italic underline strikethrough | forecolor backcolor | ' +
    'alignleft aligncenter alignright alignjustify | ' +
    'bullist numlist outdent indent | ' +
    'link image media table | browseImage uploadImageGeneric | code fullscreen preview',
    menubar: 'file edit view insert format tools table help',
    statusbar: true,

    // Upload d’image par copier/coller ou glisser-déposer
    images_upload_url: "/medias/upload/blog/",  // URL vers la vue Django d’upload mutualisé
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
          formData.append('image', file);  // Fichier image à uploader
    
          // Récupération dynamique du sous-dossier depuis le champ actif
          const activeEditor = tinymce.activeEditor;
          const textarea = activeEditor?.getElement();
          const sousDossier = textarea?.dataset?.subfolder || 'autres';  // dossier fallback
    
          formData.append('subfolder', sousDossier);
    
          // Récupération du token CSRF
          const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
          // Envoi au backend Django
          fetch('/medias/site/', {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrfToken,
            },
            body: formData
          })
          .then(response => response.json())
          .then(data => {
            // Insère l’URL dans le contenu
            callback(data.location);
          })
          .catch(() => {
            alert("Échec de l’upload.");
          });
        };
    
        // Ouvre le sélecteur de fichier
        input.click();
      }
    },     

    // Ajout du bouton custom pour ouvrir la bibliothèque d’images existantes
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
    
      editor.ui.registry.addButton('uploadImageGeneric', {
        text: 'Uploader une image',
        icon: 'upload',
        onAction: function () {
          const textarea = editor.getElement();
          const section = textarea?.dataset?.section || 'site';  // fallback : site
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
