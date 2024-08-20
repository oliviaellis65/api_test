import json
import requests

# file location and api_key variables redacted


#### GENE -> CONCEPT 
gene_categories = ["CSLYT000001", "GENE", "T116", "CHEM", "CSLYT000001"]
oncology_drug_categories =  ["C3653621",
               # "CHEM",
                "T061",
                "T123"]
entry_terms = ["TIGIT", "IRF5"]


concept_ids = {}
# i would like to filter my search for concepts to be in the following categories: GENE, CHEM, CSLY...
for entry_term in entry_terms:
    # 1. map genes to concepts
    url = "https://api.causaly.com/rest/v0/concepts/search?q=" + entry_term
    payload = {}
    headers = {"x-api-key": api_key}
    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()
    # save outputs into a dictionary called 'ids' of concept id:name pairs
    ids = {}
    for term in r["data"]:
        ids[term["id"]] = term["name"]
    concept_ids[entry_term] = ids
    # 2. map concepts to drugs
    url = "https://api.causaly.com/rest/v0/relationships/search"
    request_body = {
        "cursor": "",
        "data_sources": [],
        "document_sections": [],
        "document_scope": "(oncology)",
        "publication_types": [],
        "publication_year": {},
        "journals": [],
        "journal_rank_quartiles": [],
        "relationship": {
            "cause": {"ids": [], 
                      #"category_ids": oncology_drug_categories, 
                      "category_taxonomies": "ATC"},
            "effect": {"ids": list(ids.keys()), "category_ids": gene_categories},
            "relationship_types": [
                "UPREGULATE",
                "DOWNREGULATE",
                "UNIDIRECTIONAL"
            ],
        },
    }
    payload = json.dumps(request_body)
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)
    r = response.json()
    with open(
        f"{file_location}/{entry_term}_oncology_drugs.json", mode="w", encoding="utf-8"
    ) as f:
        json.dump(r, f, ensure_ascii=False, indent=4)
    print("status_code: ", response.status_code, "; page: ", 1, " downloaded.")


#### CONCEPT -> drug
#print(concept_ids)
#categories.id



# cause = drugs, effects = gene

###_request_execution_###
