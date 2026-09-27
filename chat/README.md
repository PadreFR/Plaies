# Papote — chat textuel avec des inconnus (prototype)

Un site où l’on discute par écrit, en tête-à-tête, avec une personne tirée au
hasard. Pas de compte, pas de vidéo. On peut indiquer des centres d’intérêt pour
être mis en relation en priorité avec quelqu’un qui les partage.

« Papote » est un nom provisoire : vérifier qu’il est libre (marque à l’INPI,
nom de domaine) avant de l’utiliser pour de vrai.

> Ce dossier est indépendant du site de Patricia Poggi (`site/`). Il n’est pas
> publié par GitHub Pages, qui ne sait pas faire tourner un serveur.

## Lancer le site sur son ordinateur

Il faut [Node.js](https://nodejs.org) 18 ou plus récent.

```bash
cd chat
npm install
npm start
```

Ouvrir ensuite <http://localhost:3000> dans **deux onglets** (ou deux
navigateurs) pour se parler à soi-même.

Lancer les tests : `npm test`.

## Ce qui est fait

- Mise en relation aléatoire, avec priorité aux intérêts communs. Si personne ne
  partage vos intérêts, vous êtes mis en relation avec n’importe qui au bout de
  5 secondes.
- Messages en direct, indicateur « L’inconnu écrit… », nombre de personnes en
  ligne.
- Bouton **Suivant** (à confirmer d’un second appui, ou touche Échap).
- Case « J’ai 18 ans ou plus » obligatoire.
- **Signaler** : termine la conversation, empêche de retomber sur la même
  personne pendant 24 h, et enregistre les derniers messages de la conversation
  dans `reports.jsonl`. Au bout de 3 signalements par des personnes
  différentes en 24 h, l’adresse IP est bloquée 24 h.
- Anti-spam : pas plus de 5 messages d’affilée, puis environ un par seconde.
- Les adresses IP ne sont jamais stockées en clair : seule une empreinte (hachage) est gardée.
- Aucun message n’est conservé, sauf ceux d’une conversation signalée.
- Adapté au téléphone, mode sombre automatique.

## Réglages

Variables d’environnement lues au démarrage :

| Variable        | Rôle                                                                 | Défaut            |
| --------------- | -------------------------------------------------------------------- | ----------------- |
| `PORT`          | Port d’écoute                                                        | `3000`            |
| `TRUST_PROXY`   | Mettre `1` derrière un hébergeur ou un proxy (lit `X-Forwarded-For`) | désactivé         |
| `BAN_THRESHOLD` | Nombre de signalements distincts avant blocage                       | `3`               |
| `REPORTS_FILE`  | Fichier où sont écrits les signalements                              | `reports.jsonl`   |
| `IP_SALT`       | Secret pour calculer l’empreinte des IP (à fixer pour garder les blocages) | aléatoire         |

## Organisation du code

- `server.js` : serveur web + WebSocket (`/ws`), relais des messages, signalements.
- `lib/matchmaker.js` : file d’attente et mise en relation.
- `lib/moderation.js` : nettoyage des textes, limitation du débit, signalements et blocages.
- `public/` : la page (HTML, CSS, JavaScript sans framework).
- `test/` : tests automatiques (`node --test`).

## Avant une ouverture au public

Le prototype suffit pour tester entre amis. Pour un vrai site public, il manque
au minimum :

1. **Hébergement** : un service qui fait tourner Node.js et accepte les
   WebSocket (Render, Railway, Fly.io, un petit serveur privé…), en HTTPS, avec
   `TRUST_PROXY=1`. Tout est en mémoire : une seule instance du serveur, et les
   blocages sont perdus au redémarrage (prévoir une base de données).
2. **Modération** : quelqu’un doit relire les signalements, en particulier ceux
   marqués « mineur ». Ajouter un filtre automatique (liens, insultes, contenus
   sexuels) et un moyen de contacter l’équipe.
3. **Âge** : une case à cocher ne vérifie rien. Réfléchir à une vraie
   vérification selon le public visé.
4. **Cadre légal (France / UE)** : mentions légales, conditions d’utilisation,
   politique de confidentialité (RGPD), obligations du règlement européen sur
   les services numériques (DSA) pour les plateformes, signalement des contenus
   illégaux sur PHAROS, et obligations de conservation des données de
   connexion. À faire valider par un juriste.
