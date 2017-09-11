"""
    Takes a tsv file as input, with terms to be mapped in the first column
    Generates a file called mapped_terms.tsv that has in the first column the term
    that was mapped, and in the second column the ontology term mappings that Zooma found.

    You can specify:
        -confidence
            HIGH, GOOD, or MEDIUM
            will restrict the mappings with the desired confidence found in Zooma
            if the confidence isn't met, the term is left unmapped
            default confidence is HIGH
        -type
            you can specify a type for the terms that are searched
            and zooma will try and find a mapping under that category
            e.g. -type: 'organism part' for searching the term 'liver'
        -ontologies
            the ontologies that the search will be restriced to if it hits OLS
            enter as many as you want, but comma separated
            e.g. -ontologies efo,uberon,omim
            can be: -ontologies none - and no ontologies will be searched
            (it will hit OLS if no mapping is found in the datasources or
            if we specify filter=required:[none], i.e. ignore the datasources)
        -datasources
            the datasources we want to restrict the search to
            enter comma separated like ontologies above
            can also be none

"""

import requests
import argparse
import urllib
import csv


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-value', help='zooma propertyValue to search for')
    parser.add_argument("-f", help='file with list of terms to be mapped', required = True)
    parser.add_argument('-type', help='zooma propertyType to restrict the proprtyValue search to')
    parser.add_argument('-ontologies', help='ontologies to restrict search to, comma separated')
    parser.add_argument('-datasources', help='datasources to restrict search to, comma separated')
    parser.add_argument('-confidence', help='can be: HIGH, GOOD, MEDIUM, GOOD|MEDIUM')
    parser.add_argument('-tutorial', help='for the icbo tutorial, query all datasources except gwas')
    args = parser.parse_args()

    if args.tutorial is not None:
        datasources = "cbi, eva, sysmicro, atlas, uniprot, ebisc, clinvar-xrefs, cttv"
        args.datasources = datasources

    confidence = get_confidence(args.confidence)
    with open(args.f, 'r') as csvfile:
        with open('mapped_terms.tsv', 'w') as mapped:
            # reader =
            for line in csv.reader(csvfile.read().splitlines(), delimiter='\t'):
                value = line[0]
                semantic_tags = None
                if len(line) < 2:
                    try:
                        semantic_tags = get_semantic_tags_for_high_confidence(value, args.ontologies, args.datasources, confidence, args.type)
                        print "Queried zooma for value:", value
                    except ValueError:
                        print "Could not query zooma for value:", value
                    if semantic_tags is not None:
                        for st in semantic_tags:
                            stid = st.split("/")
                            mapped.write(value + "\t" + st + "\t" + confidence + "\t" + stid[len(stid) - 1]  + "\n")
                    else:
                        mapped.write(value + "\n")
                else:
                    mapped.write(str(line).replace("'","").replace("[","").replace("]","").replace(",","\t") + "\n")


def get_confidence(confidence):
    if confidence is None:
        return "HIGH"
    elif confidence == "GOOD" or confidence == "MEDIUM" or confidence == "HIGH":
        return confidence
    else:
        print "Wrong confidence input"
        exit(1)


def get_semantic_tags_for_high_confidence(value, ontologies, datasources, confidence, value_type):
    url_base = "http://www.ebi.ac.uk/spot/zooma/v2/api/services/annotate?"
    params = {'propertyValue' : value}

    datafilter = None
    restrict_to_datasources = []
    if datasources is not None:
        for dsource in datasources.split(","):
            restrict_to_datasources.append(dsource)
        datafilter = "required:{}".format(str(restrict_to_datasources).replace("'","").replace(" ",""))

    restrict_to_ontologies = []
    if ontologies is not None:
        for ontology in ontologies.split(","):
            restrict_to_ontologies.append(ontology)
        if datafilter is not None:
            datafilter = "{},{}".format(datafilter, "ontologies:{}".format(str(restrict_to_ontologies).replace("'","").replace(" ","")))

        else:
            datafilter = "ontologies:{}".format(str(restrict_to_ontologies).replace("'","").replace(" ",""))


    # if value_type is not None:
    #     params['propertyType'] = value_type

    # url = "{}propertyValue={}".format(url_base, value)
    url = "{}{}".format(url_base, urllib.urlencode(params))

    if datafilter is not None:
        url = "{}&filter={}".format(url, datafilter)

    response = requests.get(url)

    reply = response.json()

    for mapping in reply:
        st = None
        if mapping['confidence'] == confidence:
            if st is None:
                st = mapping['semanticTags']
            else:
                st.append(mapping['semanticTags'])
        return st


if __name__ == '__main__':
    main()
