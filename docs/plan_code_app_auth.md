
# Plan pour l'app `app_auth` – Authentification Soundamental

## 📦 1. Création et déclaration de l’app
- Créer l’app `app_auth`
- Ajouter `app_auth` à `INSTALLED_APPS` dans `config/settings/base.py`

## 🌐 2. Configuration des URLs
- Créer un fichier `urls.py` dans `app_auth`
- Ajouter les URLs suivantes :
  - `/login/`
  - `/logout/`
  - `/password-reset/`
  - `/password-reset/confirm/...`
  - `/password-change/`
- Inclure les URLs de `app_auth` dans `config/urls.py`

## 🎨 3. Templates à prévoir
Créer dans `templates/app_auth/` :

- `login.html`
- `logout.html` *(facultatif)*
- `password_reset_form.html`
- `password_reset_done.html` ✅ message confirmation simple
- `password_reset_confirm.html`
- `password_reset_complete.html`
- `password_change_form.html`
- `password_change_done.html` ✅ message confirmation simple
- `login_error.html` *(ou intégré dans `login.html`)*

## 🔐 4. Comportements à définir

- ✅ Redirection après connexion : vers la **page d’accueil**
- ✅ Message de confirmation après :
  - Réinitialisation mot de passe
  - Changement de mot de passe
- ✅ Message d’erreur clair si identifiants invalides

## 🧑‍💼 5. Gestion des rôles et permissions

### Groupes recommandés :
- `SuperAdmin` : tous les droits (toi seul)
- `Admin` : droits étendus mais limités (gestion de contenu, pas des comptes)
- `Contributeur` : création/édition de contenu (limité)
- `Membre` : accès à son espace utilisateur
- `Visiteur` : **non connecté**, pas besoin de groupe (`user.is_authenticated == False`)
