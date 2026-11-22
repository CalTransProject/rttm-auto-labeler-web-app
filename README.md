# LiDAR Frame Data Quality Auditor

This tool checks raw LiDAR `.bin` point-cloud frames before subsequent labeling or vehicle-analysis tasks. It is a standalone quality-audit utility and does **not** perform object detection, vehicle speed estimation, annotation validation, or distance estimation.

## Input and assumptions

- Input: a directory containing `.bin` files (searched recursively), or a ZIP archive containing `.bin` files.
- Expected record layout: **four little-endian float32 values per point**, interpreted as `(x, y, z, fourth_field)`.
- The fourth field is not assumed to represent intensity; its meaning depends on the dataset.
- Typical frame filenames are six digits followed by `.bin`, e.g. `000203.bin`.

Verify the binary record layout before using this script on a different dataset.

## Setup

Requires Python 3.9+ and NumPy.

```bash
python -m pip install -r requirements.txt
```

## Run

From this folder, scan a ZIP archive:

```bash
python lidar_frame_auditor.py "path/to/frames.zip" --output audit_output
```

Or scan a directory:

```bash
python lidar_frame_auditor.py "path/to/frames_folder" --output audit_output
```

## Generated files

- `audit_output/audit_summary.json`: aggregate results and per-frame records
- `audit_output/audit_summary.csv`: tabular results, one row per frame
- `audit_output/numbered_txt_reports/`: a plain-text report per frame

For each frame the script reports its point count, file size, non-finite points, zero-XYZ points, and minimum/maximum values for X, Y, Z and the fourth field. It also flags empty files, unexpected frame filenames, and sizes incompatible with four float32 values per point.

Missing frame IDs inside the observed range are informational; a selected dataset need not be sequential. The utility cannot verify object labels or true vehicle positions from `.bin` alone.

## Tests

```bash
python -m unittest discover -v
```

The included tests use **generated synthetic point clouds**, not actual project frames.

## Repository organization

Store this folder under `lidar_analysis/` within the team's repository. Run the tool locally on a frame folder or ZIP. **Do not commit raw LiDAR datasets or generated audit reports unless your team specifically requests them.**

## Project context

Supporting quality checks for the senior-design LiDAR auto-labeling workflow. Future work can incorporate the reviewed labels and a reference-object workflow to support vehicle-distance analysis; those capabilities are not part of this script.
