# Site vitrine — Sidi Koné

Site vitrine professionnel (one-page) pour Sidi Koné, expert en développement rural, sécurité
alimentaire et nutritionnelle et action humanitaire au Mali.

Stack : HTML5 / CSS3 / JavaScript vanilla — aucune dépendance externe, aucun build nécessaire.
Choix volontaire pour un site léger et rapide, y compris sur des connexions internet limitées.

## Arborescence

```
Site_sidi/
├── index.html              # Page unique (FR) — toutes les sections (Accueil, Profil, Expertises, ...)
├── en/
│   └── index.html          # Version anglaise, mêmes sections, chemins relatifs adaptés
├── css/
│   └── style.css           # Palette, typographies, mise en page, responsive
├── js/
│   └── main.js             # Navigation, animations au scroll, compteurs, accordéon, formulaire
├── assets/
│   ├── images/
│   │   └── sidi-portrait.jpg   # Photo de profil (recadrée automatiquement, à remplacer si besoin)
│   └── cv/
│       └── CV-Sidi-Kone.pdf    # CV téléchargeable, généré depuis scripts/generate_cv.py
├── scripts/
│   └── generate_cv.py      # Script Python (reportlab) qui génère le CV PDF
├── robots.txt
├── sitemap.xml
└── README.md
```

## Lancer le site en local

Aucune installation n'est nécessaire : ouvrez simplement `index.html` dans un navigateur.

Pour un rendu plus fidèle à la production (chemins relatifs, cache), servez le dossier avec un
petit serveur local :

```bash
# Python (déjà présent sur la plupart des systèmes)
python -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Déploiement

Le site est un ensemble de fichiers statiques : il se déploie sur n'importe quel hébergeur statique.

- **Netlify** : glisser-déposer le dossier `Site_sidi` sur [app.netlify.com/drop](https://app.netlify.com/drop), ou connecter un dépôt Git.
- **Vercel** : `vercel deploy` depuis ce dossier (après `npm i -g vercel`).
- **GitHub Pages** : pousser ce dossier sur un dépôt GitHub, puis activer Pages sur la branche principale.

Avant la mise en ligne, pensez à :
1. Réserver le nom de domaine `smk-consulting.com` (déjà renseigné dans `index.html`, `robots.txt` et `sitemap.xml` — à corriger dans ces trois fichiers si le nom change).
2. Vérifier que `assets/cv/CV-Sidi-Kone.pdf` est à jour.

## Où modifier le contenu

Tout le contenu texte est directement dans `index.html`, section par section (commentaires
`<!-- ===== NOM DE LA SECTION ===== -->`). Il n'y a pas de CMS ni de fichier de données séparé —
modifiez le texte directement dans les balises HTML correspondantes.

Chaque information à personnaliser est signalée par un commentaire :
```html
<!-- TODO: à personnaliser — ... -->
```

### Liste des éléments à personnaliser avant mise en ligne

| Élément | Emplacement dans `index.html` | Statut |
|---|---|---|
| Photo de profil | `assets/images/sidi-portrait.jpg` | ✅ Portrait professionnel fourni par le client. |
| Adresse e-mail | Sections Contact et Pied de page | ✅ `sidi.kone@ymail.com`. |
| Numéro de téléphone | Section Contact | ✅ `+223 78 50 49 67`. |
| Lien LinkedIn | Sections Contact et Pied de page | ✅ Profil réel renseigné. |
| Nom de domaine | `index.html`, `en/index.html`, `robots.txt`, `sitemap.xml` | ⏳ `smk-consulting.com` est déjà pris par un tiers (revente possible via courtier, non recommandé). `sidikone.com` est disponible et retenu comme alternative — en attente d'achat, puis à corriger dans ces quatre fichiers. |
| CV en PDF | `assets/cv/CV-Sidi-Kone.pdf` | ✅ Généré depuis `scripts/generate_cv.py` (voir ci-dessous). |
| Témoignages | Section « Témoignages » | ✅ Trois témoignages réels (FAO, ADH-Mali, AMAPROS). |
| Formulaire de contact | Section Contact | ✅ Branché sur Formspree. |
| Favicon &amp; image de partage (OG) | `assets/images/apple-touch-icon.png`, `assets/images/og-image.jpg`, `favicon.ico` | ✅ Générés aux couleurs de la marque. |
| Disponibilité | Section Contact, sous-titre | ⏳ À préciser (ex. « disponible à partir de... »). |

## Source du contenu

Le texte du site (profil, expériences, formations, distinctions) reprend fidèlement le CV officiel
fourni par le client : `source/Sidi_KONE_CV_2026_Professionnel.docx`. Ce dossier `source/` n'est
qu'une référence de travail — à **exclure du déploiement** (ne pas le pousser vers l'hébergeur
statique, ou l'ajouter à un `.gitignore` si le projet passe sous Git), car il contient les
coordonnées personnelles complètes dans un format non destiné à la diffusion publique brute.

Toute mise à jour future du CV doit être répercutée à deux endroits : dans `index.html` (le texte
du site) et dans `scripts/generate_cv.py` (le CV PDF téléchargeable), voir ci-dessous.

## Mettre à jour le CV PDF

Le CV téléchargeable (`assets/cv/CV-Sidi-Kone.pdf`) est généré à partir du script
`scripts/generate_cv.py`, qui reprend fidèlement les données du CV officiel (profil, distinctions,
compétences, expériences, formations). Pour le régénérer après une modification :

```bash
pip install reportlab   # si nécessaire
python scripts/generate_cv.py
```

Vous pouvez aussi remplacer directement le fichier PDF par une version mise en forme dans un autre
outil (Word, Canva, etc.), à condition de conserver le même nom de fichier.

## Brancher le formulaire de contact

Le formulaire (section Contact) fonctionne déjà côté client : validation des champs obligatoires
(nom, e-mail, message) avant tout envoi. Il lui manque uniquement une destination d'envoi, à
choisir parmi les deux solutions suivantes (aucune n'exige de backend) :

### Option recommandée — Formspree

1. Créer un compte gratuit sur [formspree.io](https://formspree.io) et un nouveau formulaire.
2. Récupérer l'URL fournie (de la forme `https://formspree.io/f/xxxxxxxx`).
3. Dans `index.html`, sur la balise `<form id="contact-form" ...>`, ajouter l'attribut :
   ```html
   action="https://formspree.io/f/xxxxxxxx" method="POST"
   ```
4. C'est tout — `js/main.js` détecte automatiquement l'attribut `action` et envoie le formulaire en
   arrière-plan (sans rechargement de page), avec message de confirmation.

### Option alternative — EmailJS

1. Créer un compte sur [emailjs.com](https://www.emailjs.com) et configurer un service d'envoi
   (Gmail, Outlook...) et un template d'e-mail.
2. Inclure le SDK EmailJS dans `index.html` et adapter la fonction d'envoi dans `js/main.js`
   (remplacer le bloc `fetch(...)` par un appel à `emailjs.sendForm(...)`), en suivant la
   documentation officielle d'EmailJS.

Tant qu'aucune des deux options n'est branchée, le formulaire affiche un message clair indiquant
qu'il n'est pas encore connecté (aucun envoi silencieux ou perdu).

## Multilingue (FR / EN)

Le site existe en deux versions statiques indépendantes :

- `index.html` (français, `<html lang="fr">`) — page racine.
- `en/index.html` (anglais, `<html lang="en">`) — mêmes sections, chemins relatifs adaptés
  (`../css/style.css`, `../js/main.js`, `../assets/...`).

Un lien de bascule (« EN » / « Passer à la version française ») est présent dans l'en-tête de
chaque version, toujours visible (desktop et mobile), à côté du bouton hamburger.

Les quelques messages générés en JavaScript (erreurs de formulaire, libellés d'accessibilité du
menu) sont centralisés dans `js/main.js`, partagé par les deux pages : un dictionnaire `STRINGS`
choisit fr/en selon `document.documentElement.lang`, pour éviter de dupliquer le script.

Pour toute modification de contenu, penser à répercuter le changement dans les **deux** fichiers
HTML si l'information concernée doit apparaître dans les deux langues (ex. coordonnées de contact,
nouvelle expérience professionnelle).

## Accessibilité & performance

- Navigation clavier complète (lien d'évitement, focus visible, menu mobile accessible).
- Attributs ARIA sur le menu, l'accordéon et les messages de statut du formulaire.
- Contrastes de couleurs vérifiés sur la palette olive / terre de sienne / blanc cassé.
- Aucune police externe chargée (polices système) et aucune bibliothèque JavaScript tierce :
  le site reste utilisable sur une connexion lente.
- Image de profil compressée en JPEG (~26 Ko).

## Prochaines étapes possibles

- Réserver le nom de domaine `sidikone.com` (retenu — `smk-consulting.com` est déjà pris) et le
  connecter à l'hébergeur (Netlify → Domain settings) une fois acheté.
- Ajouter Google Search Console + Google Analytics (ou une alternative respectueuse de la vie privée comme Plausible) une fois le domaine en place.
- Préciser la disponibilité dans la section Contact (dernier élément « à personnaliser » restant).
