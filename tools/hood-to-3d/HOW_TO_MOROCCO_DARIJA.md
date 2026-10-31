# Kifach t7awl l7oma dyalk l 3D — Tari9a sahla 100% fabor

**L7oma → 3D → Godot game** — bla flous, bla drone, ghir b Blender + data 7a9i9iya mn OpenStreetMap.

> Hadchi li darti nta f Mehdia v4.1 (screenshots li 3ndek) rah **nafs tari9a** li ghadi ndiro l ay blasa f l'Maghrib.

---

## 0. Ach 3ndek deja? (Mzyan bzaf!)

F screenshots dyalk:

- `mehdia_v4_1_topdown.png` + `mehdia_v4_1_angled.png` = **Mehdia kamla 3D** f Blender
- Collections: `V2_ROADS`, `Road_Network`, `Sidewalk_Netw`, `V2_BUILDINGS` (m9sma mzyan!)
- `Map_Ground` = l'ard kbira

Hadi hiya 80% dial lkhdma. Ba9i ghir t7awlha l Godot.

---

## 1. Tari9a 1 — L3adia (OSM → Blender) — **Kan-ns7k biha**

Hadi li khdama 3ndek daba, o khdama l ay mdina:

### Chno khask:
- Blender (free) — https://blender.org
- Addon **Blosm** (free, open source) — https://github.com/vvoovv/blosm

### Khotowat:
1. **Satel Blender** → `Edit → Preferences → Add-ons → Install` → khtar `blosm.zip` → ✓ activate
2. F 3D Viewport, cliqui `n` → ghadi tchouf onglet **Blosm** 3la limen
3. 7et **coordinates** dyal l7oma dyalk:
   - Sir l https://www.openstreetmap.org
   - 9elleb 3la l7oma dyalk → clic droit → "Show address" → ghadi tchouf lat/lon
   - Wla khoud mn Google Maps: clic droit 3la blasa → copy coordinates
4. F Blosm: `Extent` = coordinates, `Mode` = `3D` → cocher `Buildings` + `Highways` + `Water` ila kayn b7ar
5. Cliquer **Import** → ghadi ijik nafs Mehdia v4: tri9an ka curves + buildings extrudés
6. Sauvegarder `.blend` → Export `File → Export → glTF 2.0 (.glb)`

> **Nasi7a:** Ila kan OSM khawi f l7oma dyalk (ma kayninch buildings), t9der tzidhom nta f openstreetmap.org → `Edit` → rsm buildings → Save. Mn ba3d t9der t-importihom 3awtani.

---

## 2. Tari9a 2 — Photogrammétrie (Telephone / Drone)

Ila bghiti **dar dyalk b debt** b textures 7a9i9iya:

- Sawwar b telephone 40-60 sora dayr 3la dar (walk around)
- Software free: **Meshroom** (AliceVision) — https://alicevision.org
- Import images → Meshroom i7seb 3D mesh → export OBJ → Blender clean-up → Godot

*Mo9arana:* Tari9a 1 = l7oma kamla low-poly (mzyan l game). Tari9a 2 = dar wa7da b detail 3ali.

---

## 3. Mn Blender → Godot 4 (tsog fiha!)

1. F Blender: select `Map_Ground + Road_Network + Buildings` → `File → Export → glTF (.glb)` → ✓ `Apply Modifiers`
2. F Godot 4: 7et `.glb` f `res://game/assets/mehdia/`
3. Godot ghadi i-cree scene automatic. Zid:
   ```
   - StaticBody3D (l Map_Ground)
     - CollisionShape3D → create Trimesh Collision
   - Car (VehicleBody3D) → zid f nafs scene
   - CameraRig (SpringArm3D)
   ```
4. Dir `F5` → tsog! 🚗

**Perf tip GTX 960M:** Buildings → `MultiMeshInstance3D` ila >500, roads → merge mesh, textures 1024 max.

---

## 4. Viewer li saybt lik daba

F `tools/hood-to-3d/index.html` kayn preview live:

- Khtar ay blasa f l'Maghrib (presets: Mehdia, Kenitra, Rabat, Casa...)
- Wla kteb smiya o dir "9elleb"
- Chouf preview 3D direct f browser (b7al Mehdia screenshots)
- Boutons: Top View / 3D Angled / Street View / Wireframe
- Screenshot + Export info l Godot

**Lien preview:** khdem f Arena — sir l port 8000 preview.

---

## 5. Bghiti ndirha ana kamla lik?

Sift liya:

- Smiya dyal l7oma wla link Google Maps
- Wla file `.blend` dyal Mehdia v4.1 (ila bghiti n7awlha direct l Godot playable)

O ana nsayb lik `.glb` wajd + `mehdia.tscn` wajda tsog fiha.

---

## 6. Questions fréquentes (Darija)

**Wach OSM fih kolchi?** — Lmodon lkbar (Rabat/Casa/Kenitra/Mehdia) 3amrin mzyan. Dowarat sghar 9der ikon na9es — t9der tkmlo nta.

**Wach lazem drone?** — La. Tari9a 1 bla ta sora.

**Wach free 100%?** — Oui. Blender + Blosm + OSM + Godot = 0 DH. Kolchi CC0/MIT.

**Wach n9der nbi3 l-game?** — Oui, OSM data = ODbL (khask t-mentioner "© OpenStreetMap contributors"), o Blosm = GPL, o assets dyalk. Ma kayn ta mochkil commercial.

---

*Dirha o sifet liya screenshot dyal l7oma dyalk f 3D — nchoufha!*
