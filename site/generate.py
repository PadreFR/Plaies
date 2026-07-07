#!/usr/bin/env python3
# One-off generator: unrolls the Claude Design SPA into static, linked HTML pages.
import os

NAV = [
    ("index.html", "Accueil"),
    ("a-propos.html", "À propos"),
    ("expertises.html", "Expertises"),
    ("patients-proches.html", "Patients"),
    ("professionnels.html", "Professionnels"),
    ("formations.html", "Formations"),
    ("ressources.html", "Ressources"),
]
FOOTER_NAV = NAV + [("contact.html", "Contact")]

SITE_TITLE = "Patricia Poggi — Plaies & Cicatrisation"

def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''

def header(active):
    desktop_links = []
    mobile_links = []
    for href, label in NAV:
        cls = " active" if href == active else ""
        desktop_links.append(f'          <a href="{href}" class="nav-link{cls}">{label}</a>')
        mobile_links.append(f'          <a href="{href}" class="mobile-nav-link{cls}">{label}</a>')
    desktop_links = "\n".join(desktop_links)
    mobile_links = "\n".join(mobile_links)
    return f'''<header class="site-header">
  <div class="header-inner">
    <a href="index.html" class="brand">
      <img src="assets/mark-poggi.png" alt="Logo Poggi" width="42" height="42">
      <span class="brand-text">
        <span class="brand-name">Patricia Poggi</span>
        <span class="brand-sub">Plaies &amp; Cicatrisation</span>
      </span>
    </a>

    <nav class="desktop-nav">
{desktop_links}
      <a href="contact.html" class="btn-pill-primary">Prendre contact</a>
    </nav>

    <button class="menu-toggle" data-menu-toggle aria-label="Menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>

  <div class="mobile-nav" data-mobile-nav>
    <div class="mobile-nav-inner">
{mobile_links}
      <a href="contact.html" class="btn-pill-primary">Prendre contact</a>
    </div>
  </div>
</header>

<main>
'''

def footer():
    footer_links = "\n".join(
        f'          <a href="{href}" class="footer-link">{label}</a>' for href, label in FOOTER_NAV
    )
    return f'''</main>

<footer class="site-footer">
  <div class="footer-top">
    <div style="max-width:280px">
      <div class="footer-brand">
        <img src="assets/mark-poggi.png" width="38" height="38" alt="">
        <span class="footer-brand-text">
          <span class="footer-brand-name">Patricia Poggi</span>
          <span class="footer-brand-sub">Plaies &amp; Cicatrisation</span>
        </span>
      </div>
      <p style="margin:0;font:400 13.5px/1.7 'Mulish',sans-serif;color:#93A0A8">Expertise, accompagnement et coordination des soins pour les plaies complexes, chroniques ou à cicatrisation difficile.</p>
    </div>
    <div>
      <div class="footer-col-title">Navigation</div>
      <div class="footer-links">
{footer_links}
      </div>
    </div>
    <div>
      <div class="footer-col-title">Informations</div>
      <div class="footer-links">
        <a href="mentions-legales.html" class="footer-link">Mentions légales</a>
        <a href="mentions-legales.html" class="footer-link">Politique de confidentialité</a>
        <a href="mentions-legales.html" class="footer-link">Accessibilité</a>
        <a href="contact.html" class="footer-link">Plan du site</a>
      </div>
    </div>
    <div>
      <div class="footer-col-title">Contact</div>
      <div class="footer-links">
        <a href="contact.html" class="footer-link">Formulaire de contact</a>
        <span class="footer-static">[Ajouter e-mail]</span>
        <span class="footer-static">[Ajouter téléphone]</span>
        <span class="footer-static">[Réseaux professionnels]</span>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="footer-bottom-inner">
      <span class="footer-copy">© 2026 Patricia Poggi — Plaies &amp; Cicatrisation. Tous droits réservés.</span>
      <span class="footer-note">Ce site ne remplace pas une consultation ou un avis médical personnalisé.</span>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
</body>
</html>
'''

def page(filename, active, title, desc, body):
    html = head(title, desc) + header(active) + body + footer()
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)

PAGES = {}

# ============================================================= ACCUEIL
PAGES["accueil"] = '''
<section class="hero-section">
  <div class="container" style="padding:clamp(48px,6vw,88px) 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:clamp(32px,5vw,64px);align-items:center">
    <div>
      <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(124,154,139,.16);border:1px solid rgba(94,125,110,.3);border-radius:999px;padding:6px 14px;margin-bottom:26px">
        <span style="width:7px;height:7px;border-radius:50%;background:#5E7D6E;display:block"></span>
        <span style="font:600 11.5px 'Mulish',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#4C6857">Expertise en cicatrisation</span>
      </div>
      <h1 class="h1">Patricia&nbsp;Poggi<br><span style="color:#5E7D6E;font-style:italic;font-weight:300">Plaies &amp; Cicatrisation</span></h1>
      <p class="lede" style="margin:0 0 18px;max-width:30ch">Accompagnement spécialisé des plaies complexes, chroniques ou à cicatrisation difficile.</p>
      <p class="body-text" style="margin:0 0 34px;max-width:46ch">Une approche clinique, coordonnée et personnalisée pour les patients, les soignants et les structures de soins.</p>
      <div style="display:flex;flex-wrap:wrap;gap:14px">
        <a href="contact.html" class="btn-pill-primary large">Prendre contact</a>
        <a href="professionnels.html" class="btn-pill-secondary">Je suis professionnel de santé</a>
      </div>
    </div>
    <div style="position:relative">
      <div class="placeholder-box">
        <span class="placeholder-caption">photo — geste de soin / consultation, sans plaie visible</span>
      </div>
      <div class="floating-badge">
        <img src="assets/mark-poggi.png" width="34" height="34" alt="">
        <span>Évaluation · Coordination · Stratégie de soin</span>
      </div>
    </div>
  </div>
</section>

<section class="container section">
  <div style="max-width:640px;margin-bottom:44px">
    <div class="eyebrow">Pour qui ?</div>
    <h2 class="h2">Un appui adapté à chaque situation</h2>
  </div>
  <div class="grid grid-auto-280">
    <div class="card">
      <div class="card-icon">1</div>
      <h3>Patients &amp; proches</h3>
      <p>Comprendre une plaie qui ne cicatrise pas, préparer une consultation et être orienté.</p>
    </div>
    <div class="card">
      <div class="card-icon">2</div>
      <h3>Professionnels de santé</h3>
      <p>Bénéficier d’un appui spécialisé pour les situations de cicatrisation complexe.</p>
    </div>
    <div class="card">
      <div class="card-icon">3</div>
      <h3>Établissements</h3>
      <p>Former les équipes, structurer les protocoles et améliorer les pratiques autour des plaies chroniques.</p>
    </div>
  </div>
</section>

<section class="sage-band">
  <div class="container section">
    <div style="max-width:640px;margin-bottom:40px">
      <div class="eyebrow">Domaines d’intervention</div>
      <h2 class="h2">Des situations de cicatrisation complexes</h2>
    </div>
    <div class="grid grid-auto-220" style="gap:14px">
      <div class="tile"><span class="diamond"></span><span class="label">Plaies chroniques</span></div>
      <div class="tile"><span class="diamond"></span><span class="label">Ulcères de jambe</span></div>
      <div class="tile"><span class="diamond"></span><span class="label">Escarres</span></div>
      <div class="tile"><span class="diamond"></span><span class="label">Pied diabétique</span></div>
      <div class="tile"><span class="diamond"></span><span class="label">Plaies post-opératoires</span></div>
      <div class="tile"><span class="diamond"></span><span class="label">Retards de cicatrisation</span></div>
      <div class="tile"><span class="diamond"></span><span class="label">Douleur au soin</span></div>
      <div class="tile"><span class="diamond"></span><span class="label">Prévention des récidives</span></div>
    </div>
  </div>
</section>

<section class="container section">
  <div style="max-width:640px;margin-bottom:48px">
    <div class="eyebrow">Méthode</div>
    <h2 class="h2">Une démarche structurée, du bilan au suivi</h2>
  </div>
  <div class="grid grid-auto-240">
    <div style="position:relative;padding-top:20px">
      <div style="font:300 46px 'Spectral',serif;color:#7C9A8B;line-height:1;margin-bottom:16px">01</div>
      <div style="height:1px;background:rgba(29,59,82,.14);margin-bottom:18px"></div>
      <h3 style="margin:0 0 10px;font:600 21px 'Spectral',serif;color:#1D3B52">Évaluer</h3>
      <p style="margin:0;font:400 15px/1.65 'Mulish',sans-serif;color:#4A5860">Comprendre la plaie, son évolution, le contexte médical et les facteurs de retard.</p>
    </div>
    <div style="position:relative;padding-top:20px">
      <div style="font:300 46px 'Spectral',serif;color:#7C9A8B;line-height:1;margin-bottom:16px">02</div>
      <div style="height:1px;background:rgba(29,59,82,.14);margin-bottom:18px"></div>
      <h3 style="margin:0 0 10px;font:600 21px 'Spectral',serif;color:#1D3B52">Coordonner</h3>
      <p style="margin:0;font:400 15px/1.65 'Mulish',sans-serif;color:#4A5860">Travailler avec les professionnels déjà impliqués dans le parcours de soin.</p>
    </div>
    <div style="position:relative;padding-top:20px">
      <div style="font:300 46px 'Spectral',serif;color:#7C9A8B;line-height:1;margin-bottom:16px">03</div>
      <div style="height:1px;background:rgba(29,59,82,.14);margin-bottom:18px"></div>
      <h3 style="margin:0 0 10px;font:600 21px 'Spectral',serif;color:#1D3B52">Adapter</h3>
      <p style="margin:0;font:400 15px/1.65 'Mulish',sans-serif;color:#4A5860">Construire une stratégie réaliste, traçable et réévaluable.</p>
    </div>
    <div style="position:relative;padding-top:20px">
      <div style="font:300 46px 'Spectral',serif;color:#7C9A8B;line-height:1;margin-bottom:16px">04</div>
      <div style="height:1px;background:rgba(29,59,82,.14);margin-bottom:18px"></div>
      <h3 style="margin:0 0 10px;font:600 21px 'Spectral',serif;color:#1D3B52">Prévenir</h3>
      <p style="margin:0;font:400 15px/1.65 'Mulish',sans-serif;color:#4A5860">Limiter les complications, les récidives et les ruptures de suivi.</p>
    </div>
  </div>
</section>

<section class="quote-section">
  <div style="max-width:960px;margin:0 auto;padding:clamp(60px,8vw,110px) 24px;text-align:center">
    <div class="quote-mark">"</div>
    <p class="quote-text">Une plaie n’est jamais seulement une lésion cutanée. Elle s’inscrit dans une histoire médicale, un quotidien, des contraintes de soin et parfois une perte de qualité de vie.</p>
  </div>
</section>

<section class="container section">
  <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;justify-content:space-between;margin-bottom:40px">
    <div style="max-width:560px">
      <div class="eyebrow">Ressources</div>
      <h2 class="h2">Comprendre pour mieux accompagner</h2>
    </div>
    <a href="ressources.html" class="btn-pill-secondary small">Toutes les ressources</a>
  </div>
  <div class="grid grid-auto-280">
    <a href="ressources.html" class="article-card">
      <div class="placeholder-box wide">
        <span class="placeholder-caption small">illustration sobre — carnet clinique</span>
      </div>
      <div class="article-card-body">
        <div class="eyebrow" style="margin-bottom:12px">Article</div>
        <h3>Plaie chronique : quand demander un avis ?</h3>
        <span class="read-more">Lire &rarr;</span>
      </div>
    </a>
    <a href="ressources.html" class="article-card">
      <div class="placeholder-box wide">
        <span class="placeholder-caption small">illustration sobre — prévention</span>
      </div>
      <div class="article-card-body">
        <div class="eyebrow" style="margin-bottom:12px">Article</div>
        <h3>Escarre : les signes à surveiller</h3>
        <span class="read-more">Lire &rarr;</span>
      </div>
    </a>
    <a href="ressources.html" class="article-card">
      <div class="placeholder-box wide">
        <span class="placeholder-caption small">illustration sobre — matériel propre</span>
      </div>
      <div class="article-card-body">
        <div class="eyebrow" style="margin-bottom:12px">Article</div>
        <h3>Cicatrisation difficile : pourquoi une plaie peut stagner ?</h3>
        <span class="read-more">Lire &rarr;</span>
      </div>
    </a>
  </div>
</section>

<section class="container" style="padding:0 24px clamp(60px,8vw,100px)">
  <div class="cta-box">
    <h2 style="margin:0 auto 16px;max-width:22ch;font:400 clamp(26px,3.2vw,38px) 'Spectral',serif;line-height:1.15;color:#1D3B52">Vous souhaitez demander un avis, organiser une formation ou échanger sur une situation complexe ?</h2>
    <div style="display:flex;justify-content:center;margin:28px 0 22px">
      <a href="contact.html" class="btn-pill-primary" style="padding:16px 34px">Contacter Patricia Poggi</a>
    </div>
    <p style="margin:0 auto;max-width:56ch;font:400 13px/1.6 'Mulish',sans-serif;color:#6A757D">Ce formulaire ne remplace pas une consultation médicale et ne doit pas être utilisé en cas d’urgence.</p>
  </div>
</section>
'''

page("index.html", "index.html", SITE_TITLE,
     "Accompagnement spécialisé des plaies complexes, chroniques ou à cicatrisation difficile.",
     PAGES["accueil"])

# ============================================================= À PROPOS
PAGES["apropos"] = '''
<section class="hero-section bordered">
  <div class="container" style="padding:clamp(48px,6vw,84px) 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:clamp(32px,5vw,56px);align-items:center">
    <div>
      <div class="eyebrow">À propos</div>
      <h1 class="h1" style="font-size:clamp(34px,4.6vw,52px);line-height:1.08;margin-bottom:24px">Patricia Poggi</h1>
      <p style="margin:0 0 18px;font:400 17px/1.75 'Mulish',sans-serif;color:#3E4A52;max-width:52ch">Les plaies chroniques ou complexes nécessitent rarement une réponse unique. Elles demandent une évaluation globale : état de la plaie, douleur, mobilité, pathologies associées, nutrition, observance, environnement de soin et coordination entre professionnels.</p>
      <p style="margin:0;font:500 17px/1.75 'Mulish',sans-serif;color:#2C5169;max-width:52ch">Mon rôle est d’apporter une expertise spécialisée, lisible et utile, pour aider à construire une prise en charge adaptée.</p>
    </div>
    <div class="placeholder-box">
      <span class="placeholder-caption">photo professionnelle — portrait</span>
    </div>
  </div>
</section>

<section class="container section">
  <div class="eyebrow">Parcours &amp; expertise</div>
  <h2 style="margin:0 0 36px;font:400 clamp(26px,3.2vw,36px) 'Spectral',serif;color:#1D3B52">Une spécialisation dédiée aux plaies</h2>
  <div class="grid grid-auto-260" style="gap:18px">
    <div style="background:#FBF9F5;border:1px solid rgba(29,59,82,.1);border-radius:16px;padding:26px 24px">
      <div style="font:700 11px 'Mulish',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#5E7D6E;margin-bottom:12px">Statut professionnel</div>
      <p style="margin:0;font:500 15.5px/1.55 'Mulish',sans-serif;color:#6A757D">[Ajouter ici le statut professionnel exact]</p>
    </div>
    <div style="background:#FBF9F5;border:1px solid rgba(29,59,82,.1);border-radius:16px;padding:26px 24px">
      <div style="font:700 11px 'Mulish',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#5E7D6E;margin-bottom:12px">Diplômes &amp; formations</div>
      <p style="margin:0;font:500 15.5px/1.55 'Mulish',sans-serif;color:#6A757D">[Ajouter ici les diplômes]</p>
    </div>
    <div style="background:#FBF9F5;border:1px solid rgba(29,59,82,.1);border-radius:16px;padding:26px 24px">
      <div style="font:700 11px 'Mulish',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#5E7D6E;margin-bottom:12px">Expérience</div>
      <p style="margin:0;font:500 15.5px/1.55 'Mulish',sans-serif;color:#6A757D">[Ajouter ici les années d’expérience]</p>
    </div>
    <div style="background:#FBF9F5;border:1px solid rgba(29,59,82,.1);border-radius:16px;padding:26px 24px">
      <div style="font:700 11px 'Mulish',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#5E7D6E;margin-bottom:12px">Collaborations</div>
      <p style="margin:0;font:500 15.5px/1.55 'Mulish',sans-serif;color:#6A757D">[Ajouter ici les structures ou collaborations]</p>
    </div>
  </div>
</section>

<section class="sage-band">
  <div class="container" style="padding:clamp(52px,6vw,80px) 24px">
    <div class="eyebrow">Structures accompagnées</div>
    <h2 style="margin:0 0 30px;font:400 clamp(26px,3.2vw,36px) 'Spectral',serif;color:#1D3B52">Une expérience de terrain, en ville et en établissement</h2>
    <div style="display:flex;flex-wrap:wrap;gap:12px">
      <span class="pill-tag">Domicile</span>
      <span class="pill-tag">Cabinet</span>
      <span class="pill-tag">EHPAD</span>
      <span class="pill-tag">HAD</span>
      <span class="pill-tag">Établissements de santé</span>
      <span class="pill-tag">Équipes de soins</span>
    </div>
  </div>
</section>

<section style="max-width:920px;margin:0 auto;padding:clamp(52px,6vw,88px) 24px">
  <div class="eyebrow">Vision du soin</div>
  <p style="margin:0;font:300 clamp(22px,2.8vw,30px)/1.5 'Spectral',serif;font-style:italic;color:#1D3B52">Apporter une expertise spécialisée, lisible et utile — au service d’une prise en charge réaliste, coordonnée et respectueuse du quotidien de chaque personne.</p>
</section>
'''

page("a-propos.html", "a-propos.html", f"À propos — {SITE_TITLE}",
     "Présentation de Patricia Poggi, parcours, expertise et structures accompagnées.",
     PAGES["apropos"])

# ============================================================= EXPERTISES
EXPERTISE_BLOCKS = [
    ("Plaies chroniques", "Une plaie qui ne cicatrise pas dans les délais attendus nécessite une évaluation globale des facteurs qui freinent la réparation tissulaire."),
    ("Ulcères veineux, artériels ou mixtes", "Identifier l’origine vasculaire est déterminant pour orienter la stratégie de soin et l’indication éventuelle d’une compression."),
    ("Escarres", "Évaluation du stade, prévention et adaptation des soins selon la localisation, la mobilité et l’état général de la personne."),
    ("Plaies du pied diabétique", "Une vigilance particulière s’impose : le pied diabétique expose à des complications rapides qui justifient un suivi rapproché."),
    ("Plaies post-opératoires difficiles", "Accompagnement des cicatrisations qui se compliquent ou se prolongent après une intervention chirurgicale."),
    ("Plaies douloureuses", "Intégrer la douleur ressentie pendant et entre les soins dans la stratégie thérapeutique et le choix des pansements."),
    ("Plaies exsudatives", "Gérer un exsudat abondant par un choix de pansement adapté, réévalué régulièrement selon l’évolution."),
    ("Retards de cicatrisation", "Rechercher et corriger les facteurs — locaux, généraux, environnementaux — qui font stagner la plaie."),
    ("Prévention des récidives", "Limiter la réapparition des plaies par un accompagnement durable et des mesures de prévention adaptées."),
    ("Aide au choix et à l’adaptation des pansements", "Un choix raisonné, sans solution universelle, ajusté à chaque plaie et à chaque contexte de soin."),
    ("Coordination du parcours de soin", "Faire le lien entre les professionnels impliqués pour assurer la cohérence et la continuité de la prise en charge."),
]
AVIS_SPECIALISE = [
    "Plaie qui ne cicatrise pas", "Plaie qui s’aggrave", "Douleur importante", "Exsudat abondant",
    "Odeur inhabituelle", "Récidive", "Difficulté à trouver le bon protocole de soin",
    "Situation complexe impliquant plusieurs professionnels",
]

expertise_cards = "\n".join(
    f'''    <div class="card" style="gap:12px">
      <span class="diamond"></span>
      <h3>{title}</h3>
      <p>{text}</p>
    </div>''' for title, text in EXPERTISE_BLOCKS
)
avis_tiles = "\n".join(
    f'''      <div style="display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:18px 20px">
        <span class="diamond" style="width:8px;height:8px"></span>
        <span style="font:500 15.5px 'Mulish',sans-serif;color:#EDE7DC">{item}</span>
      </div>''' for item in AVIS_SPECIALISE
)

PAGES["expertises"] = f'''
<section class="hero-section bordered">
  <div class="container" style="padding:clamp(48px,6vw,84px) 24px;max-width:860px">
    <div class="eyebrow">Expertises</div>
    <h1 class="h1-page">Un appui spécialisé pour les plaies complexes</h1>
    <p class="body-text-lg" style="max-width:60ch">Une évaluation, une aide à la stratégie de soin et une coordination du parcours — au service des patients comme des professionnels qui les accompagnent.</p>
  </div>
</section>

<section class="container" style="padding:clamp(52px,6vw,80px) 24px">
  <div class="grid grid-auto-300">
{expertise_cards}
  </div>
</section>

<section class="petrol-band">
  <div class="container" style="padding:clamp(52px,6vw,80px) 24px">
    <div style="max-width:600px;margin-bottom:36px">
      <div class="eyebrow" style="color:#7C9A8B">Repères</div>
      <h2 style="margin:0;font:400 clamp(26px,3.2vw,38px) 'Spectral',serif;color:#F3EFE8">Quand demander un avis spécialisé ?</h2>
    </div>
    <div class="grid grid-auto-260" style="gap:14px">
{avis_tiles}
    </div>
  </div>
</section>

<section class="container" style="padding:clamp(44px,6vw,72px) 24px">
  <div class="alert-terracotta" style="max-width:820px">
    <p>L’accompagnement proposé est un appui spécialisé : évaluation, aide à la stratégie de soin et coordination. Il ne constitue pas un diagnostic médical à distance et ne promet pas de guérison. Il vient en complément — jamais en remplacement — d’une consultation ou d’un avis médical personnalisé.</p>
  </div>
  <div style="display:flex;justify-content:center;margin-top:44px">
    <a href="contact.html" class="btn-pill-primary" style="padding:15px 30px">Demander un avis</a>
  </div>
</section>
'''

page("expertises.html", "expertises.html", f"Expertises — {SITE_TITLE}",
     "Plaies chroniques, ulcères, escarres, pied diabétique : un appui spécialisé pour les situations de cicatrisation complexe.",
     PAGES["expertises"])

# ============================================================= PATIENTS & PROCHES
PATIENTS_SECTIONS = [
    ("01", "Comprendre ce qu’est une plaie chronique", "Une plaie est dite chronique lorsqu’elle ne cicatrise pas dans les délais habituellement attendus. Ce n’est pas une fatalité, mais le signe qu’une évaluation plus approfondie est utile."),
    ("02", "Pourquoi une plaie peut avoir du mal à cicatriser", "De nombreux facteurs peuvent ralentir la cicatrisation : circulation, diabète, nutrition, infection, pression, douleur ou soins non adaptés. Souvent, plusieurs facteurs se combinent."),
    ("03", "Comment préparer un échange ou une consultation", "Rassembler les bonnes informations en amont permet de gagner du temps et d’obtenir un avis plus précis sur votre situation."),
    ("04", "Quand consulter rapidement", "Certains signes doivent alerter et conduire à contacter rapidement un professionnel de santé (voir l’encadré ci-dessous)."),
]
PATIENTS_PREPARE = [
    "Ordonnances", "Liste des traitements", "Antécédents médicaux importants",
    "Compte-rendu opératoire si nécessaire", "Résultats récents si disponibles",
    "Évolution de la plaie", "Nom des professionnels déjà impliqués",
]
PATIENTS_ALERTE = "En cas de fièvre, douleur importante, rougeur qui s’étend, écoulement purulent, mauvaise odeur brutale, aggravation rapide, plaie chez une personne diabétique ou altération de l’état général, il faut contacter rapidement un professionnel de santé ou un service d’urgence."

patients_rows = "\n".join(
    f'''    <div style="display:flex;gap:22px;padding:26px 0;border-bottom:1px solid rgba(29,59,82,.1)">
      <div style="font:300 34px 'Spectral',serif;color:#7C9A8B;line-height:1;flex:none;width:44px">{num}</div>
      <div>
        <h3 style="margin:0 0 10px;font:600 21px 'Spectral',serif;color:#1D3B52">{title}</h3>
        <p style="margin:0;font:400 15.5px/1.7 'Mulish',sans-serif;color:#4A5860">{text}</p>
      </div>
    </div>''' for num, title, text in PATIENTS_SECTIONS
)
patients_prepare_tiles = "\n".join(
    f'''      <div class="check-tile"><span class="check">&#10003;</span><span class="label">{item}</span></div>'''
    for item in PATIENTS_PREPARE
)

PAGES["patients"] = f'''
<section class="hero-section bordered">
  <div class="container" style="padding:clamp(48px,6vw,84px) 24px;max-width:820px">
    <div class="eyebrow">Patients &amp; proches</div>
    <h1 class="h1-page">Vous avez une plaie qui ne cicatrise pas ?</h1>
    <p class="body-text-lg" style="max-width:58ch">Comprendre, se repérer et préparer un échange : quelques clés pour aborder plus sereinement une plaie qui tarde à guérir.</p>
  </div>
</section>

<section class="section-narrow" style="padding:clamp(48px,6vw,72px) 24px">
  <div style="display:flex;flex-direction:column;gap:8px">
{patients_rows}
  </div>
</section>

<section class="sage-band">
  <div class="section-narrow" style="padding:clamp(48px,6vw,72px) 24px">
    <div class="eyebrow">À préparer</div>
    <h2 style="margin:0 0 28px;font:400 clamp(24px,3vw,34px) 'Spectral',serif;color:#1D3B52">Quels documents rassembler</h2>
    <div class="grid grid-auto-240" style="gap:12px">
{patients_prepare_tiles}
    </div>
  </div>
</section>

<section class="section-narrow" style="padding:clamp(44px,6vw,72px) 24px">
  <div class="alert-urgence">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
      <span class="alert-urgence-icon">!</span>
      <h3>Quand consulter rapidement</h3>
    </div>
    <p>{PATIENTS_ALERTE}</p>
  </div>
  <p style="margin:26px 0 0;font:400 13px/1.6 'Mulish',sans-serif;color:#6A757D;text-align:center">Ces informations sont générales et ne remplacent pas un avis médical personnalisé.</p>
</section>
'''

page("patients-proches.html", "patients-proches.html", f"Patients &amp; proches — {SITE_TITLE}",
     "Comprendre une plaie qui ne cicatrise pas, préparer une consultation et savoir quand consulter rapidement.",
     PAGES["patients"])

# ============================================================= PROFESSIONNELS
PRO_PUBLICS = ["Médecins", "Infirmiers libéraux", "Pharmaciens", "EHPAD", "HAD", "SSIAD", "Établissements de santé", "Équipes de coordination"]
PRO_SERVICES = [
    "Avis spécialisé sur situation complexe", "Aide à l’évaluation d’une plaie",
    "Aide à la structuration d’un protocole de soin", "Coordination ville-hôpital",
    "Appui aux équipes de terrain", "Formation", "Audit des pratiques",
    "Mise à jour des protocoles internes", "Traçabilité et transmissions",
]
PRO_SITUATIONS = [
    ("01", "Ulcère qui stagne"), ("02", "Escarre récidivante"), ("03", "Plaie très exsudative"),
    ("04", "Douleur pendant les soins"), ("05", "Pansements changés sans stratégie claire"),
    ("06", "Suspicion de facteur vasculaire ou métabolique"),
    ("07", "Besoin de coordination entre prescripteur, infirmiers et structure"),
]

pro_publics_tags = "\n".join(f'      <span class="pill-tag">{p}</span>' for p in PRO_PUBLICS)
pro_services_tiles = "\n".join(
    f'''      <div class="tile"><span class="diamond"></span><span class="label">{s}</span></div>'''
    for s in PRO_SERVICES
)
pro_situations_rows = "\n".join(
    f'''    <div style="display:flex;align-items:center;gap:16px;padding:18px 4px;border-bottom:1px solid rgba(29,59,82,.1)">
      <span style="font:600 14px 'Mulish',sans-serif;color:#7C9A8B;flex:none;width:26px">{num}</span>
      <span style="font:500 16px 'Mulish',sans-serif;color:#284453">{label}</span>
    </div>''' for num, label in PRO_SITUATIONS
)

PAGES["professionnels"] = f'''
<section class="hero-section bordered">
  <div class="container" style="padding:clamp(48px,6vw,84px) 24px;max-width:860px">
    <div class="eyebrow">Professionnels de santé</div>
    <h1 class="h1-page" style="font-size:clamp(30px,4.2vw,48px);line-height:1.12">Un appui spécialisé pour les situations de cicatrisation complexe</h1>
    <p class="body-text-lg" style="max-width:60ch">Évaluation, structuration de protocole, coordination ville-hôpital et appui aux équipes de terrain — en complément de votre prise en charge.</p>
  </div>
</section>

<section class="container" style="padding:clamp(48px,6vw,72px) 24px">
  <div class="eyebrow" style="margin-bottom:20px">Publics concernés</div>
  <div style="display:flex;flex-wrap:wrap;gap:12px">
{pro_publics_tags}
  </div>
</section>

<section class="sage-band">
  <div class="container" style="padding:clamp(48px,6vw,80px) 24px">
    <div class="eyebrow">Services</div>
    <h2 style="margin:0 0 32px;font:400 clamp(26px,3.2vw,36px) 'Spectral',serif;color:#1D3B52">Un accompagnement modulable</h2>
    <div class="grid grid-auto-280" style="gap:14px">
{pro_services_tiles}
    </div>
  </div>
</section>

<section class="container" style="padding:clamp(48px,6vw,80px) 24px">
  <div class="eyebrow">Situations fréquentes</div>
  <h2 style="margin:0 0 32px;font:400 clamp(26px,3.2vw,36px) 'Spectral',serif;color:#1D3B52">Des cas où un regard spécialisé aide</h2>
  <div style="display:flex;flex-direction:column;gap:2px">
{pro_situations_rows}
  </div>
  <div style="display:flex;justify-content:center;margin-top:44px">
    <a href="contact.html" class="btn-pill-primary" style="padding:15px 30px">Échanger sur une situation</a>
  </div>
</section>
'''

page("professionnels.html", "professionnels.html", f"Professionnels de santé — {SITE_TITLE}",
     "Un appui spécialisé pour les situations de cicatrisation complexe : évaluation, coordination, formation, audit.",
     PAGES["professionnels"])

# ============================================================= FORMATIONS
FORM_PUBLICS = ["Infirmiers", "Aides-soignants", "Équipes EHPAD", "HAD", "SSIAD", "Structures de soins", "Étudiants ou professionnels en perfectionnement"]
FORM_MODULES = [
    "Évaluation d’une plaie", "Plaies chroniques", "Ulcères de jambe",
    "Escarres : prévention et prise en charge", "Pied diabétique", "Choix raisonné des pansements",
    "Douleur et soins de plaies", "Traçabilité et transmissions", "Cas pratiques et analyse de situations",
]
FORM_FORMATS = ["Présentiel", "Visioconférence", "Atelier terrain", "Formation intra-établissement", "Audit + accompagnement"]

form_publics_tags = "\n".join(f'      <span class="pill-tag">{p}</span>' for p in FORM_PUBLICS)
form_modules_tiles = "\n".join(
    f'''      <div class="tile" style="border-radius:12px;padding:20px 22px"><span class="diamond"></span><span class="label">{m}</span></div>'''
    for m in FORM_MODULES
)
form_formats_rows = "\n".join(
    f'''      <div style="display:flex;align-items:center;gap:14px;padding:16px 4px;border-bottom:1px solid rgba(29,59,82,.1)">
        <span class="diamond" style="width:8px;height:8px"></span>
        <span style="font:500 16px 'Mulish',sans-serif;color:#284453">{fmt}</span>
      </div>''' for fmt in FORM_FORMATS
)

PAGES["formations"] = f'''
<section class="hero-section bordered">
  <div class="container" style="padding:clamp(48px,6vw,84px) 24px;max-width:820px">
    <div class="eyebrow">Formations</div>
    <h1 class="h1-page">Formations plaies &amp; cicatrisation</h1>
    <p class="body-text-lg" style="max-width:58ch">Renforcer les compétences des équipes autour de l’évaluation, du choix des soins et de la prévention des plaies chroniques.</p>
  </div>
</section>

<section class="container" style="padding:clamp(48px,6vw,72px) 24px">
  <div class="eyebrow" style="margin-bottom:20px">Publics</div>
  <div style="display:flex;flex-wrap:wrap;gap:12px">
{form_publics_tags}
  </div>
</section>

<section class="sage-band">
  <div class="container" style="padding:clamp(48px,6vw,80px) 24px">
    <div class="eyebrow">Modules possibles</div>
    <h2 style="margin:0 0 32px;font:400 clamp(26px,3.2vw,36px) 'Spectral',serif;color:#1D3B52">Des contenus adaptables à vos besoins</h2>
    <div class="grid grid-auto-260" style="gap:14px">
{form_modules_tiles}
    </div>
  </div>
</section>

<section class="container" style="padding:clamp(48px,6vw,80px) 24px">
  <div class="grid grid-auto-280" style="gap:40px;align-items:start">
    <div>
      <div class="eyebrow" style="margin-bottom:20px">Formats</div>
      <div style="display:flex;flex-direction:column;gap:2px">
{form_formats_rows}
      </div>
    </div>
    <div style="background:#1D3B52;border-radius:20px;padding:clamp(30px,4vw,44px);color:#EDE7DC">
      <h3 style="margin:0 0 14px;font:400 24px 'Spectral',serif;color:#F3EFE8">Organiser une formation</h3>
      <p style="margin:0 0 26px;font:400 15px/1.7 'Mulish',sans-serif;color:#B9C4CB">Vous souhaitez former une équipe ou construire un programme sur mesure pour votre structure ? Échangeons sur vos besoins et vos contraintes.</p>
      <a href="contact.html" style="background:#7C9A8B;color:#132833;border:none;border-radius:999px;padding:15px 28px;font:700 15px 'Mulish',sans-serif;cursor:pointer;display:inline-block">Demander une formation</a>
    </div>
  </div>
</section>
'''

page("formations.html", "formations.html", f"Formations — {SITE_TITLE}",
     "Formations plaies et cicatrisation pour infirmiers, aides-soignants, EHPAD, HAD, SSIAD et structures de soins.",
     PAGES["formations"])

# ============================================================= RESSOURCES
RESSOURCES_ARTICLES = [
    ("Plaie chronique : à partir de quand s’inquiéter ?",
     "Toute plaie qui ne progresse pas après plusieurs semaines mérite un regard attentif.",
     "Le délai attendu de cicatrisation dépend du type de plaie et du contexte médical. Lorsqu’une plaie stagne ou régresse malgré des soins réguliers, il est utile de réévaluer l’ensemble de la situation plutôt que de changer seulement de pansement.",
     "Une plaie qui n’évolue pas malgré des soins réguliers justifie une réévaluation globale."),
    ("Pourquoi une plaie ne cicatrise pas ?",
     "La cicatrisation est un processus qui peut être freiné par de multiples facteurs.",
     "Circulation, diabète, infection, pression, nutrition, douleur ou soins inadaptés : les causes de retard sont souvent multiples et intriquées. Les identifier est la première étape d’une stratégie efficace.",
     "Chercher la cause du retard est plus utile que multiplier les changements de pansement."),
    ("Ulcère de jambe : comprendre les causes",
     "Derrière un ulcère de jambe se cache presque toujours une cause vasculaire.",
     "Origine veineuse, artérielle ou mixte : la nature de l’atteinte oriente la prise en charge, notamment l’indication ou non d’une compression. Un bilan vasculaire est souvent nécessaire.",
     "L’origine vasculaire conditionne le traitement, dont l’éventuelle compression."),
    ("Escarre : prévention, signes d’alerte et prise en charge",
     "L’escarre est en grande partie évitable par une prévention adaptée.",
     "Mobilisation, positionnement, supports, nutrition et surveillance de la peau sont essentiels. Une rougeur qui ne blanchit pas est un signal d’alerte à prendre au sérieux.",
     "La prévention et la surveillance quotidienne de la peau sont déterminantes."),
    ("Pied diabétique : pourquoi la vigilance est essentielle",
     "Chez la personne diabétique, une plaie du pied peut évoluer rapidement.",
     "La perte de sensibilité et les troubles vasculaires masquent souvent la gravité. Toute plaie du pied chez une personne diabétique doit être évaluée sans attendre.",
     "Toute plaie du pied chez un patient diabétique impose une évaluation rapide."),
    ("Pansements : pourquoi il n’existe pas de solution universelle",
     "Le « bon pansement » dépend de la plaie, pas d’une habitude.",
     "Le choix se fonde sur le type de plaie, l’exsudat, la douleur, l’état de la peau et l’objectif du soin. Il doit être réévalué au fil de l’évolution.",
     "Le pansement se choisit selon la plaie et se réévalue régulièrement."),
    ("Douleur au changement de pansement : que peut-on faire ?",
     "La douleur au soin n’est pas une fatalité et peut être anticipée.",
     "Choix des matériaux, techniques de retrait, rythme des soins et mesures antalgiques adaptées permettent souvent de réduire nettement l’inconfort.",
     "La douleur au soin peut et doit être anticipée dans la stratégie de soin."),
    ("Nutrition et cicatrisation : quel lien ?",
     "La cicatrisation est aussi une question d’apports nutritionnels.",
     "Un déficit en protéines, en énergie ou en certains micronutriments peut ralentir la réparation tissulaire. L’état nutritionnel fait partie de l’évaluation globale.",
     "Un état nutritionnel altéré peut freiner la cicatrisation."),
    ("Compression veineuse : pourquoi elle est parfois indispensable",
     "Dans l’ulcère veineux, la compression est souvent le traitement de fond.",
     "Elle agit sur la cause du retard de cicatrisation. Son indication et ses modalités doivent être validées après un bilan vasculaire.",
     "Dans l’ulcère veineux, la compression traite la cause, après bilan vasculaire."),
]

ressources_articles_html = "\n".join(
    f'''    <article style="background:#FBF9F5;border:1px solid rgba(29,59,82,.1);border-radius:18px;padding:clamp(26px,3vw,40px);overflow:hidden">
      <div class="eyebrow" style="margin-bottom:14px">Article pédagogique</div>
      <h2 style="margin:0 0 14px;font:600 clamp(22px,2.6vw,28px)/1.25 'Spectral',serif;color:#1D3B52">{title}</h2>
      <p style="margin:0 0 14px;font:500 16.5px/1.6 'Mulish',sans-serif;color:#2C5169">{intro}</p>
      <p style="margin:0 0 22px;font:400 15.5px/1.75 'Mulish',sans-serif;color:#4A5860">{body}</p>
      <div class="retenir-box">
        <div class="retenir-label">À retenir</div>
        <p>{retenir}</p>
      </div>
      <p class="disclaimer-italic">Cet article ne remplace pas un avis médical personnalisé.</p>
    </article>''' for title, intro, body, retenir in RESSOURCES_ARTICLES
)

PAGES["ressources"] = f'''
<section class="hero-section bordered">
  <div class="container" style="padding:clamp(48px,6vw,84px) 24px;max-width:820px">
    <div class="eyebrow">Ressources</div>
    <h1 class="h1-page">Comprendre les plaies et la cicatrisation</h1>
    <p class="body-text-lg" style="max-width:60ch">Des repères pédagogiques pour patients, proches et soignants. Ces contenus sont informatifs et ne remplacent pas un avis médical personnalisé.</p>
  </div>
</section>

<section class="section-narrower" style="max-width:960px;margin:0 auto;padding:clamp(44px,6vw,72px) 24px">
  <div style="display:flex;flex-direction:column;gap:26px">
{ressources_articles_html}
  </div>
</section>
'''

page("ressources.html", "ressources.html", f"Ressources — {SITE_TITLE}",
     "Articles pédagogiques sur les plaies chroniques, ulcères, escarres, pied diabétique, pansements et cicatrisation.",
     PAGES["ressources"])

# ============================================================= CONTACT
CONTACT_PROFILS = ["Patient", "Proche", "Professionnel de santé", "Établissement", "Autre"]
contact_options = "\n".join(f'              <option>{p}</option>' for p in CONTACT_PROFILS)

PAGES["contact"] = f'''
<section class="hero-section bordered">
  <div class="container" style="padding:clamp(48px,6vw,80px) 24px;max-width:820px">
    <div class="eyebrow">Contact</div>
    <h1 class="h1-page">Prendre contact</h1>
    <p class="body-text-lg" style="max-width:56ch">Demander un avis, organiser une formation ou échanger sur une situation complexe : décrivez votre demande, une réponse vous sera apportée.</p>
  </div>
</section>

<section class="container grid grid-auto-300" style="padding:clamp(44px,6vw,72px) 24px;gap:clamp(28px,4vw,48px);align-items:start">
  <form class="contact-form" data-contact-form>
    <div class="form-row">
      <label class="form-field">
        <span>Nom</span>
        <input type="text" name="nom" autocomplete="family-name">
      </label>
      <label class="form-field">
        <span>Prénom</span>
        <input type="text" name="prenom" autocomplete="given-name">
      </label>
    </div>
    <div class="form-row">
      <label class="form-field">
        <span>Téléphone</span>
        <input type="tel" name="telephone" autocomplete="tel">
      </label>
      <label class="form-field">
        <span>Email</span>
        <input type="email" name="email" autocomplete="email">
      </label>
    </div>
    <label class="form-field">
      <span>Vous êtes</span>
      <select name="profil">
{contact_options}
      </select>
    </label>
    <label class="form-field">
      <span>Motif général</span>
      <input type="text" name="motif" placeholder="Avis spécialisé, formation, coordination…">
    </label>
    <label class="form-field">
      <span>Message court</span>
      <textarea name="message" rows="4"></textarea>
    </label>
    <button type="submit" class="btn-pill-primary" style="padding:15px 28px;margin-top:4px;border:none">Envoyer ma demande</button>
  </form>

  <div style="display:flex;flex-direction:column;gap:20px">
    <div class="alert-urgence">
      <h3 style="text-transform:uppercase;letter-spacing:.04em;font-size:13px;margin-bottom:10px">Urgence</h3>
      <p style="font-size:14.5px">Ce formulaire ne doit pas être utilisé pour une urgence médicale. En cas d’urgence ou d’aggravation rapide, contactez un professionnel de santé ou les services d’urgence.</p>
    </div>
    <div class="side-card">
      <h3>Confidentialité</h3>
      <p>Merci de ne pas transmettre de photographies de plaies ni de documents médicaux via ce formulaire. Les informations envoyées servent uniquement à répondre à votre demande.</p>
    </div>
    <div class="side-card">
      <h3>Coordonnées</h3>
      <div class="coord-list">
        <span>[Ajouter e-mail professionnel]</span>
        <span>[Ajouter téléphone]</span>
        <span>[Ajouter zone d’intervention]</span>
      </div>
    </div>
  </div>
</section>
'''

page("contact.html", "contact.html", f"Contact — {SITE_TITLE}",
     "Demander un avis spécialisé, organiser une formation ou échanger sur une situation complexe.",
     PAGES["contact"])

# ============================================================= MENTIONS LÉGALES
MENTIONS_BLOCKS = [
    ("Éditeur du site", "[Ajouter ici l’identité de l’éditeur, le statut professionnel, l’adresse professionnelle et les coordonnées de contact.]"),
    ("Hébergement", "[Ajouter ici le nom et les coordonnées de l’hébergeur du site.]"),
    ("Propriété intellectuelle", "L’ensemble des contenus de ce site (textes, visuels, identité graphique) est protégé. Toute reproduction sans autorisation est interdite."),
    ("Données personnelles", "Les informations transmises via le formulaire de contact sont utilisées uniquement pour répondre à votre demande. Conformément au RGPD, vous disposez d’un droit d’accès, de rectification et de suppression de vos données. [Ajouter ici les modalités d’exercice de ces droits.]"),
    ("Cookies", "[Préciser ici l’usage éventuel de cookies de mesure d’audience ou de fonctionnement, et les moyens de les paramétrer.]"),
    ("Accessibilité", "Ce site vise une lecture claire et accessible. [Ajouter ici les engagements et le niveau de conformité visé.]"),
]

mentions_blocks_html = "\n".join(
    f'''    <div style="padding:28px 0;border-bottom:1px solid rgba(29,59,82,.1)">
      <h2 style="margin:0 0 12px;font:600 20px 'Spectral',serif;color:#1D3B52">{title}</h2>
      <p style="margin:0;font:400 15.5px/1.75 'Mulish',sans-serif;color:#4A5860">{text}</p>
    </div>''' for title, text in MENTIONS_BLOCKS
)

PAGES["mentions"] = f'''
<section class="hero-section bordered">
  <div class="container" style="padding:clamp(48px,6vw,80px) 24px;max-width:820px">
    <div class="eyebrow">Informations légales</div>
    <h1 class="h1-page" style="font-size:clamp(30px,4vw,46px)">Mentions légales &amp; confidentialité</h1>
    <p style="margin:0;font:400 16px/1.75 'Mulish',sans-serif;color:#3E4A52;max-width:58ch">Les éléments ci-dessous sont à compléter avec les informations officielles avant la mise en ligne du site.</p>
  </div>
</section>

<section style="max-width:820px;margin:0 auto;padding:clamp(44px,6vw,72px) 24px">
  <div style="display:flex;flex-direction:column;gap:8px">
{mentions_blocks_html}
  </div>
  <p style="margin:32px 0 0;font:400 13px/1.7 'Mulish',sans-serif;color:#6A757D;font-style:italic">Ce site a une vocation informative. Il ne délivre pas de diagnostic en ligne et ne remplace pas une consultation ou un avis médical personnalisé.</p>
</section>
'''

page("mentions-legales.html", "mentions-legales.html", f"Mentions légales &amp; confidentialité — {SITE_TITLE}",
     "Mentions légales, hébergement, propriété intellectuelle, données personnelles, cookies et accessibilité.",
     PAGES["mentions"])





