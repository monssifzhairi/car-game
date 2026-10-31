# Blender script — Import ay l7oma f l'Maghrib b 1 click
# Kifach tst3mlo: F Blender → Text Editor → Open had file → Run Script
# Y7taj Blosm addon installé (Edit → Preferences → Add-ons → Blosm)

import bpy

# === BDEL HNA COORDINATES DYAL L7OMA DYALK ===
# Ex: Mehdia, Hay Salam, Kenitra Centre...
LAT = 34.2553  # Mehdia default
LON = -6.6575
SIZE_METERS = 1000  # 600=s7ira, 1000=motawassita, 1800=kbira

# === Import via Blosm ===
# Blosm lazem ikon activé
try:
    # N7awlo n3ayto l operator dyal Blosm
    # Ila ma khdamch, dirha manual: N-panel → Blosm → set lat/lon → Import
    d_lat = SIZE_METERS / 111000
    d_lon = SIZE_METERS / (111000 * 0.839)  # approx for Morocco lat 34

    bpy.ops.blosm.import_data(
        data_type='osm',
        osm_source='server',
        lat=str(LAT),
        lon=str(LON),
        radius=str(SIZE_METERS/2),
        buildings=True,
        highways=True,
        water=True
    )
    print(f"✅ Import OSM kamal: lat={LAT}, lon={LON}, size={SIZE_METERS}m")
except Exception as e:
    print(f"⚠️ Auto-import fail: {e}")
    print("👉 Dirha manual: N → Blosm → kteb lat/lon → Import")
    print(f"   lat={LAT}, lon={LON}, radius={SIZE_METERS/2}")

# === T9ad lmaterials bach iwelli low-poly game-friendly ===
for mat in bpy.data.materials:
    # 7awl kolchi l flat shading style Cap Sirocco
    if mat.use_nodes:
        mat.use_nodes = False
    # loun 7asab smiya?
    # buildings = beige, roads = dark grey
    name = mat.name.lower()
    if "building" in name or "wall" in name:
        mat.diffuse_color = (0.91, 0.89, 0.84, 1.0)
    elif "road" in name or "highway" in name:
        mat.diffuse_color = (0.23, 0.24, 0.27, 1.0)
    elif "sidewalk" in name:
        mat.diffuse_color = (0.29, 0.30, 0.33, 1.0)

# === Ncree collection jdida ===
if "L7OMA_3D" not in bpy.data.collections:
    col = bpy.data.collections.new("L7OMA_3D")
    bpy.context.scene.collection.children.link(col)

print("🎮 Daba dir: File → Export → glTF 2.0 (.glb) → 7etha f Godot!")
