# microsint

Estimation de la **distance** et de l'**angle relatif** d'usagers vulnérables (piétons, vélos, trottinettes) à partir d'images panoramiques 360°, couplée aux pièces **CAD** du boîtier GNSS embarqué utilisé pour la collecte terrain.

---

## Pièces CAD

Deux pièces STEP décrivent le boîtier d'acquisition GNSS monté sur la plateforme mobile.

| Pièce | Fichier | Aperçu |
|---|---|---|
| Boîtier GNSS (couvercle + composants) | [CAD_pieces/gnss_box.step](CAD_pieces/gnss_box.step) | ![gnss_box](CAD_pieces/gnss_box.svg) |
| Socle (bottom box) | [CAD_pieces/bottom_box.step](CAD_pieces/bottom_box.step) | ![bottom_box](CAD_pieces/bottom_box.svg) |

> Les `.step` s'ouvrent dans FreeCAD, Fusion 360, OnShape, SolidWorks, etc. Les `.svg` sont rendus via `cadquery` pour prévisualisation.

---

## Structure du dépôt

```
.
├── CAD_pieces/                    # Modèles 3D STEP du boîtier GNSS
├── Bikes_relative_position/       # Estimation distance/angle — vélos
├── Escooter_relatvie_position/    # Estimation distance/angle — trottinettes
└── Pedestrian_relative_position/  # Estimation distance/angle — piétons
    └── Experiment_FUSE/           # Jeu d'entraînement/test fusionné
```

Chaque dossier *relative_position* contient :
- un notebook `*_model_developpment.ipynb` — développement et entraînement du modèle ;
- un script `*_distance.py` — API `get_ang_dist_<classe>(c_x, c_y)` utilisée en inférence ;
- deux modèles `joblib` : `distance_predictor_small` (courte portée) et `distance_predictor_big` (longue portée) ;
- un modèle d'angle `angle_predictor*` ;
- des données d'entraînement / validation (`*_data.csv`, `validation/`).

---

## Principe

L'image panoramique source fait **5376 px de large** (360°). Pour chaque usager détecté, on fournit sa position pixel `(c_x, c_y)` dans l'image ; le pipeline renvoie :

- **angle relatif** par rapport à l'avant du véhicule (`-180°` … `+180°`),
- **distance** en mm (basculement automatique entre un modèle *short-range* et *long-range* selon un seuil de ~1 m).

L'image est découpée en segments (4 pour vélos/trottinettes, 8 pour piétons) pour linéariser la régression et gérer les symétries avant/arrière/gauche/droite.

```python
from Bikes_relative_position.bike_distance import get_ang_dist_bike

angle_deg, dist_mm = get_ang_dist_bike(c_x=1200, c_y=850)
```

> ⚠️ Les chemins `joblib.load(...)` dans les scripts pointent vers un emplacement local absolu (`/Users/.../PhD/Position_Estimation/...`). À adapter avant exécution sur une autre machine.

---

## Installation

```bash
conda create -n microsint python=3.11
conda activate microsint
pip install pandas scikit-learn joblib numpy
# pour régénérer les aperçus SVG des pièces CAD :
pip install cadquery
```

## Régénérer les aperçus CAD

```bash
python - <<'PY'
import cadquery as cq
from cadquery import exporters
for name in ("bottom_box", "gnss_box"):
    wp = cq.importers.importStep(f"CAD_pieces/{name}.step")
    exporters.export(wp, f"CAD_pieces/{name}.svg",
                     opt={"width": 900, "height": 600,
                          "projectionDir": (0.5, -0.8, 0.6)})
PY
```

---

## Licence

Usage de recherche — contacter l'auteur pour toute réutilisation.
