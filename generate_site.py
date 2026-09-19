from pathlib import Path
import json
from string import Template
from urllib.parse import quote


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_FILE = BASE_DIR / "templates" / "index_template.html"
DATA_FILE = BASE_DIR / "data.json"
OUT_DIR = BASE_DIR / "dist"
OUT_FILE = OUT_DIR / "index.html"


def flatten(data: dict) -> dict:
    """
    Zanořené dict -> plochý dict s klíči pro Template.
    Přidá i URL-encoded verze map_query.
    """
    out = {}

    site = data.get("site", {})
    out["site_title"] = site.get("title", "")
    out["site_language"] = site.get("language", "cs")
    out["site_theme_color"] = site.get("theme_color", "#7C3AED")
    out["site_hero_quote"] = site.get("hero_quote", "")
    out["site_welcome_text"] = site.get("welcome_text", "")
    out["site_welcome_text2"] = site.get("welcome_text2", "")
    out["site_welcome_text3"] = site.get("welcome_text3", "")
    out["site_welcome_text4"] = site.get("welcome_text4", "")
    out["site_welcome_text5"] = site.get("welcome_text5", "")
    out["site_welcome_text6"] = site.get("welcome_text6", "")

    couple = data.get("couple", {})
    out["bride_name"] = couple.get("bride_name", "")
    out["groom_name"] = couple.get("groom_name", "")
    out["couple_hashtag"] = couple.get("hashtag", "")

    out["wedding_date_iso"] = data.get("wedding_date_iso", "")

    wedding = data.get("wedding", {})
    out["wedding_date_display"] = wedding.get("date_display", "")
    out["wedding_ceremony_time"] = wedding.get("ceremony_time", "")
    out["wedding_reception_time"] = wedding.get("reception_time", "")
    out["wedding_end_time"] = wedding.get("end_time", "")
    out["wedding_timezone"] = wedding.get("timezone", "")

    ubytovani = data.get("ubytovani",{})
    out["ubytovani_info"] = ubytovani.get("info", "")
    out["ubytovani_hrazeno"] = ubytovani.get("hrazeno", "")
    out["ubytovani_cena"] = ubytovani.get("cena", "")
    out["ubytovani_den_predem"] = ubytovani.get("den_predem", "")

    loc = data.get("locations", {})
    cer = loc.get("ceremony", {})
    
    out["ceremony_name"] = cer.get("name", "")
    out["ceremony_address"] = cer.get("address", "")
    out["ceremony_map_query"] = quote(cer.get("map_query", ""))
    out["ceremony_parking_info"] = cer.get ("parking_info","")
    out["ceremony_doprava_info"] = cer.get ("doprava_info","")
    out["ceremony_thanks"] = cer.get ("thanks","")
    out["ceremony_doprava_odjezd"] = cer.get ("doprava_odjezd","")
    
    rsvp = data.get("rsvp", {})
    out["rsvp_deadline_display"] = rsvp.get("deadline_display", "")
    out["rsvp_email"] = rsvp.get("email", "")

    return out


def build():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Chybí {DATA_FILE}")

    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(f"Chybí {TEMPLATE_FILE}")

    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    values = flatten(data)

    tpl = Template(TEMPLATE_FILE.read_text(encoding="utf-8"))
    html = tpl.safe_substitute(values)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(html, encoding="utf-8")

    print(f"✅ Hotovo: {OUT_FILE}")


if __name__ == "__main__":
    build()