import requests
from multiprocessing.pool import ThreadPool
from elasticsearch_dsl import MultiSearch, Search
from elasticsearch import Elasticsearch
import pprint


def start_stop_chr(start, stop, chr):
    es = Elasticsearch()
    request = []
    for i in range(len(chr)):
        req_head = {'index': 'annotations', 'type': 'annotations'}
        req_body = {"from": 0, "size": 100, "query": {
            "bool": {
                "must": [
                    {"match": {"CHROM": chr}}
                ],
                "filter":
                    {"range": {"START": {"gte": start, "lte": stop}}}

            }
        }
                    }
        request.extend([req_head, req_body])
    resp = es.msearch(body=request)
    annotations = []
    start = []
    stop = []
    chr = []
    for i in resp["responses"][0]["hits"]["hits"]:
        annotations.append(i["_source"])
        start.append(i["_source"]["START"])
        stop.append(i["_source"]["STOP"])
        chr.append(i["_source"]["CHROM"])
    return binding_site(start, stop, chr, annotations)


def binding_site(start, stop, chr, annotations):
    es = Elasticsearch()
    request = []
    for i in range(len(chr)):
        req_head = {'index': 'bs', 'type': 'bs'}
        req_body = {"from": 0, "size": 1, "query": {
            "bool": {
                "must": [{
                    "range": {"START": {"gte": start[i], "lte": stop[i]}},
                    "range": {"STOP": {"lte": stop[i], "gte": start[i]}}
                }],
                "filter": {
                    "term": {"CHR": chr[i]}
                }
            }
        }
                    }
        request.extend([req_head, req_body])
    resp = es.msearch(body=request)
    bs = []
    bs_start = []
    bs_stop = []
    bs_chr = []
    for i in resp["responses"]:
        if i["hits"]["hits"] != []:
            bs.append(i["hits"]["hits"][0]["_source"])
            bs_start.append(i["hits"]["hits"][0]["_source"]["START"])
            bs_stop.append(i["hits"]["hits"][0]["_source"]["STOP"])
            bs_chr.append(i["hits"]["hits"][0]["_source"]["CHR"])
    return exon_sgrna_peek(bs_start, bs_stop, bs_chr, annotations, bs)


def sg_rna(coordinate, chr):
    sg_rna = []
    for i in range(0, len(coordinate)):
        upper_lim = int(coordinate[i]) + 100000
        lower_lim = int(coordinate[i]) - 100000
        res = requests.post("http://localhost:9200/sgrna/_search?pretty=true&size=1", verify=False json={
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "BS_START": {
                                    "gte": lower_lim, "lte": upper_lim
                                }
                            }
                        },
                        {
                            "term": {
                                "BS_CHR": chr[i]
                            }
                        }]
                }
            }
            ,
            "sort": {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "params": {
                            "factor": int(coordinate[i])
                        },
                        "inline": "def cur = 0; cur = (params.factor - doc['BS_START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                    "order": "asc"
                }
            }
        })
        data = res.json()
        sg_rna.append(data["hits"]["hits"][0]["_source"])
    return sg_rna


def peek(coordinate, chr):
    peek_liver = []
    for i in range(0, len(coordinate)):
        res = requests.post("http://localhost:9200/peek/_search?pretty=true&size=1", json={
            "query": {
                "term": {"CHR": chr[i]}
            },
            "sort": {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "inline": "def factor = " + str(coordinate[
                                                            i]) + "; def cur = 0; cur = (factor - doc['START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                    "order": "asc"
                }
            }
        })
        data = res.json()
        peek_liver.append(data["hits"]["hits"][0]["_source"])
    return peek_liver


def exon_exp(coordinate, chr):
    exon_exp = []
    for i in range(0, len(coordinate)):
        res = requests.post("http://localhost:9200/exon/_search?pretty=true&size=1", json={
            "query": {
                "term": {"CHR": chr[i]}
            },
            "sort": {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "inline": "def factor = " + str(coordinate[
                                                            i]) + "; def cur = 0; cur = (factor - doc['Start'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                    "order": "asc"
                }
            }
        })
        data = res.json()
        exon_exp.append(data["hits"]["hits"][0]["_source"])
    return exon_exp


def gwas(coordinate, chr):
    gwas = []
    for i in range(0, len(coordinate)):
        res = requests.post("http://localhost:9200/gwas/_search?pretty=true&size=1", json={
            "query": {
                "term": {"CHR_ID": chr[i]}
            },
            "sort": {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "inline": "def factor = " + str(coordinate[
                                                            i]) + "; def cur = 0; cur = (factor - doc['CHR_POS'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                    "order": "asc"
                }
            }
        })
        data = res.json()
        gwas.append(data["hits"]["hits"][0]["_source"])
    return gwas


def snp(coordinate, chr):
    sg_rna = []
    for i in range(0, len(coordinate)):
        upper_lim = int(coordinate[i]) + 100000
        lower_lim = int(coordinate[i]) - 100000
        res = requests.post("http://localhost:9200/snp/_search?pretty=true&size=1", json={
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "POS": {
                                    "gte": lower_lim, "lte": upper_lim
                                }
                            }
                        },
                        {
                            "term": {
                                "CHR": chr[i]
                            }
                        }]
                }
            }
            ,
            "sort": {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "params": {
                            "factor": int(coordinate[i])
                        },
                        "inline": "def cur = 0; cur = (params.factor - doc['POS'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                    "order": "asc"
                }
            }
        })
        data = res.json()
        sg_rna.append(data["hits"]["hits"][0]["_source"])
    return sg_rna


def exon_sgrna_peek(bs_start, bs_stop, bs_chr, annotations, binding_site):
    pool_query = ThreadPool(processes=8)
    sgrna_start = pool_query.apply_async(sg_rna, (bs_start, bs_chr))
    sgrna_stop = pool_query.apply_async(sg_rna, (bs_stop, bs_chr))
    peek_start = pool_query.apply_async(peek, args=(bs_start, bs_chr))
    peek_stop = pool_query.apply_async(peek, args=(bs_stop, bs_chr))
    exon_start = pool_query.apply_async(exon_exp, args=(bs_start, bs_chr))
    exon_stop = pool_query.apply_async(exon_exp, args=(bs_stop, bs_chr))
    gwas_final = pool_query.apply_async(gwas, args=(bs_start, bs_chr))
    snp_final = pool_query.apply_async(snp, args=(bs_start, bs_chr))

    sgrna_start = sgrna_start.get()
    sgrna_stop = sgrna_stop.get()
    peek_start = peek_start.get()
    peek_stop = peek_stop.get()
    exon_start = exon_start.get()
    exon_stop = exon_stop.get()
    gwas_final = gwas_final.get()
    snp_final = snp_final.get()

    sgrna_final = []
    peek_final = []
    exon_final = []

    for i in range(len(bs_start)):
        if int(sgrna_start[i]["BS_START"]) - int(bs_start[i]) <= int(sgrna_stop[i]["BS_END"]) - int(bs_start[i]):
            sgrna_final.append(sgrna_start[i])
        else:
            sgrna_final.append(sgrna_stop[i])
        if int(exon_start[i]["Start"]) - int(bs_start[i]) <= int(exon_stop[i]["Stop"]) - int(bs_start[i]):
            exon_final.append(exon_start[i])
        else:
            exon_final.append(exon_stop[i])
        if int(peek_start[i]["START"]) - int(bs_start[i]) <= int(peek_stop[i]["STOP"]) - int(bs_start[i]):
            peek_final.append(peek_start[i])
        else:
            peek_final.append(peek_stop[i])
    return annotations, binding_site, sgrna_final, peek_final, exon_final, gwas_final, snp_final


# ________________________________________________________END OF FUNCTIONS FOR COORDINATE BASE SEARCH____________________________________________________________________________________

def rna_bp(rbp, efficiency, specificity):
    res = requests.post("http://localhost:9200/bs/_search?pretty=true&size=100", json=
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
    return gene_exon_sgrna_peek(start, stop, efficiency, specificity, data, chr)


def gene_sg_rna(coordinate, efficiency, specificity, chr):
    sg_rna = []

    for i in range(len(coordinate)):
        a = int(coordinate[i])
        res = requests.post("http://localhost:9200/sgrna/_search?pretty=true&size=1", json={
            "query": {
                "bool": {
                    "must":
                        {"match": {"BS_CHR": chr[i]}},
                    "filter":
                        [{"range": {"Specificity": {"gte": specificity}}},
                         {"range": {"Efficiency": {"gte": efficiency}}}]
                }
            },
            "sort": {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "params": {
                            "factor": a
                        },
                        "inline": "def cur = 0; cur = (params.factor - doc['BS_START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                    "order": "asc"
                }
            }

        })
        data = res.json()
        sg_rna.append(data["hits"]["hits"][0]["_source"])
    return sg_rna


def gene_peek(coordinate, chr):
    peek_liver = []
    for i in range(0, len(coordinate)):
        a = int(coordinate[i])
        res = requests.post("http://localhost:9200/peek/_search?pretty=true&size=1", json={
            "query": {
                "term": {"CHR": chr[i]}
            },
            "sort": {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "params": {
                            "factor": a
                        },
                        "inline": "def cur = 0; cur = (params.factor - doc['START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                    "order": "asc"
                }
            }

        })
        data = res.json()
        peek_liver.append(data["hits"]["hits"][0]["_source"])
    return peek_liver


def gene_gwas(coordinate, chr):
    gwas = []
    for i in range(0, len(coordinate)):
        res = requests.post("http://localhost/gwas/_search?pretty=true&size=1", verify=False, json={
            "query": {
                "term": {"CHR_ID": chr[i]}
            },
            "sort": {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "inline": "def factor = " + str(coordinate[
                                                            i]) + "; def cur = 0; cur = (factor - doc['CHR_POS'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                    "order": "asc"
                }
            }
        })
        data = res.json()
        gwas.append(data["hits"]["hits"][0]["_source"])
    return gwas


def gene_exon_exp(coordinate, chr):
    exon_exp = []
    for i in range(0, len(coordinate)):
        a = int(coordinate[i])
        res = requests.post("http://localhost:9200/exon/_search?pretty=true&size=1", json={
            "query": {
                "term": {"CHR": chr[i]}
            },
            "sort": {
                "_script": {
                    "type": "number",
                    "script": {
                        "lang": "painless",
                        "params": {
                            "factor": a
                        },
                        "inline": "def cur = 0; cur = (params.factor - doc['START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
                    "order": "asc"
                }
            }

        })
        data = res.json()
        exon_exp.append(data["hits"]["hits"][0]["_source"])
    return exon_exp


def gene_exon_sgrna_peek(bs_start, bs_stop, efficiency, specificity, binding_site, chr):
    pool_query = ThreadPool(processes=7)
    sgrna_start = pool_query.apply_async(gene_sg_rna, (bs_start, efficiency, specificity, chr))
    sgrna_stop = pool_query.apply_async(gene_sg_rna, (bs_stop, efficiency, specificity, chr))
    peek_start = pool_query.apply_async(gene_peek, args=(bs_start, chr))
    peek_stop = pool_query.apply_async(gene_peek, args=(bs_stop, chr))
    exon_start = pool_query.apply_async(gene_exon_exp, args=(bs_start, chr))
    exon_stop = pool_query.apply_async(gene_exon_exp, args=(bs_stop, chr))
    gwas_value = pool_query.apply_async(gene_gwas(bs_start, chr))
    gwas_value = gwas_value.get()
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
    return binding_site, sgrna_final, peek_final, exon_final, gwas_value


from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def process_data():
    if request.method == "POST":
        if request.form.get("check") == "ZERO":
            coordinates = request.form["search_field"]
            chrom = request.form.get("chrom")
            if "|" in coordinates:
                coordinates = coordinates.split("|")
                annotations, bs, sgrna, peek, exons, gwas_final, snp_final = start_stop_chr(coordinates[0],
                                                                                            coordinates[1],
                                                                                            str(chrom).lower())
                return render_template("result_table.html", annotations=annotations, bs=bs, sgrna=sgrna, peek=peek,
                                       exons=exons, length=len(bs), chrom=chrom, gwas_final=gwas_final)
        elif request.form.get("check") == "ONE":
            rbp = str(request.form.get("rbp")).lower()
            specificity = 50
            efficiency = 0
            if len(request.form["specificity"]) > 0:
                specificity = request.form["specificity"]
            if len(request.form["efficiency"]) > 0:
                efficiency = len(request.form["efficiency"])

            bs, sgrna, peek, exons, gwas_value = rna_bp(rbp, efficiency, specificity)
            length = len(bs)

            return render_template("rbp_result_table.html", bs=bs, sgrna=sgrna, peek=peek, exons=exons, length=length,
                                   gwas_final=gwas_value)

    RNA_BINDING_PROTEINS = {'AKAP8L': 'ENSG00000011243', 'BCCIP': 'ENSG00000107949', 'CPSF6': 'ENSG00000111605',
                            'CSTF2T': 'ENSG00000177613', 'DDX3X': 'ENSG00000215301', 'DDX42': 'ENSG00000198231',
                            'DDX55': 'ENSG00000111364', 'DDX6': 'ENSG00000110367', 'DKC1': 'ENSG00000130826',
                            'DROSHA': 'ENSG00000113360', 'EFTUD2': 'ENSG00000108883', 'EIF3D': 'ENSG00000100353',
                            'EIF4G1': 'ENSG00000114867', 'EIF4G2': 'ENSG00000110321', 'EWSR1': 'ENSG00000182944',
                            'FAM120A': 'ENSG00000048828', 'FASTKD2': 'ENSG00000118246', 'FKBP4': 'ENSG00000004478',
                            'FMR1': 'ENSG00000102081', 'FUS': 'ENSG00000089280', 'FXR1': 'ENSG00000114416',
                            'FXR2': 'ENSG00000129245', 'GRSF1': 'ENSG00000132463', 'GTF2F1': 'ENSG00000125651',
                            'HLTF': 'ENSG00000071794', 'HNRNPA1': 'ENSG00000135486', 'HNRNPC': 'ENSG00000092199',
                            'HNRNPK': 'ENSG00000165119', 'HNRNPM': 'ENSG00000099783', 'HNRNPU': 'ENSG00000153187',
                            'HNRNPUL1': 'ENSG00000105323', 'IGF2BP1': 'ENSG00000159217', 'IGF2BP2': 'ENSG00000073792',
                            'IGF2BP3': 'ENSG00000136231', 'ILF3': 'ENSG00000129351', 'KHDRBS1': 'ENSG00000121774',
                            'KHSRP': 'ENSG00000088247', 'LARP4': 'ENSG00000161813', 'LARP7': 'ENSG00000174720',
                            'LIN28B': 'ENSG00000187772', 'LSM11': 'ENSG00000155858', 'METAP2': 'ENSG00000111142',
                            'MTPAP': 'ENSG00000107951', 'NCBP2': 'ENSG00000114503', 'NKRF': 'ENSG00000186416',
                            'NOL12': 'ENSG00000256872', 'NONO': 'ENSG00000147140', 'NPM1': 'ENSG00000181163',
                            'PCBP2': 'ENSG00000197111', 'PPIL4': 'ENSG00000131013', 'PRPF8': 'ENSG00000174231',
                            'PTBP1': 'ENSG00000011304', 'PUM2': 'ENSG00000055917', 'QKI': 'ENSG00000112531',
                            'RBFOX2': 'ENSG00000100320', 'RBM15': 'ENSG00000162775', 'RBM22': 'ENSG00000086589',
                            'RBM27': 'ENSG00000091009', 'RPS11': 'ENSG00000142534', 'RPS5': 'ENSG00000083845',
                            'SAFB2': 'ENSG00000130254', 'SBDS': 'ENSG00000126524', 'SF3A3': 'ENSG00000183431',
                            'SF3B4': 'ENSG00000143368', 'SFPQ': 'ENSG00000116560', 'SLBP': 'ENSG00000163950',
                            'SLTM': 'ENSG00000137776', 'SMNDC1': 'ENSG00000119953', 'SND1': 'ENSG00000197157',
                            'SRSF1': 'ENSG00000136450', 'SRSF7': 'ENSG00000115875', 'SRSF9': 'ENSG00000111786',
                            'TAF15': 'ENSG00000172660', 'TARDBP': 'ENSG00000120948', 'TBRG4': 'ENSG00000136270',
                            'TIA1': 'ENSG00000116001', 'TIAL1': 'ENSG00000151923', 'TNRC6A': 'ENSG00000090905',
                            'TRA2A': 'ENSG00000164548', 'TROVE2': 'ENSG00000116747', 'U2AF1': 'ENSG00000160201',
                            'U2AF2': 'ENSG00000063244', 'UPF1': 'ENSG00000005007', 'XRCC6': 'ENSG00000196419',
                            'XRN2': 'ENSG00000088930', 'YWHAG': 'ENSG00000170027', 'ZNF622': 'ENSG00000173545',
                            'ZRANB2': 'ENSG00000132485', 'AARS': 'ENSG00000090861', 'AGGF1': 'ENSG00000164252',
                            'AUH': 'ENSG00000148090', 'DGCR8': 'ENSG00000128191'}

    return render_template("index.html", RNA_BINDING_PROTEINS=RNA_BINDING_PROTEINS)


if __name__ == '__main__':
    app.run()









