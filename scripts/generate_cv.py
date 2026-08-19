# Génère assets/cv/CV-Sidi-Kone.pdf à partir du CV officiel (Sidi_KONE_CV_2026_Professionnel.docx).
# Usage : python scripts/generate_cv.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

OLIVE = colors.HexColor("#2F3E28")
SIENNA = colors.HexColor("#A85C32")
TEXT = colors.HexColor("#24291F")
SOFT = colors.HexColor("#52584A")

styles = getSampleStyleSheet()

name_style = ParagraphStyle("Name", parent=styles["Title"], fontName="Times-Bold",
                             fontSize=22, textColor=OLIVE, spaceAfter=2, alignment=TA_LEFT)
title_style = ParagraphStyle("SubTitle", parent=styles["Normal"], fontName="Helvetica",
                              fontSize=11, textColor=SIENNA, spaceAfter=6)
contact_style = ParagraphStyle("Contact", parent=styles["Normal"], fontName="Helvetica",
                                fontSize=9, textColor=SOFT, spaceAfter=12)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Times-Bold", fontSize=13,
                     textColor=OLIVE, spaceBefore=14, spaceAfter=6)
h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=10,
                     textColor=SIENNA, spaceBefore=8, spaceAfter=4)
body = ParagraphStyle("Body", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5,
                       textColor=TEXT, leading=13.5, spaceAfter=4)
job_title = ParagraphStyle("JobTitle", parent=styles["Normal"], fontName="Helvetica-Bold",
                            fontSize=10.5, textColor=OLIVE, spaceAfter=1)
job_meta = ParagraphStyle("JobMeta", parent=styles["Normal"], fontName="Helvetica-Oblique",
                           fontSize=9, textColor=SIENNA, spaceAfter=4)
bullet = ParagraphStyle("Bullet", parent=body, leftIndent=10, bulletIndent=0, spaceAfter=2)
degree_year = ParagraphStyle("DegreeYear", parent=styles["Normal"], fontName="Helvetica-Bold",
                              fontSize=10, textColor=SIENNA)
degree_body = ParagraphStyle("DegreeBody", parent=body, spaceAfter=0)

doc = SimpleDocTemplate(
    "assets/cv/CV-Sidi-Kone.pdf",
    pagesize=A4,
    topMargin=16 * mm,
    bottomMargin=14 * mm,
    leftMargin=18 * mm,
    rightMargin=18 * mm,
    title="CV - Sidi Kone",
    author="Sidi Kone",
)

story = []

story.append(Paragraph("Sidi Koné", name_style))
story.append(Paragraph("Expert en développement rural, sécurité alimentaire et action humanitaire", title_style))
story.append(Paragraph("Bougouni, Mali &nbsp;|&nbsp; +223 78 50 49 67 &nbsp;|&nbsp; sidi.kone@ymail.com &nbsp;|&nbsp; Nationalité malienne", contact_style))
story.append(HRFlowable(width="100%", thickness=1.2, color=SIENNA, spaceAfter=8))

# Profil
story.append(Paragraph("Profil professionnel", h2))
story.append(Paragraph(
    "Expert en développement rural fort de plus de 28 années d'expérience dans le secteur de la "
    "sécurité alimentaire et nutritionnelle, tant à travers des interventions d'urgence humanitaire "
    "que des projets et programmes de promotion d'une agriculture et de systèmes alimentaires "
    "durables, sensibles à la nutrition et résilients aux effets du changement climatique.", body
))
story.append(Paragraph(
    "Compétences avérées en gestion de projets intégrés à activités diversifiées, pour le compte "
    "d'organisations non gouvernementales nationales et internationales, y compris des agences du "
    "système des Nations Unies réunies en consortium pour la conduite de projets conjoints.", body
))
story.append(Paragraph(
    "Grande capacité à collaborer avec les organisations paysannes, féminines et de jeunesse afin "
    "d'analyser leurs contraintes socio-économiques et besoins spécifiques, et d'y apporter des "
    "solutions adaptées en valorisant la participation, l'inclusion et la mobilisation des ressources "
    "internes des communautés cibles.", body
))
story.append(Paragraph(
    "Expérience confirmée de collaboration avec les collectivités locales et les partenaires au "
    "développement, à travers la conduite d'études monographiques et de diagnostics participatifs "
    "ayant alimenté plusieurs plans et programmes de développement régional et local.", body
))

# Distinctions
story.append(Paragraph("Distinctions et reconnaissance professionnelle", h2))
story.append(Paragraph(
    "• Certificat de reconnaissance d'expertise professionnelle — Organisation des Nations Unies "
    "pour l'Alimentation et l'Agriculture (FAO), juillet 2026 : reconnu comme Spécialiste de "
    "référence de l'approche des Clubs d'écoute communautaire Dimitra au Mali et en Afrique de "
    "l'Ouest (mars 2016 – décembre 2025) ; a représenté le Mali lors de rencontres internationales "
    "des spécialistes Dimitra (République démocratique du Congo, Niger).", bullet
))
story.append(Paragraph(
    "• Employee Recognition Award — « 100 Young and 100 Young at Heart », FAO (2022).", bullet
))

# Domaines d'expertise
story.append(Paragraph("Domaines d'expertise", h2))

story.append(Paragraph("Sécurité alimentaire, agriculture durable &amp; résilience", h3))
for s in [
    "Suivi et coordination de projets intégrés de sécurité alimentaire et nutritionnelle, de "
    "réconciliation et de cohésion sociale, avec un accent particulier sur le genre et les personnes "
    "à besoins spécifiques (personnes déplacées internes, retournées, vivant avec un handicap).",
    "Distribution et suivi des intrants et outils agricoles ; conduite d'interventions d'urgence et "
    "de projets d'agriculture durable sensible à la nutrition, intégrant l'approche des banques "
    "alimentaires.",
    "Maraîchage sensible à la nutrition et promotion des bio-fertilisants et bio-pesticides.",
    "Approche des caisses de résilience communautaire : champs écoles agropastoraux (volet "
    "technique), associations villageoises d'épargne et de crédit (volet financier), transferts "
    "monétaires, fonds de contingence et Clubs Dimitra (volet social).",
]:
    story.append(Paragraph("• " + s, bullet))

story.append(Paragraph("Engagement communautaire &amp; approches participatives", h3))
for s in [
    "Expert-formateur en approche de développement des Clubs d'écoute communautaire Dimitra.",
    "Diagnostics participatifs — Méthode Active de Recherche Participative (MARP).",
    "Animation de champs écoles agropastoraux.",
]:
    story.append(Paragraph("• " + s, bullet))

story.append(Paragraph("Suivi-évaluation, données &amp; outils", h3))
for s in [
    "Transferts monétaires en situation d'urgence.",
    "Système d'information géographique — production de cartes thématiques sous QGIS.",
    "Analyse de données statistiques : R, SPSS, STATA.",
    "Outils bureautiques : Word, Excel, PowerPoint, Outlook, Internet.",
]:
    story.append(Paragraph("• " + s, bullet))

# Expériences
story.append(Paragraph("Expérience professionnelle", h2))
experiences = [
    ("Assistant Agronome", "Sous-bureau de la FAO — Mopti, Mali",
     "15 avril 2015 – 31 décembre 2025 (10 ans et 8 mois)",
     ["Suivre et coordonner la mise en œuvre de projets d'urgence, de résilience et de développement "
      "dans les domaines de la sécurité alimentaire et nutritionnelle, l'agriculture, l'élevage, la "
      "pêche, la foresterie, ainsi que la prévention et la gestion des conflits liés aux ressources "
      "naturelles.",
      "Apporter un appui technique aux partenaires de mise en œuvre de la FAO (ONG et services "
      "techniques) dans la conduite et le suivi des projets.",
      "Participer à la gestion du sous-bureau de Mopti et au rapportage des activités.",
      "En tant que point focal national, former les équipes des ONG partenaires, les collectivités, "
      "les radios communautaires et les leaders communautaires à l'approche des Clubs d'écoute "
      "Dimitra.",
      "Assurer la gestion de la petite caisse de fonctionnement du sous-bureau de Mopti.",
      "Représenter le Mali lors de rencontres internationales des spécialistes de l'approche Dimitra "
      "en Afrique."]),
    ("Responsable du volet Agriculture", "Plan d'Action de Développement Intégré (PADI) — Sadiola, Mali",
     "3 janvier 2011 – 12 avril 2015 (4 ans et 3 mois)",
     ["Planifier, mettre en œuvre et suivre les activités du volet Agriculture : aménagements "
      "hydro-agricoles, maraîchage, riziculture de bas-fond, production de semences vivrières, "
      "arboriculture, agroforesterie, gestion des coopératives de producteurs de semences.",
      "Assurer le rapportage des activités du volet Agriculture.",
      "Gérer le déploiement du matériel agricole du programme (tracteurs et batteuses).",
      "Appuyer la gestion administrative du bureau du PADI."]),
    ("Agent de Développement Communautaire",
     "Groupe de Recherche et de Réalisations pour le Développement Rural (GRDR) — Kayes, Mali",
     "1er avril 2008 – 2 janvier 2011 (2 ans et 9 mois)",
     ["Participer à la mise en œuvre des activités du programme : aménagements hydro-agricoles, "
      "maraîchage, riziculture de bas-fond, cultures sèches, agroforesterie, protection de "
      "l'environnement, aviculture, élevage de petits ruminants, appui aux organisations de base et "
      "aux instances de concertation communales.",
      "Contribuer aux monographies et aux plans de développement des communes.",
      "Assurer le suivi rapproché des activités de terrain et le rapportage mensuel du programme.",
      "Appuyer les initiatives individuelles et collectives de développement local et accompagner "
      "techniquement les collectivités communales."]),
    ("Animateur de Développement Rural", "Croix-Rouge Malienne (CRM) — Kayes, Mali",
     "15 septembre 2007 – 30 mars 2008 (6 mois et 15 jours)",
     ["Appuyer la mise en œuvre d'activités génératrices de revenus pour les organisations féminines : "
      "production, conservation et transformation de légumes, promotion des PMI/PME, crédit "
      "solidaire couplé à un programme d'alphabétisation fonctionnelle.",
      "Mettre en relation les organisations féminines cibles du projet et les institutions de "
      "microfinance.",
      "Gérer le partenariat avec les services techniques et les collectivités.",
      "Assurer le suivi rapproché et le rapportage périodique des activités."]),
    ("Animateur de Développement Rural", "Association Malienne pour le Développement (AMADE) — Kayes, Mali",
     "1er janvier 1997 – 31 décembre 2006 (10 ans)",
     ["Participer à la mise en œuvre des activités du programme : maraîchage, boutiques et moulins "
      "communautaires, crédit solidaire, hydraulique villageoise, hygiène et assainissement, soins "
      "de santé primaires, gestion des CSCOM/ASACO, service juridique en milieu rural, PMI/PME, "
      "alphabétisation fonctionnelle.",
      "Apporter un appui technique aux collectivités communales des zones d'intervention du projet.",
      "Assurer le suivi rapproché et le rapportage mensuel des activités."]),
    ("Technicien de Recherche Agronomique", "ICRISAT / CIRAD — Samanko, Bamako, Mali",
     "17 juin – 31 octobre 1996 (4 mois et 14 jours)",
     ["Conduire des essais agronomiques et gérer le déploiement des équipes sur les parcelles "
      "expérimentales.",
      "Appuyer les publications et autres activités scientifiques du centre."]),
    ("Volontaire",
     "Cellule d'Aménagement du Territoire / Gestion des Ressources Naturelles (CAT/GRN) — Sikasso, Mali",
     "1er janvier – 30 mars 1996 (3 mois)",
     ["Faciliter la communication entre l'équipe du projet et les populations bénéficiaires.",
      "Appuyer la mise en œuvre d'infrastructures agropastorales (micro-barrages, parcs de "
      "vaccination, marchés à bétail) selon une approche intégrée, participative et inclusive."]),
]
for title, org, dates, bullets in experiences:
    story.append(Paragraph(title, job_title))
    story.append(Paragraph(org + " — " + dates, job_meta))
    for b in bullets:
        story.append(Paragraph("• " + b, bullet))
    story.append(Spacer(1, 4))

# Formation académique
story.append(Paragraph("Formation académique", h2))
degrees = [
    ("2024", "Master 2 Coopération Internationale et Aide Humanitaire (MCIAH) — KALU Institute, Madrid, Espagne"),
    ("2024", "Master 2 Planification Territoriale, Environnementale et Développement Durable (PTED) — Université DELTA C, Bamako, Mali"),
    ("2023", "Master 2 Management et Gestion des Projets & Programmes — Institut Sciences Campus, Ouagadougou, Burkina Faso"),
    ("2022", "Master 1 Facilitation et Conseils pour les Processus de Développement (FCPD) — Université DELTA C, Bamako, Mali"),
    ("2018", "Licence Professionnelle Gestion Technique de l'Environnement (LGTE) — Université Mandé Boukary (UMB), Bamako, Mali"),
    ("1995", "Diplôme de Technicien Supérieur en Agriculture (DTSA) — IPR/IFRA, Katibougou, Mali"),
]
rows = [[Paragraph(y, degree_year), Paragraph(d, degree_body)] for y, d in degrees]
t = Table(rows, colWidths=[16 * mm, None])
t.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
]))
story.append(t)

# Formations complémentaires et certifications professionnelles
story.append(Paragraph("Formations complémentaires et certifications professionnelles", h2))

story.append(Paragraph("Aide humanitaire, transferts monétaires &amp; suivi-évaluation", h3))
for s in [
    "2026 : Analyse de données statistiques — R, SPSS, STATA.",
    "2023 : Diplôme d'expert en Transferts Monétaires en situation d'urgence (144 h, e-learning) — "
    "Kalu Institute, Espagne.",
    "2023 : Suivi & Évaluation des projets humanitaires — IDH International-Mali, Bamako.",
    "2023 : Atelier sur l'engagement communautaire des Clubs Dimitra dans la localisation de l'aide "
    "— FAO, Niamey, Niger.",
    "2015 : Gestion axée sur les résultats et Suivi & Évaluation des projets et programmes — "
    "Programme Alimentaire Mondial (PAM), Mopti.",
]:
    story.append(Paragraph("• " + s, bullet))

story.append(Paragraph("Approches communautaires &amp; agriculture", h3))
for s in [
    "2017 : Animation des champs écoles agropastoraux — FAO / Direction nationale de l'Agriculture, San.",
    "2016 : Approche des Clubs d'écoute communautaire Dimitra — FAO Mali.",
    "2014 : Gestion de l'eau et des ouvrages (aménagements hydro-agricoles) en irrigation de "
    "proximité — Direction Régionale du Génie Rural, Kayes.",
    "2012 : Techniques culturales du riz de bas-fond — PADI, Sadiola.",
    "2008 : Élaboration et gestion des projets — GRDR, Sélibabi, Mauritanie.",
]:
    story.append(Paragraph("• " + s, bullet))

story.append(Paragraph("Environnement, information géographique &amp; gestion de l'information", h3))
for s in [
    "2016 : Système d'Information Géographique / Cartographie — IAVS, Burkina Faso.",
    "2016 : Gestion de l'Information (Excel & KoBo Collect) — OCHA, Mopti.",
    "2016 : Développement durable, un levier de croissance ; Gouvernance territoriale ; Du manager "
    "au leader agile ; Gestion de crise ; Comptabilité de gestion et pratique du tableur — France "
    "Université Numérique (FUN).",
]:
    story.append(Paragraph("• " + s, bullet))

story.append(Paragraph("Gouvernance, développement communautaire &amp; divers", h3))
for s in [
    "2005 : Élaboration des plans d'action et stratégies de lobby pour la sécurité alimentaire ; "
    "décentralisation et cadre stratégique de lutte contre la pauvreté — AMADE.",
    "2004 : Planification – Suivi – Évaluation des projets et programmes — AMADE.",
    "2003 : Prévention des IST/VIH-SIDA — Hôpital Régional de Kayes.",
    "2002 : Processus électoral — AMADE.",
    "1998 : Para-juridisme rural — AMADE.",
    "1998 : Hygiène et assainissement — Direction Régionale de la Santé, Kayes.",
    "1997 : Transcription en langue nationale bambara — Académie d'enseignement de Kayes.",
]:
    story.append(Paragraph("• " + s, bullet))

story.append(Paragraph("Stages", h3))
for s in [
    "1995 : Stage de fin de cycle (9 mois) — ICRISAT/CIRAD, Samanko : identification et "
    "caractérisation du comportement photopériodique de 13 cultivars de sorgho.",
    "1992 : Stage (45 jours) — CMDT, Kadiana : dressage des bœufs de trait et alphabétisation "
    "fonctionnelle.",
]:
    story.append(Paragraph("• " + s, bullet))

story.append(Spacer(1, 8))
story.append(Paragraph("Références professionnelles disponibles sur demande.", body))

doc.build(story)
print("CV généré : assets/cv/CV-Sidi-Kone.pdf")
