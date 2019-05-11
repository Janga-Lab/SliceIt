import requests

def rna_bp(rbp):
    res = requests.post("http://localhost:9200/lab/binding_site/_search?pretty=true&size=500", json=
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
    return start,stop,chr


def start_stop_chr(start,stop,chr):
    res = requests.post("http://localhost:9200/lab/annotations/_search?pretty=true&size=900", json=
    {
        "query": {
            "bool": {
                "must": [
                    {"match": {"CHROM": chr}}
                ],
                "filter":
                    {"range": {"START": {"gte": start, "lte": stop}}}

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
        if len(start) > 0:
            return binding_site(min(start), max(stop), chr[0], data)
        else:
            return binding_site(start, stop, chr, data)


def binding_site(start,stop,chr,annotations):
    res = requests.post("http://localhost:9200/lab/binding_site/_search?pretty=true", json={
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
        res = requests.post("http://localhost:9200/lab/sg_rna/_search?pretty=true&scroll=10m&size=1", json={
        "query": {
            "term": {"BS_CHR": chr[i]}
        },
        "sort" : {
            "_script" : {
                "type" : "number",
                "script" : {
                    "lang": "painless",
                    "inline": "def factor = "+ str(coordinate[i]) +  "; def cur = 0; cur = (factor - doc['BS_START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}"},
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
        res = requests.post("http://localhost:9200/lab/peek_liver/_search?pretty=true&scroll=10m&size=1", json={
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
        res = requests.post("http://localhost:9200/lab/exonexpression/_search?pretty=true&scroll=10m&size=1", json={
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

def gene_exon_sgrna_peek(bs_start,bs_stop,bs_chr,annotations,binding_site):
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

annotations, bs, sgrna, peek, exons = rna_bp("cstf2t")

print(bs)

#print(" Annotations: ",annotations, "\n _________________________________________________________________________")
for i in range(0,len(sgrna)):
    print(" Binding Site: " ,bs[i],"\n","SG_RNA: " , sgrna[i], "\n", "PEEK_LIVER: ",peek[i], "\n", "EXON_EXPRESSION: ",exons[i], "\n_________________________________________________________________________")