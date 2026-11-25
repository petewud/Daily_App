from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

SOURCE = Path("artwork/source")
OUTPUT = Path("artwork/output")
CELL = 512
TARGET = 448
ALPHA_THRESHOLD = 8


def bounding_box(alpha: np.ndarray) -> tuple[int, int, int, int] | None:
    rows = np.any(alpha > ALPHA_THRESHOLD, axis=1)
    cols = np.any(alpha > ALPHA_THRESHOLD, axis=0)
    if not rows.any() or not cols.any():
        return None
    top, bottom = np.where(rows)[0][[0, -1]]
    left, right = np.where(cols)[0][[0, -1]]
    return int(left), int(top), int(right + 1), int(bottom + 1)


def square_crop(image: Image.Image, box: tuple[int, int, int, int]) -> tuple[Image.Image, dict]:
    left, top, right, bottom = box
    width = right - left
    height = bottom - top
    side = max(width, height)
    centre_x = (left + right) / 2
    centre_y = (top + bottom) / 2

    crop_left = int(round(centre_x - side / 2))
    crop_top = int(round(centre_y - side / 2))
    crop_right = crop_left + side
    crop_bottom = crop_top + side

    cell_width, cell_height = image.size
    clipped = crop_left < 0 or crop_top < 0 or crop_right > cell_width or crop_bottom > cell_height
    crop_left = max(0, crop_left)
    crop_top = max(0, crop_top)
    crop_right = min(cell_width, crop_right)
    crop_bottom = min(cell_height, crop_bottom)

    return image.crop((crop_left, crop_top, crop_right, crop_bottom)), {
        "requested_side": side,
        "clipped": clipped,
        "source_width": width,
        "source_height": height,
    }


def process_characters() -> list[dict]:
    entries: list[dict] = []
    sheets = sorted(SOURCE.glob("character-atlas-*.png"))

    if len(sheets) != 11:
        raise RuntimeError(f"Expected 11 character sheets, found {len(sheets)}")

    for sheet in sheets:
        source = Image.open(sheet).convert("RGBA")
        if source.size != (1024, 1024):
            raise RuntimeError(f"{sheet.name} is {source.size}, expected 1024x1024")

        corrected = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))

        for index in range(4):
            row, column = divmod(index, 2)
            cell = source.crop((column * CELL, row * CELL, (column + 1) * CELL, (row + 1) * CELL))
            alpha = np.array(cell)[:, :, 3]
            box = bounding_box(alpha)

            if box is None:
                entries.append(
                    {
                        "sheet": sheet.name,
                        "cell": index,
                        "grid_row": row,
                        "grid_column": column,
                        "status": "empty",
                    }
                )
                continue

            artwork, crop_info = square_crop(cell, box)
            resized = artwork.resize((TARGET, TARGET), Image.Resampling.LANCZOS)
            paste_x = column * CELL + (CELL - TARGET) // 2
            paste_y = row * CELL + (CELL - TARGET) // 2
            corrected.paste(resized, (paste_x, paste_y), resized)

            entries.append(
                {
                    "sheet": sheet.name,
                    "cell": index,
                    "grid_row": row,
                    "grid_column": column,
                    "status": "processed",
                    "source_bounding_box": {
                        "x": box[0],
                        "y": box[1],
                        "width": box[2] - box[0],
                        "height": box[3] - box[1],
                    },
                    "source_circle_size": max(box[2] - box[0], box[3] - box[1]),
                    "corrected_circle_size": TARGET,
                    "corrected_position": {"x": paste_x, "y": paste_y},
                    **crop_info,
                }
            )

        corrected.save(OUTPUT / sheet.name, optimize=True)

    return entries


def validate_props() -> dict:
    manifest_path = SOURCE / "props_atlas_manifest.json"
    atlas_path = SOURCE / "props_atlas.png"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    atlas = Image.open(atlas_path).convert("RGBA")

    if atlas.size != (manifest["meta"]["size"]["w"], manifest["meta"]["size"]["h"]):
        raise RuntimeError("Prop atlas dimensions do not match its manifest")

    results = []
    for sprite in manifest["sprites"]:
        x, y, width, height = sprite["x"], sprite["y"], sprite["width"], sprite["height"]
        region = atlas.crop((x, y, x + width, y + height))
        alpha = np.array(region)[:, :, 3]
        detected = bounding_box(alpha)

        if detected is None:
            results.append({"name": sprite["name"], "status": "no_visible_artwork"})
            continue

        detected_x, detected_y, detected_right, detected_bottom = detected
        tolerance = 3
        matches = (
            abs(detected_x) <= tolerance
            and abs(detected_y) <= tolerance
            and abs((x + width) - detected_right) <= tolerance
            and abs((y + height) - detected_bottom) <= tolerance
        )
        results.append(
            {
                "name": sprite["name"],
                "status": "match" if matches else "mismatch",
                "manifest_rectangle": {"x": x, "y": y, "width": width, "height": height},
                "detected_rectangle": {
                    "x": x + detected_x,
                    "y": y + detected_y,
                    "width": detected_right - detected_x,
                    "height": detected_bottom - detected_y,
                },
            }
        )

    return {"atlas": atlas_path.name, "sprite_count": len(results), "results": results}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    characters = process_characters()
    props = validate_props()

    character_manifest = {
        "meta": {
            "source_folder": "artwork/source",
            "output_folder": "artwork/output",
            "sheet_size": {"width": 1024, "height": 1024},
            "cell_size": {"width": CELL, "height": CELL},
            "target_circle_size": TARGET,
            "character_count": sum(1 for item in characters if item["status"] == "processed"),
        },
        "characters": characters,
    }

    (OUTPUT / "character_manifest.json").write_text(
        json.dumps(character_manifest, indent=2), encoding="utf-8"
    )
    (OUTPUT / "props_validation.json").write_text(json.dumps(props, indent=2), encoding="utf-8")

    mismatches = [item for item in props["results"] if item["status"] != "match"]
    clipped = [item for item in characters if item.get("clipped")]

    report = [
        "# Artwork processing report",
        "",
        f"- Character sheets processed: {len(characters) // 4}",
        f"- Character portraits processed: {sum(1 for item in characters if item['status'] == 'processed')}",
        f"- Empty character cells: {sum(1 for item in characters if item['status'] == 'empty')}",
        f"- Character crops clipped by cell edge: {len(clipped)}",
        f"- Prop sprites checked: {props['sprite_count']}",
        f"- Prop manifest mismatches: {len(mismatches)}",
        "",
    ]

    if clipped:
        report.append("## Character crops needing review")
        report.extend(f"- {item['sheet']} cell {item['cell']}" for item in clipped)
        report.append("")

    if mismatches:
        report.append("## Prop manifest mismatches")
        report.extend(f"- {item['name']}: {item['status']}" for item in mismatches)
        report.append("")

    (OUTPUT / "report.md").write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
