import json
import os
import shutil

from rdflib import RDF, Graph, Literal, Namespace, URIRef
from tqdm import tqdm

to_ingest = "to_ingest"
out_file = os.path.join(to_ingest, "arche.ttl")
shutil.rmtree(to_ingest, ignore_errors=True)
os.makedirs(to_ingest, exist_ok=True)
g = Graph().parse("arche/arche_top_col.ttl")
arche_constants = Graph().parse("arche/arche_constants.ttl")
TOP_COL = os.environ.get("TOPCOLID", "https://id.acdh.oeaw.ac.at/kalbeck-tagebuch")
TOP_COL_URI = URIRef(TOP_COL)
ACDH = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")


with open("kalbeck_1/fileList.json", "r", encoding="utf-8") as fp:
    data = json.load(fp)

with open("kalbeck_2/fileList.json", "r", encoding="utf-8") as fp:
    data_two = json.load(fp)

data = sorted(data + data_two, key=lambda x: x["filename"])


for i, x in enumerate(tqdm(data)):
    f_name = x["filename"]
    subj = URIRef(f"{TOP_COL}/{f_name}")
    g.add((subj, RDF.type, ACDH["Resource"]))
    g.add(
        (
            subj,
            ACDH["hasCategory"],
            URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/image"),
        )
    )

    for p, o in arche_constants.predicate_objects():
        g.add((subj, p, o))
    if f_name.startswith("kalbeck_1"):
        parent_col = URIRef(f"{TOP_COL}/facs/1895")
    else:
        parent_col = URIRef(f"{TOP_COL}/facs/1897")
    g.add((subj, ACDH["isPartOf"], parent_col))
    g.add((subj, ACDH["hasTitle"], Literal(f_name, lang="und")))
    g.add(
        (subj, ACDH["hasDigitisingAgent"], URIRef("https://id.acdh.oeaw.ac.at/memir"))
    )
    try:
        next_item = data[i + 1]
    except IndexError:
        next_item = False
        continue
    next_item = next_item["filename"]
    if "kalbeck_1" in f_name and "kalbeck_1" in next_item:
        g.add((subj, ACDH["hasNextItem"], URIRef(URIRef(f"{TOP_COL}/{next_item}"))))
    if "kalbeck_2" in f_name and "kalbeck_2" in next_item:
        g.add((subj, ACDH["hasNextItem"], URIRef(URIRef(f"{TOP_COL}/{next_item}"))))


g.serialize(out_file)
