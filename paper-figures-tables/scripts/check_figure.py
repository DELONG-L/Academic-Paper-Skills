"""Read-only figure diagnostics; no implicit venue or house-style gate.

--strict controls process exit status for definite file/explicit resolution
failures. It does not establish manuscript readiness or semantic correctness.
"""
from __future__ import annotations
import argparse
import glob
import math
import os
from typing import Any

SEVERITY = {"INFO": 0, "WARN": 1, "FAIL": 2}
VECTOR_FORMATS = {"pdf", "svg", "eps"}
RASTER_OK_FORMATS = {"png", "tiff", "tif"}
JPEG_FORMATS = {"jpg", "jpeg"}

def _obj(value):
    return value.get_object() if hasattr(value, "get_object") else value

def _check_pdf_fonts(path):
    issues=[]
    try:
        from pypdf import PdfReader
    except ImportError:
        issues.append(("INFO", "pypdf unavailable: PDF/font inspection not performed."))
        return issues
    try:
        reader=PdfReader(path)
        seen=set()
        for page in reader.pages:
            resources=_obj(page.get("/Resources")) or {}
            fonts=_obj(resources.get("/Font")) or {}
            for font_ref in fonts.values():
                font=_obj(font_ref)
                candidates=[_obj(x) for x in (_obj(font.get("/DescendantFonts")) or [font])]
                for leaf in candidates:
                    subtype=str(leaf.get("/Subtype", ""))
                    base=str(leaf.get("/BaseFont", "unknown"))
                    key=(base,subtype)
                    if key in seen:
                        continue
                    seen.add(key)
                    if subtype == "/Type3":
                        issues.append(("WARN", f"Type 3 font {base}: inspect rendering and actual venue font requirements; type alone is not a failure."))
                        continue
                    descriptor=_obj(leaf.get("/FontDescriptor")) or {}
                    if not any(k in descriptor for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                        issues.append(("WARN", f"Font {base} has no detected embedded program; inspect portability and venue requirements."))
    except Exception as exc:
        issues.append(("WARN", f"PDF/font inspection incomplete: {exc}"))
    return issues

def _check_raster(path, ext, min_dpi, target_inches):
    issues=[]
    info={"category":"raster", "ext":ext}
    if ext in JPEG_FORMATS:
        issues.append(("WARN", "JPEG is lossy: inspect text/line artifacts and actual format requirements; photographs may be suitable."))
    try:
        from PIL import Image
    except ImportError:
        return issues+[("INFO", "Pillow unavailable: raster decoding/resolution not checked.")],info
    try:
        with Image.open(path) as img:
            img.load()
            info["size_px"]=img.size
            info["dpi"]=img.info.get("dpi")
    except Exception as exc:
        return issues+[("FAIL", f"Cannot decode image: {exc}")],info
    if target_inches is not None:
        dpi=tuple(px/inches for px,inches in zip(info["size_px"],target_inches))
        info["resolution_basis"]="pixels_at_declared_final_size"
        info["final_inches"]=target_inches
    else:
        dpi=info["dpi"]
        if dpi is not None and not isinstance(dpi,(list,tuple)):
            dpi=(dpi,dpi)
        info["resolution_basis"]="embedded_dpi_only"
        issues.append(("INFO", "Final placement size not supplied; embedded DPI does not establish final resolution."))
    if dpi is None or len(dpi)!=2 or not all(math.isfinite(float(v)) and float(v)>0 for v in dpi):
        issues.append(("WARN", "No usable DPI metadata or final placement; resolution cannot be checked."))
    else:
        info["checked_dpi"]=[float(v) for v in dpi]
        if min_dpi is not None and min(float(v) for v in dpi)+0.01 < min_dpi:
            issues.append(("FAIL", f"Resolution {dpi} is below explicitly requested {min_dpi} DPI on at least one axis."))
    return issues,info

def _check_svg(path):
    import xml.etree.ElementTree as ET
    try:
        root=ET.parse(path).getroot()
    except (OSError,ET.ParseError) as exc:
        return [("FAIL",f"Cannot parse SVG: {exc}")]
    if root.tag.rsplit("}",1)[-1] != "svg":
        return [("FAIL","File root is not SVG.")]
    if any(node.tag.rsplit("}",1)[-1] == "image" for node in root.iter()):
        return [("INFO","SVG contains raster/image content; inspect its effective resolution and fidelity. Mixed output is valid.")]
    return []

def check_figure(path: str, min_dpi: int | None = None,
                 target_inches: tuple[float,float] | None = None
                 ) -> tuple[list[tuple[str,str]],dict[str,Any]]:
    if min_dpi is not None and (not math.isfinite(min_dpi) or min_dpi<=0):
        raise ValueError("min_dpi must be positive and finite")
    if target_inches is not None and (len(target_inches)!=2 or not all(math.isfinite(v) and v>0 for v in target_inches)):
        raise ValueError("target_inches must contain two positive finite final dimensions")
    info={"path":str(path)}
    if not os.path.isfile(path):
        return [("FAIL","File does not exist or is not a regular file.")],info
    info["size_bytes"]=os.path.getsize(path)
    if info["size_bytes"]==0:
        return [("FAIL","File is empty.")],info
    ext=os.path.splitext(path)[1].lower().lstrip(".")
    info["ext"]=ext
    if ext in RASTER_OK_FORMATS | JPEG_FORMATS:
        issues,extra=_check_raster(path,ext,min_dpi,target_inches)
        info.update(extra)
    elif ext=="pdf":
        info["category"]="vector_container"
        issues=_check_pdf_fonts(path)
    elif ext=="svg":
        info["category"]="vector_container"
        issues=_check_svg(path)
    else:
        issues=[("INFO",f"Content inspection for .{ext} is not implemented; inspect with an appropriate renderer.")]
    info["coverage"]="File diagnostics only; no semantic, final-width readability, complete font-tree, or venue-readiness assessment."
    return issues,info

def print_report(path,issues,info):
    print(str(path))
    for key in ("category","size_px","dpi","checked_dpi","resolution_basis"):
        if key in info:
            print(f"  {key}: {info[key]}")
    for severity,message in sorted(issues,key=lambda item:-SEVERITY[item[0]]):
        print(f"  [{severity}] {message}")
    verdict=max((s for s,_ in issues),key=lambda s:SEVERITY[s],default="PASS")
    print(f"  Diagnostic result: {verdict}; not a manuscript readiness judgment.")
    return verdict

def _cli():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths",nargs="+")
    parser.add_argument("--min-dpi",type=int,help="Explicit required minimum; no default venue threshold")
    parser.add_argument("--width-in",type=float,help="Final placed width in inches")
    parser.add_argument("--height-in",type=float,help="Final placed height in inches")
    parser.add_argument("--strict",action="store_true",help="Exit 2 on definite file or explicit resolution failures")
    args=parser.parse_args()
    if (args.width_in is None)!=(args.height_in is None):
        parser.error("Supply both final width and height")
    target=None if args.width_in is None else (args.width_in,args.height_in)
    failed=False
    for pattern in args.paths:
        for path in glob.glob(pattern) or [pattern]:
            try:
                issues,info=check_figure(path,args.min_dpi,target)
            except ValueError as exc:
                parser.error(str(exc))
            failed |= print_report(path,issues,info)=="FAIL"
    return 2 if args.strict and failed else 0

if __name__=="__main__":
    raise SystemExit(_cli())
