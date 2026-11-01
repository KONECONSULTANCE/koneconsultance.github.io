"""
Carte agricole de la région de Bougouni (Mali) — découpage administratif 2023.

Les nouveaux cercles (loi n°2023-006 du 13 mars 2023, communes : loi n°2023-007)
sont reconstitués en fusionnant les anciennes communes (geoBoundaries MLI ADM3,
découpage 1999) selon la composition ci-dessous.

Usage :
    python scripts/carte_bougouni_agricole.py <dossier_donnees> <dossier_sortie>

<dossier_donnees> doit contenir :
    MLI-ADM1.geojson, MLI-ADM3.geojson  (geoBoundaries, gbOpen)
    ne_10m_admin_0_countries.geojson, ne_10m_rivers_lake_centerlines.geojson,
    ne_10m_roads.geojson                 (Natural Earth)
Dépendances : geopandas, matplotlib.
"""
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, FancyArrow
import matplotlib.patheffects as pe
from shapely.geometry import LineString, Point

DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("cartes")
OUT.mkdir(parents=True, exist_ok=True)
warnings.filterwarnings("ignore", message="Geometry is in a geographic CRS")

# ---------------------------------------------------------------------------
# 1. Composition des 10 cercles (57 communes) — noms des communes geoBoundaries
# ---------------------------------------------------------------------------
CERCLES = {
    "Bougouni": ["Bougouni Commune", "Danou", "Faradiele", "Faragouaran", "Keleya",
                 "Kokele", "Kola", "Kouroulamini", "Ouroun", "Sido", "Syen Toula",
                 "Tiemala Banimonotie", "Zantiebougou"],
    "Yanfolila": ["Bolo-Fouta", "Djallon-Foula", "Djiguiya De Koloni", "Gouanan",
                  "Gouandiaka", "Koussan", "Sere Moussa Ani Samo", "Wassoulou Balle",
                  "Yallankoro-Soloba"],
    "Kolondiéba": ["Kolondieba", "Mena", "N'golodiana", "Kebila", "Tousseguela", "Kolosso"],
    "Garalo": ["Garalo", "Bladie-Tiemala", "Defina", "Sibirila", "Yinindougou", "Yiridougou"],
    "Koumantou": ["Koumantou", "Debelin", "Domba", "Sanso", "Wola"],
    "Sélingué": ["Baya", "Tagandougou", "Sankarani", "Selefougou", "Kourouba",
                 "Tiakadougou Dialakoro", "Niagadina"],
    "Ouéléssébougou": ["Ouelessebougou", "Faraba", "Sanankoro Djitoumou"],
    "Kadiana": ["Kadiana", "Nangalasso", "Tiongui"],
    "Fakola": ["Fakola", "Bougoula", "Farako"],
    "Dogo": ["Dogo", "Meridiela"],
}
# Homonymes hors région à exclure (Faraba de Kéniéba, Bougoula de Kati)
HOMONYMES_LON_MIN = -8.7

# ---------------------------------------------------------------------------
# 2. Typologie agricole (dominante indicative par cercle)
# ---------------------------------------------------------------------------
ZONES = {
    "A": ("Coton – céréales (maïs, sorgho, mil) –\nélevage ; bassin cotonnier CMDT",
          "#E9C46A"),
    "B": ("Coton – maïs – anacarde – riz de bas-fonds ;\nzone soudano-guinéenne humide",
          "#8AB17D"),
    "C": ("Riz de bas-fonds et de plaine – anacarde –\nmangue – élevage (Wassoulou) ;\nforte pression de l'orpaillage",
          "#2A9D8F"),
    "D": ("Riz irrigué (périmètres de Sélingué /\nManinkoura) – pêche et pisciculture –\nmaraîchage",
          "#4D9DE0"),
    "E": ("Céréales sèches – maraîchage – arboriculture\nfruitière (mangue, agrumes) – élevage ;\nbassin d'approvisionnement de Bamako",
          "#E76F51"),
}
ZONE_CERCLE = {
    "Bougouni": "A", "Koumantou": "A", "Kolondiéba": "A", "Dogo": "A",
    "Garalo": "B", "Kadiana": "B", "Fakola": "B",
    "Yanfolila": "C", "Sélingué": "D", "Ouéléssébougou": "E",
}
PRODUCTIONS = {
    "Bougouni": "coton, maïs, sorgho, arachide, anacarde, karité, bovins",
    "Yanfolila": "riz, maïs, fonio, anacarde, mangue, bovins",
    "Kolondiéba": "coton, maïs, sorgho, arachide, karité, anacarde",
    "Garalo": "coton, maïs, riz bas-fonds, anacarde, mangue",
    "Koumantou": "coton, maïs, sorgho, mil, niébé, bovins",
    "Sélingué": "riz irrigué, poisson, maraîchage, banane",
    "Ouéléssébougou": "mil, sorgho, maïs, maraîchage, mangue, agrumes",
    "Kadiana": "coton, maïs, anacarde, riz bas-fonds, igname",
    "Fakola": "coton, maïs, anacarde, riz bas-fonds",
    "Dogo": "coton, maïs, sorgho, karité, petits ruminants",
}
CHEF_LIEU_COMMUNE = {
    "Bougouni": "Bougouni Commune", "Yanfolila": "Wassoulou Balle",
    "Kolondiéba": "Kolondieba", "Garalo": "Garalo", "Koumantou": "Koumantou",
    "Sélingué": "Baya", "Ouéléssébougou": "Ouelessebougou", "Kadiana": "Kadiana",
    "Fakola": "Fakola", "Dogo": "Dogo",
}

# ---------------------------------------------------------------------------
# 3. Données
# ---------------------------------------------------------------------------
adm3 = gpd.read_file(DATA / "MLI-ADM3.geojson")
adm1 = gpd.read_file(DATA / "MLI-ADM1.geojson")
pays = gpd.read_file(DATA / "ne_10m_admin_0_countries.geojson", bbox=(-12, 7, -3, 16))
rivers = gpd.read_file(DATA / "ne_10m_rivers_lake_centerlines.geojson", bbox=(-10, 9.5, -5, 13.5))
roads = gpd.read_file(DATA / "ne_10m_roads.geojson", bbox=(-10, 9.5, -5, 13.5))

adm3["rep_x"] = adm3.representative_point().x
rows = []
for cercle, communes in CERCLES.items():
    for c in communes:
        sel = adm3[(adm3.shapeName == c) & (adm3.rep_x > HOMONYMES_LON_MIN)]
        if len(sel) > 1:  # homonymes : garder la commune la plus proche du centre régional
            d = sel.representative_point().distance(Point(-7.6, 11.3))
            sel = sel.loc[[d.idxmin()]]
        if len(sel) != 1:
            raise SystemExit(f"Commune introuvable ou ambiguë : {c} ({len(sel)})")
        r = sel.iloc[0]
        rows.append({"cercle": cercle, "commune": c, "geometry": r.geometry})
communes = gpd.GeoDataFrame(rows, crs=adm3.crs)
assert len(communes) == 57, len(communes)

cercles = communes.dissolve(by="cercle", as_index=False)
cercles["zone"] = cercles.cercle.map(ZONE_CERCLE)
cercles["couleur"] = cercles.zone.map(lambda z: ZONES[z][1])
cercles["nb_communes"] = cercles.cercle.map(lambda c: len(CERCLES[c]))
cercles["superficie_km2"] = (cercles.to_crs(32629).area / 1e6).round(0).astype(int)
cercles["productions"] = cercles.cercle.map(PRODUCTIONS)
region = cercles.dissolve()

# export SIG
cercles[["cercle", "zone", "nb_communes", "superficie_km2", "productions", "geometry"]] \
    .to_file(OUT / "bougouni_cercles_2023.geojson", driver="GeoJSON")
communes.to_file(OUT / "bougouni_communes_2023.geojson", driver="GeoJSON")

# ---------------------------------------------------------------------------
# 4. Mise en page
# ---------------------------------------------------------------------------
plt.rcParams["font.family"] = "DejaVu Sans"
fig = plt.figure(figsize=(16.5, 11.7))  # A3 paysage
ax = fig.add_axes([0.035, 0.075, 0.585, 0.845])
xmin, ymin, xmax, ymax = region.total_bounds
pad = 0.12
ax.set_xlim(xmin - pad, xmax + pad)
ax.set_ylim(ymin - pad, ymax + pad)
ax.set_aspect(1 / 0.98)  # ~cos(11.4°)
ax.set_facecolor("#F4F1EA")

# Fond : pays voisins et autres régions
pays.plot(ax=ax, color="#ECE8DF", edgecolor="#9C9588", linewidth=1.2, zorder=1)
mali = pays[pays.ADM0_A3 == "MLI"]
mali.plot(ax=ax, color="#F7F5F0", edgecolor="none", zorder=1)
adm1.boundary.plot(ax=ax, color="#BDB6A8", linewidth=0.6, linestyle=(0, (4, 2)), zorder=2)

# Zones agricoles par cercle
cercles.plot(ax=ax, color=cercles.couleur, alpha=0.82, edgecolor="none", zorder=3)
communes.boundary.plot(ax=ax, color="white", linewidth=0.45, alpha=0.9, zorder=4)
cercles.boundary.plot(ax=ax, color="#3D3A35", linewidth=1.1, zorder=5)
region.boundary.plot(ax=ax, color="#1E1C19", linewidth=2.6, zorder=6)

# Isohyètes indicatives (pluviométrie moyenne annuelle)
iso = {1000: 12.30, 1100: 11.80, 1200: 11.20, 1300: 10.60}
for mm, lat in iso.items():
    xs = [xmin - pad, (xmin + xmax) / 2, xmax + pad]
    line = LineString([(xs[0], lat + 0.05), (xs[1], lat), (xs[2], lat - 0.07)])
    gx, gy = line.xy
    ax.plot(gx, gy, color="#3A6EA5", lw=1.0, ls=(0, (6, 3)), alpha=0.75, zorder=7)
    ax.text(xmax + pad - 0.02, lat - 0.05, f"{mm} mm", color="#3A6EA5", fontsize=8,
            ha="right", va="bottom", style="italic", zorder=7,
            path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])

# Hydrographie et routes
rivers.plot(ax=ax, color="#3A86C8", linewidth=1.6, zorder=8)
roads[roads.scalerank <= 5].plot(ax=ax, color="#7A3E2B", linewidth=1.1, zorder=8)
roads[roads.scalerank > 5].plot(ax=ax, color="#7A3E2B", linewidth=0.6, linestyle=(0, (2, 1.5)), zorder=8)

# Lac / barrage de Sélingué et périmètres irrigués
ax.scatter([-8.23], [11.64], marker="s", s=70, color="#1D5FA8", edgecolor="white", zorder=12)
ax.annotate("Barrage et lac\nde Sélingué", (-8.23, 11.64), xytext=(-8.62, 11.42), fontsize=8.5,
            color="#1D5FA8", fontweight="bold", zorder=12,
            arrowprops=dict(arrowstyle="-", color="#1D5FA8", lw=0.8),
            path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
ax.scatter([-8.30], [11.69], marker="*", s=140, color="#0B3C5D", edgecolor="white", zorder=12)

# Chefs-lieux et noms de cercles
for _, r in cercles.iterrows():
    cl = communes[communes.commune == CHEF_LIEU_COMMUNE[r.cercle]].iloc[0].geometry.representative_point()
    ax.scatter(cl.x, cl.y, s=36 if r.cercle != "Bougouni" else 90,
               marker="o" if r.cercle != "Bougouni" else "*", color="#1E1C19",
               edgecolor="white", linewidth=0.8, zorder=13)
    p = r.geometry.representative_point()
    if r.cercle in ("Sélingué",):
        p = Point(-8.05, 11.52)
    if r.cercle == "Bougouni":
        p = Point(-7.62, 11.55)
    ax.text(p.x, p.y, r.cercle.upper(), fontsize=11 if r.cercle == "Bougouni" else 9.5,
            fontweight="bold", ha="center", va="center", color="#1E1C19", zorder=14,
            path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    ax.text(p.x, p.y - 0.075, f"{r.superficie_km2:,} km²".replace(",", " "), fontsize=7.5,
            ha="center", va="center", color="#3D3A35", zorder=14,
            path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])

# Voisins
for txt, x, y in [("GUINÉE", -8.55, 10.45), ("CÔTE D'IVOIRE", -6.75, 10.18),
                  ("Région de\nKoulikoro", -8.45, 12.38), ("District de\nBamako", -7.98, 12.62),
                  ("Région de\nDioïla", -6.95, 12.25), ("Région de\nSikasso", -6.35, 11.55)]:
    if ax.get_xlim()[0] < x < ax.get_xlim()[1] and ax.get_ylim()[0] < y < ax.get_ylim()[1]:
        ax.text(x, y, txt, fontsize=8.5, color="#77706A", ha="center", va="center",
                style="italic", zorder=9)

# Graticule, échelle, nord
ax.tick_params(labelsize=7, colors="#77706A")
ax.set_xlabel("")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{abs(v):.1f}°O"))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}°N"))
ax.grid(color="#C9C2B4", lw=0.3, ls=":", zorder=0)
for s in ax.spines.values():
    s.set_color("#3D3A35")

x0, y0 = xmin - pad + 0.08, ymin - pad + 0.08
km_deg = 1 / (111.32 * 0.98)
for i in range(4):
    ax.add_patch(plt.Rectangle((x0 + i * 12.5 * km_deg, y0), 12.5 * km_deg, 0.022,
                               color="#1E1C19" if i % 2 == 0 else "white", ec="#1E1C19", lw=0.6, zorder=15))
for d in (0, 25, 50):
    ax.text(x0 + d * km_deg, y0 + 0.04, f"{d}", fontsize=7.5, ha="center", zorder=15)
ax.text(x0 + 50 * km_deg + 0.03, y0 + 0.004, "km", fontsize=7.5, zorder=15)
nx, ny = xmin - pad + 0.12, ymin - pad + 0.30
ax.add_patch(FancyArrow(nx, ny, 0, 0.16, width=0.035, head_width=0.09, head_length=0.08,
                        color="#1E1C19", zorder=15))
ax.text(nx, ny + 0.27, "N", ha="center", fontsize=12, fontweight="bold", zorder=15)

# ---------------------------------------------------------------------------
# 5. Titre, légende, tableau, encart, sources
# ---------------------------------------------------------------------------
fig.text(0.015, 0.965, "RÉGION DE BOUGOUNI — CARTE AGRICOLE", fontsize=21, fontweight="bold", color="#1E1C19")
fig.text(0.015, 0.937, "Dominantes agricoles par cercle · Découpage administratif 2023 "
         "(lois n°2023-006 et 2023-007) · 10 cercles, 57 communes",
         fontsize=11, color="#4A453F")

lx = 0.635
fig.text(lx, 0.905, "Systèmes de production dominants", fontsize=12.5, fontweight="bold")
handles = [Patch(facecolor=c, edgecolor="#3D3A35", alpha=0.85, label=f"{k}. {lab}") for k, (lab, c) in ZONES.items()]
leg1 = fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(lx - 0.005, 0.9), frameon=False,
                  fontsize=8.4, handlelength=2.2, handleheight=1.6, labelspacing=0.6)

sym = [
    Line2D([], [], color="#1E1C19", lw=2.6, label="Limite de la région de Bougouni"),
    Line2D([], [], color="#3D3A35", lw=1.1, label="Limite de cercle (2023)"),
    Line2D([], [], color="white", lw=2, label="Limite de commune", path_effects=[pe.withStroke(linewidth=3.2, foreground="#9C9588")]),
    Line2D([], [], color="#BDB6A8", lw=0.8, ls=(0, (4, 2)), label="Limite des anciennes régions"),
    Line2D([], [], marker="*", color="none", markerfacecolor="#1E1C19", markersize=12, label="Chef-lieu de région"),
    Line2D([], [], marker="o", color="none", markerfacecolor="#1E1C19", markersize=6, label="Chef-lieu de cercle (commune)"),
    Line2D([], [], color="#3A86C8", lw=1.6, label="Cours d'eau principal"),
    Line2D([], [], color="#7A3E2B", lw=1.1, label="Route principale / secondaire"),
    Line2D([], [], color="#3A6EA5", lw=1.0, ls=(0, (6, 3)), label="Isohyète indicative (mm/an)"),
    Line2D([], [], marker="s", color="none", markerfacecolor="#1D5FA8", markersize=7, label="Barrage hydro-agricole"),
    Line2D([], [], marker="*", color="none", markerfacecolor="#0B3C5D", markersize=10, label="Périmètre irrigué (Sélingué – Maninkoura)"),
]
fig.legend(handles=sym, loc="upper left", bbox_to_anchor=(lx - 0.005, 0.635), frameon=False,
           fontsize=8.3, ncol=2, columnspacing=1.2, labelspacing=0.6)

# Tableau des cercles
fig.text(lx, 0.455, "Cercles, communes et principales productions", fontsize=12.5, fontweight="bold")
tab = cercles.sort_values(["zone", "cercle"])
yy = 0.432
fig.text(lx, yy, "Cercle", fontsize=8.3, fontweight="bold")
fig.text(lx + 0.083, yy, "Comm.", fontsize=8.3, fontweight="bold")
fig.text(lx + 0.115, yy, "km²", fontsize=8.3, fontweight="bold")
fig.text(lx + 0.150, yy, "Productions principales", fontsize=8.3, fontweight="bold")
for _, r in tab.iterrows():
    yy -= 0.0225
    fig.patches.append(plt.Rectangle((lx, yy - 0.003), 0.008, 0.014, transform=fig.transFigure,
                                     color=r.couleur, figure=fig))
    fig.text(lx + 0.012, yy, r.cercle, fontsize=8.3)
    fig.text(lx + 0.090, yy, str(r.nb_communes), fontsize=8.3)
    fig.text(lx + 0.112, yy, f"{r.superficie_km2:,}".replace(",", " "), fontsize=8.3)
    fig.text(lx + 0.150, yy, r.productions, fontsize=8.0, color="#3D3A35")
yy -= 0.025
tot = cercles.superficie_km2.sum()
fig.text(lx + 0.012, yy, "Total région", fontsize=8.3, fontweight="bold")
fig.text(lx + 0.090, yy, "57", fontsize=8.3, fontweight="bold")
fig.text(lx + 0.112, yy, f"{tot:,}".replace(",", " "), fontsize=8.3, fontweight="bold")

# Encart Mali
ins = fig.add_axes([0.875, 0.775, 0.115, 0.17])
mali_adm = adm1
mali_adm.plot(ax=ins, color="#ECE8DF", edgecolor="#9C9588", linewidth=0.4)
region.plot(ax=ins, color="#C0392B", edgecolor="#7B241C", linewidth=0.6)
ins.set_axis_off()
ins.set_title("Localisation au Mali", fontsize=8.5, color="#4A453F")

# Notes et sources
notes = (
    "Notes : les limites des cercles 2023 sont reconstituées par agrégation des communes de 1999 (geoBoundaries) selon la composition "
    "des lois n°2023-006/007 ; elles restent indicatives\n"
    "en l'absence de limites officielles numérisées. Les dominantes agricoles et isohyètes sont des synthèses qualitatives "
    "(zone cotonnière CMDT, aménagements de Sélingué, normales pluviométriques) à valider avec les données DRA/CPS-SDR.\n"
    "Sources : geoBoundaries (MLI ADM1/ADM3, CC BY 4.0) · Natural Earth (cours d'eau, routes, frontières) · "
    "Lois n°2023-006 et 2023-007 du 13 mars 2023 · Réalisation : Kone Consultance, novembre 2026 · Projection : WGS 84"
)
fig.text(0.015, 0.012, notes, fontsize=7.2, color="#5A544D", va="bottom", linespacing=1.45)

for ext in ("png", "pdf"):
    fig.savefig(OUT / f"carte_agricole_region_bougouni_2023.{ext}", dpi=220, facecolor="white")
print(cercles[["cercle", "zone", "nb_communes", "superficie_km2"]].to_string(index=False))
print("Total", tot)
