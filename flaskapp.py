import requests
from multiprocessing.pool import ThreadPool

def start_stop_chr(start,stop,chr):
    res = requests.post("http://HIDDEN_PATH/annotations/_search?pretty=true&size=50", json=
    {
        "query": {
            "bool": {
                "must": [
                    {"match": {"CHROM": chr} }
                ],
                "filter":
                    {"range": {"START": {"gte": start, "lte": stop} } }

            }
        }
    })
    data = res.json()["hits"]["hits"]
    start = []
    stop = []
    chr = []
    gene_name = []
    for i in data:
        start.append(i["_source"]["START"])
        stop.append(i["_source"]["STOP"])
        chr.append(i["_source"]["CHROM"])
        gene_name.append(i["_source"]["GENE_NAME"])
        if len(start) >0:
            return binding_site(min(start),max(stop),chr[0],data)
        else:
            return binding_site(start,stop,chr,data)

def binding_site(start,stop,chr,annotations):
    res = requests.post("http://HIDDEN_PATH/binding_site/_search?pretty=true", json={
      "query": {
        "bool" : {
          "must" : [{
            "range" : { "START" : {"gte" : start, "lte" : stop} },
            "range" : { "STOP" : {"lte" : stop, "gte" : start} }
        }],
        "filter" : {
            "term" : {"CHR" : chr}
        }
    }
    }
    })
    data = res.json()["hits"]["hits"]
    binding_site = []
    start = []
    stop = []
    chr = []
    for i in data:
        start.append(i["_source"]["START"])
        stop.append(i["_source"]["STOP"])
        chr.append(i["_source"]["CHR"])
        binding_site.append(i["_source"])
    return exon_sgrna_peek(start, stop, chr, annotations,binding_site)


def sg_rna(coordinate,chr):
    sg_rna = []
    for i in range(0,len(coordinate)):
        res = requests.post("http://HIDDEN_PATH/sg_rna/_search?pretty=true&scroll=10m&size=1", json={
        "query": {
            "term": {"BS_CHR": chr[i]}
        },
        "sort" : {
            "_script" : {
                "type" : "number",
                "script" : {
                    "lang": "painless",
                    "params": {
                  "factor": int(coordinate[i])
                },
                    "inline": "def cur = 0; cur = (params.factor - doc['BS_START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}" },
                "order" : "asc"
            }
        }
        })
        data = res.json()
        sg_rna.append(data["hits"]["hits"][0]["_source"])
    return sg_rna

def peek(coordinate,chr):
    peek_liver = []
    for i in range(0,len(coordinate)):
        res = requests.post("http://HIDDEN_PATH/peek_liver/_search?pretty=true&scroll=10m&size=1", json={
        "query": {
            "term": {"CHR": chr[i]}
        },
        "sort" : {
            "_script" : {
                "type" : "number",
                "script" : {
                    "lang": "painless",
                    "inline": "def factor = "+ str(coordinate[i]) +  "; def cur = 0; cur = (factor - doc['START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                "order" : "asc"
            }
        }
        })
        data = res.json()
        peek_liver.append(data["hits"]["hits"][0]["_source"])
    return peek_liver

def exon_exp(coordinate,chr):
    exon_exp = []
    for i in range(0,len(coordinate)):
        res = requests.post("http://HIDDEN_PATH/exonexpression/_search?pretty=true&scroll=10m&size=1", json={
        "query": {
            "term": {"CHR": chr[i]}
        },
        "sort" : {
            "_script" : {
                "type" : "number",
                "script" : {
                    "lang": "painless",
                    "inline": "def factor = "+ str(coordinate[i]) +  "; def cur = 0; cur = (factor - doc['START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                "order" : "asc"
            }
        }
        })
        data = res.json()
        exon_exp.append(data["hits"]["hits"][0]["_source"])
    return exon_exp

def exon_sgrna_peek(bs_start,bs_stop,bs_chr,annotations,binding_site):
    sgrna_start = sg_rna(bs_start,bs_chr)
    sgrna_stop = sg_rna(bs_stop,bs_chr)
    peek_start = peek(bs_start,bs_chr)
    peek_stop = peek(bs_stop,bs_chr)
    exon_start = exon_exp(bs_start,bs_chr)
    exon_stop = exon_exp(bs_stop,bs_chr)
    sgrna_final = []
    exon_final = []
    peek_final = []
    for i in range(len(bs_start)):
        if int(sgrna_start[i]["BS_START"]) - int(bs_start[i]) <= int(sgrna_stop[i]["BS_END"]) - int(bs_start[i]):
            sgrna_final.append(sgrna_start[i])
        else:
            sgrna_final.append(sgrna_stop[i])
        if int(exon_start[i]["START"]) - int(bs_start[i]) <= int(exon_stop[i]["STOP"]) - int(bs_start[i]):
            exon_final.append(exon_start[i])
        else:
            exon_final.append(exon_stop[i])
        if int(peek_start[i]["START"]) - int(bs_start[i]) <= int(peek_stop[i]["STOP"]) - int(bs_start[i]):
            peek_final.append(peek_start[i])
        else:
            peek_final.append(peek_stop[i])
    return annotations, binding_site, sgrna_final, peek_final,exon_final

#________________________________________________________END OF FUNCTIONS FOR COORDINATE BASE SEARCH____________________________________________________________________________________

def rna_bp(rbp, efficiency,specificity):
    res = requests.post("http://HIDDEN_PATH/binding_site/_search?pretty=true&size=500", json=
    {
        "query": {
            "match": {
                "GENE": rbp.lower()
            }
        }
    })
    data = res.json()["hits"]["hits"]
    binding_site = []
    start = []
    stop = []
    chr = []
    for i in data:
        start.append(i["_source"]["START"])
        stop.append(i["_source"]["STOP"])
        chr.append(i["_source"]["CHR"])
        binding_site.append(i["_source"])
    return gene_exon_sgrna_peek(start,stop,efficiency,specificity,data,chr)

def gene_sg_rna(coordinate,efficiency,specificity,chr):
    sg_rna = []
    for i in range(len(coordinate)):
        a = int(coordinate[i])
        res = requests.post("http://HIDDEN_PATH/_search?pretty=true&scroll=10m&size=1", json={
        "query": {
            "bool": {
                "must":
        			{"match": {"BS_CHR" : chr[i]} },
                "filter":
                    [ {"range": {"Specificity": {"gte": specificity} } },
                      {"range": {"Efficiency": {"gte": efficiency} } } ]
            }
        },
        "sort" : {
            "_script" : {
                "type" : "number",
                "script" : {
                    "lang": "painless",
                    "params": {
                  "factor": a
                },
                    "inline": "def cur = 0; cur = (params.factor - doc['BS_START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}" },
                "order" : "asc"
            }
        }

    })
        data = res.json()
        sg_rna.append(data["hits"]["hits"][0]["_source"])
    return sg_rna

def gene_peek(coordinate, chr):
    peek_liver = []
    for i in range(0,len(coordinate)):
        a = int(coordinate[i])
        res = requests.post("http://HIDDEN_PATH/peek_liver/_search?pretty=true&scroll=10m&size=1", json={
        "query": {
            "term": {"CHR": chr[i]}
        },
        "sort" : {
            "_script" : {
                "type" : "number",
                "script" : {
                    "lang": "painless",
                    "params": {
                  "factor": a
                },
                    "inline": "def cur = 0; cur = (params.factor - doc['START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}" },
                "order" : "asc"
            }
        }

    })
        data = res.json()
        peek_liver.append(data["hits"]["hits"][0]["_source"])
    return peek_liver


def gene_exon_exp(coordinate, chr):
    exon_exp = []
    for i in range(0,len(coordinate)):
        a = int(coordinate[i])
        res = requests.post("http://HIDDEN_PATH/exonexpression/_search?pretty=true&scroll=10m&size=1", json={
        "query": {
            "term": {"CHR": chr[i]}
        },
        "sort" : {
            "_script" : {
                "type" : "number",
                "script" : {
                    "lang": "painless",
                    "params": {
                  "factor": a
                },
                    "inline": "def cur = 0; cur = (params.factor - doc['START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}" },
                "order" : "asc"
            }
        }

    })
        data = res.json()
        exon_exp.append(data["hits"]["hits"][0]["_source"])
    return exon_exp

def gene_exon_sgrna_peek(bs_start,bs_stop,efficiency,specificity,binding_site,chr):
    pool_query = ThreadPool(processes=6)
    sgrna_start = pool_query.apply_async(gene_sg_rna, (bs_start, efficiency,specificity, chr))
    sgrna_stop = pool_query.apply_async(gene_sg_rna, (bs_stop, efficiency,specificity, chr))
    peek_start = pool_query.apply_async(gene_peek, args=(bs_start, chr))
    peek_stop = pool_query.apply_async(gene_peek, args=(bs_stop, chr))
    exon_start = pool_query.apply_async(gene_exon_exp, args=(bs_start, chr))
    exon_stop = pool_query.apply_async(gene_exon_exp, args=(bs_stop, chr))
    sgrna_start = sgrna_start.get()
    sgrna_stop = sgrna_stop.get()
    peek_start = peek_start.get()
    peek_stop = peek_stop.get()
    exon_start = exon_start.get()
    exon_stop = exon_stop.get()
    sgrna_final = []
    exon_final = []
    peek_final = []
    for i in range(len(bs_start)):
        if int(sgrna_start[i]["BS_START"]) - int(bs_start[i]) <= int(sgrna_stop[i]["BS_END"]) - int(bs_start[i]):
            sgrna_final.append(sgrna_start[i])
        else:
            sgrna_final.append(sgrna_stop[i])
        if int(exon_start[i]["START"]) - int(bs_start[i]) <= int(exon_stop[i]["STOP"]) - int(bs_start[i]):
            exon_final.append(exon_start[i])
        else:
            exon_final.append(exon_stop[i])
        if int(peek_start[i]["START"]) - int(bs_start[i]) <= int(peek_stop[i]["STOP"]) - int(bs_start[i]):
            peek_final.append(peek_start[i])
        else:
            peek_final.append(peek_stop[i])
    return binding_site, sgrna_final, peek_final,exon_final


from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def process_data():
    if request.method == "POST":
        if request.form.get("check") == "ZERO":
            coordinates = request.form["search_field"]
            chrom = request.form.get("chrom")
            if "|" in coordinates:
                coordinates = coordinates.split("|")
                annotations, bs, sgrna, peek, exons = start_stop_chr(coordinates[0], coordinates[1], str.lower(chrom))
                return render_template("result.html", annotations=annotations, bs=bs, sgrna=sgrna, peek=peek, exons=exons, length=len(bs), chrom=chrom)
        elif request.form.get("check") == "ONE":
            rbp = str(request.form.get("rbp")).lower()
            specificity =50
            efficiency =0
            if len(request.form["specificity"]) >0:
                specificity = request.form["specificity"]
            if len(request.form["efficiency"]) >0:
                efficiency =  len(request.form["efficiency"])

            bs, sgrna, peek, exons = rna_bp(rbp,efficiency,specificity)
            length = len(bs)

            return render_template("rbp_result.html",bs=bs, sgrna=sgrna, peek=peek, exons=exons, length=length)

    RNA_BINDING_PROTEINS = {'AKAP8L': 'ENSG00000011243', 'BCCIP': 'ENSG00000107949', 'CPSF6': 'ENSG00000111605', 'CSTF2T': 'ENSG00000177613', 'DDX3X': 'ENSG00000215301', 'DDX42': 'ENSG00000198231', 'DDX55': 'ENSG00000111364', 'DDX6': 'ENSG00000110367', 'DKC1': 'ENSG00000130826', 'DROSHA': 'ENSG00000113360', 'EFTUD2': 'ENSG00000108883', 'EIF3D': 'ENSG00000100353', 'EIF4G1': 'ENSG00000114867', 'EIF4G2': 'ENSG00000110321', 'EWSR1': 'ENSG00000182944', 'FAM120A': 'ENSG00000048828', 'FASTKD2': 'ENSG00000118246', 'FKBP4': 'ENSG00000004478', 'FMR1': 'ENSG00000102081', 'FUS': 'ENSG00000089280', 'FXR1': 'ENSG00000114416', 'FXR2': 'ENSG00000129245', 'GRSF1': 'ENSG00000132463', 'GTF2F1': 'ENSG00000125651', 'HLTF': 'ENSG00000071794', 'HNRNPA1': 'ENSG00000135486', 'HNRNPC': 'ENSG00000092199', 'HNRNPK': 'ENSG00000165119', 'HNRNPM': 'ENSG00000099783', 'HNRNPU': 'ENSG00000153187', 'HNRNPUL1': 'ENSG00000105323', 'IGF2BP1': 'ENSG00000159217', 'IGF2BP2': 'ENSG00000073792', 'IGF2BP3': 'ENSG00000136231', 'ILF3': 'ENSG00000129351', 'KHDRBS1': 'ENSG00000121774', 'KHSRP': 'ENSG00000088247', 'LARP4': 'ENSG00000161813', 'LARP7': 'ENSG00000174720', 'LIN28B': 'ENSG00000187772', 'LSM11': 'ENSG00000155858', 'METAP2': 'ENSG00000111142', 'MTPAP': 'ENSG00000107951', 'NCBP2': 'ENSG00000114503', 'NKRF': 'ENSG00000186416', 'NOL12': 'ENSG00000256872', 'NONO': 'ENSG00000147140', 'NPM1': 'ENSG00000181163', 'PCBP2': 'ENSG00000197111', 'PPIL4': 'ENSG00000131013', 'PRPF8': 'ENSG00000174231', 'PTBP1': 'ENSG00000011304', 'PUM2': 'ENSG00000055917', 'QKI': 'ENSG00000112531', 'RBFOX2': 'ENSG00000100320', 'RBM15': 'ENSG00000162775', 'RBM22': 'ENSG00000086589', 'RBM27': 'ENSG00000091009', 'RPS11': 'ENSG00000142534', 'RPS5': 'ENSG00000083845', 'SAFB2': 'ENSG00000130254', 'SBDS': 'ENSG00000126524', 'SF3A3': 'ENSG00000183431', 'SF3B4': 'ENSG00000143368', 'SFPQ': 'ENSG00000116560', 'SLBP': 'ENSG00000163950', 'SLTM': 'ENSG00000137776', 'SMNDC1': 'ENSG00000119953', 'SND1': 'ENSG00000197157', 'SRSF1': 'ENSG00000136450', 'SRSF7': 'ENSG00000115875', 'SRSF9': 'ENSG00000111786', 'TAF15': 'ENSG00000172660', 'TARDBP': 'ENSG00000120948', 'TBRG4': 'ENSG00000136270', 'TIA1': 'ENSG00000116001', 'TIAL1': 'ENSG00000151923', 'TNRC6A': 'ENSG00000090905', 'TRA2A': 'ENSG00000164548', 'TROVE2': 'ENSG00000116747', 'U2AF1': 'ENSG00000160201', 'U2AF2': 'ENSG00000063244', 'UPF1': 'ENSG00000005007', 'XRCC6': 'ENSG00000196419', 'XRN2': 'ENSG00000088930', 'YWHAG': 'ENSG00000170027', 'ZNF622': 'ENSG00000173545', 'ZRANB2': 'ENSG00000132485', 'AARS': 'ENSG00000090861', 'AGGF1': 'ENSG00000164252', 'AUH': 'ENSG00000148090', 'DGCR8': 'ENSG00000128191'}


    return render_template("index.html", RNA_BINDING_PROTEINS=RNA_BINDING_PROTEINS)

if __name__ == '__main__':
    app.run(debug=True)