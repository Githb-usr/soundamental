document.addEventListener("DOMContentLoaded", function () {
  // Vérifie que TinyMCE est bien chargé
  if (typeof tinymce === "undefined") {
    console.warn("TinyMCE non chargé : richtext_init.js ignoré.");
    return;
  }

  tinymce.init({
    selector: '#id_contenu, textarea.richtext',
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
      'code | undo redo | formatselect fontselect fontsizeselect | ' +
      'bold italic underline strikethrough | forecolor backcolor | ' +
      'alignleft aligncenter alignright alignjustify | ' +
      'bullist numlist outdent indent | ' +
      'link image media table | browseImage uploadImageFromSite | fullscreen preview | insertGrilleImg',
    menubar: 'file edit view insert format tools table help',
    statusbar: true,
    content_style: "body { font-family: Arial,Helvetica,sans-serif; font-size:14px }",
    content_css: "/static/css/custom.css",
    fontsize_formats: "8pt 10pt 12pt 14pt 16pt 18pt 24pt 36pt 48pt",

    // ====== BALISES AUTORISÉES ======
    valid_elements: [
      "p[class|id|style]", "br", "ul[class|id|style]", "ol[class|id|style]", "li[class|id|style]",
      "div[class|id|style]", "span[class|id|style|aria-*|data-*]", "b", "strong", "i", "em", "u", "sup", "sub",
      "h1[class|id|style]", "h2[class|id|style]", "h3[class|id|style]", "h4[class|id|style]", "h5[class|id|style]", "h6[class|id|style]",
      "blockquote[class|id|style]", "pre[class|id|style]", "code[class|id|style]", "hr[class|id|style]",
      "a[href|title|target|rel|class|id|style]",
      "img[src|alt|title|width|height|style|class|id]",
      "table[class|id|style]", "tr[class|id|style]", "td[class|id|style]", "th[class|id|style]",
      "thead[class|id|style]", "tbody[class|id|style]", "tfoot[class|id|style]",
      "dl[class|id|style]", "dt[class|id|style]", "dd[class|id|style]",
      "figure[class|id|style]", "figcaption[class|id|style]",
      "section[class|id|style]", "article[class|id|style]", "nav[class|id|style]", "aside[class|id|style]", "main[class|id|style]",
      "header[class|id|style]", "footer[class|id|style]", "address[class|id|style]",
      "mark[class|id|style]", "time[class|id|style]", "abbr[class|id|style|title]", "cite[class|id|style]", "small[class|id|style]",
      "data[class|id|style|value]", "s[class|id|style]", "del[class|id|style|cite|datetime]", "ins[class|id|style|cite|datetime]",
      "kbd[class|id|style]", "samp[class|id|style]", "var[class|id|style]", "bdi[class|id|style]", "bdo[class|id|style|dir]",
      "details[class|id|style]", "summary[class|id|style]",
      "audio[src|controls|autoplay|loop|muted|preload|class|id|style]", "source[src|type|media]", "track[src|kind|label|srclang|default]",
      "video[src|controls|autoplay|loop|muted|preload|poster|width|height|class|id|style]",
      "iframe[src|width|height|frameborder|allowfullscreen|title|allow|scrolling|allowtransparency|sandbox|class|id|style]",
      // BALISES MANQUANTES POUR CAROUSEL BOOTSTRAP/SVG :
      "button[class|id|type|style|title|aria-*|data-*]",
      "svg[*]",
      "polyline[*]",
      "path[*]",
      "use[*]",
      "g[*]",
      "rect[*]",
      "circle[*]",
      "line[*]"
    ].join(','),

    // ====== BALISES ÉTENDUES AUTORISÉES ======
    extended_valid_elements: [
      "a[href|title|target|rel|class|id|style]", "img[src|alt|title|width|height|class|id|style]", "span[class|id|style|aria-*|data-*]", "div[class|id|style]", "p[class|id|style]",
      "ul[class|id|style]", "ol[class|id|style]", "li[class|id|style]",
      "table[class|id|style]", "tr[class|id|style]", "td[class|id|style]", "th[class|id|style]",
      "thead[class|id|style]", "tbody[class|id|style]", "tfoot[class|id|style]",
      "h1[class|id|style]", "h2[class|id|style]", "h3[class|id|style]", "h4[class|id|style]", "h5[class|id|style]", "h6[class|id|style]",
      "blockquote[class|id|style]", "pre[class|id|style]", "code[class|id|style]",
      "dl[class|id|style]", "dt[class|id|style]", "dd[class|id|style]",
      "figure[class|id|style]", "figcaption[class|id|style]",
      "section[class|id|style]", "article[class|id|style]", "nav[class|id|style]", "aside[class|id|style]", "main[class|id|style]",
      "header[class|id|style]", "footer[class|id|style]", "address[class|id|style]",
      "mark[class|id|style]", "time[class|id|style]", "abbr[class|id|style|title]", "cite[class|id|style]", "small[class|id|style]",
      "data[class|id|style|value]", "s[class|id|style]", "del[class|id|style|cite|datetime]", "ins[class|id|style|cite|datetime]",
      "kbd[class|id|style]", "samp[class|id|style]", "var[class|id|style]", "bdi[class|id|style]", "bdo[class|id|style|dir]",
      "details[class|id|style]", "summary[class|id|style]",
      "audio[src|controls|autoplay|loop|muted|preload|class|id|style]", "source[src|type|media]", "track[src|kind|label|srclang|default]",
      "video[src|controls|autoplay|loop|muted|preload|poster|width|height|class|id|style]",
      "iframe[src|width|height|frameborder|allowfullscreen|title|allow|scrolling|allowtransparency|sandbox|class|id|style]",
      // BALISES MANQUANTES POUR CAROUSEL BOOTSTRAP/SVG :
      "button[class|id|type|style|title|aria-*|data-*]",
      "svg[*]",
      "polyline[*]",
      "path[*]",
      "use[*]",
      "g[*]",
      "rect[*]",
      "circle[*]",
      "line[*]"
    ].join(','),

    valid_styles: {
      '*': 'float,width,height,max-width,max-height,min-width,min-height,margin,margin-top,margin-bottom,margin-left,margin-right,padding,padding-top,padding-bottom,padding-left,padding-right,display,border,border-radius,background,background-color,background-image,background-size,background-repeat,background-position,text-align,vertical-align,position,top,left,right,bottom,overflow,overflow-x,overflow-y,box-shadow,font-size,font-family,font-weight,font-style,color,letter-spacing,line-height,text-decoration,text-transform,white-space,word-break,word-wrap,opacity,filter,z-index,list-style-type,list-style-position,outline,outline-color,outline-width,outline-style,caption-side,table-layout,empty-cells,border-collapse,border-spacing'
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

      editor.ui.registry.addButton('insertGrilleImg', {
        text: 'Grille d\'images',
        tooltip: 'Insérer une grille d’images',
        onAction: function () {
          editor.insertContent(
            `<div id="albums-grille">
              <img src="/media/blog/img1.jpg" alt="Objet 1" title="Objet 1">
              <img src="/media/blog/img2.jpg" alt="Objet 2" title="Objet 2">
              <img src="/media/blog/img3.jpg" alt="Objet 3" title="Objet 3">
              <img src="/media/blog/img4.jpg" alt="Objet 4" title="Objet 4">
              <img src="/media/blog/img5.jpg" alt="Objet 5" title="Objet 5">
            </div>`
          );
        }
      });

      editor.on('change', function () {
        editor.save();
      });
    }
  });
});
