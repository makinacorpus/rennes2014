#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import csv
import unicodedata
import json

candidates = {
    "gerard_de_mellon": 'Gerard DE MELLON',
    "nathalie_appere": 'Nathalie APPÉRÉ',
    "matthieu_theurier": 'Matthieu THEURIER',
    "valerie_hamon": 'Valérie HAMON',
    "caroline_ollivro": 'Caroline OLLIVRO',
    "pierre_priet": 'Pierre PRIET',
    "alexandre_noury": 'Alexandre NOURY',
}

if __name__ == '__main__':

    fname = "municipales_2014_rennes_tour1_1.csv"
    outfilename = "bureaux_decoupage.json"
    #outfilename = "bureauxG1.json"
    offices = {}
    with open(fname, 'r') as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:
            newrow = []
            if(row["NIVEAU_DETAIL"] == "bu"):
            #if(row["NIVEAU_DETAIL"] == "vi"):
                # Get results for each political list
                for i in range(1, 7):
                    nom_candidat = unicode(row["CANDIDAT_%s" % (i + 1)].decode("utf8"))
                    #normalize name
                    normalized_nom = unicodedata.normalize('NFKD', nom_candidat).encode('ascii', 'ignore').lower().replace(" ", "_")
                    newrow.append({normalized_nom: float(row["POURCENTAGE_%s" % i].replace(",", "."))})

                results = sorted(newrow, key=lambda k: k.values()[0], reverse=True)
                offices[row["NUMERO_LIEU"]] = results
                #offices = results
                #break

    with open(outfilename, 'w') as outfile:
        response_json = json.dump(offices, outfile)
