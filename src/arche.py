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

slice_one = data[:3]
for i, x in enumerate(tqdm(slice_one)):
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
    # if i + 1 < len(slice_one):
    #     next_f_name = slice_one[i + 1]["filename"]
    #     g.add((subj, ACDH["hasNextItem"], URIRef(f"{TOP_COL}/{next_f_name}")))

## this second loop is just some ugly workaround to process slices; for the whole set it can be removed
slice_two = data[len(data) - 3 :]
for i, x in enumerate(tqdm(slice_two)):
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
    # if i + 1 < len(slice_two):
    #     next_f_name = slice_two[i + 1]["filename"]
    #     g.add((subj, ACDH["hasNextItem"], URIRef(f"{TOP_COL}/{next_f_name}")))


g.serialize(out_file)
