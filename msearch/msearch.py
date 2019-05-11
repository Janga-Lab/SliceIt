from elasticsearch import Elasticsearch
from multiprocessing.pool import ThreadPool
import requests
import pprint

def rna_bp(rbp, efficiency,specificity):
    res = requests.post("http://localhost:9200/lab/binding_site/_search?scroll=20m&pretty=true&size=300", json=
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
    #return res.json()

def sgrna(factor, efficiency, specificity, chr):
    es = Elasticsearch()
    minimum = min(factor)
    request = []
    min(factor)

    for i in range(len(chr)):
        lower_lim = int(factor[i]) - 100000
        upper_lim = int(factor[i]) + 100000
        req_head = {'index': 'lab', 'type': 'sg_rna'}
        req_body = {
                      "query": {
                        "bool": {
                          "must": [
                            {
                              "range": {
                                "BS_START": {
                                  "gte": lower_lim , "lte" : upper_lim
                                }
                              }
                            },
                            {
                              "term": {
                                "BS_CHR": "chr1"
                              }
                            },
                            {
                              "range": {
                                "Efficiency": {
                                  "gte": 0.3
                                }
                              }
                            },
                            {
                              "range": {
                                "Specificity": {
                                  "gte": 10
                                }
                              }
                            }      ]
                        }
                      }
                    ,
        "sort" : {
            "_script" : {
                "type" : "number",
                "script" : {
                    "lang": "painless",
                    "params": {
                  "factor": int(factor[i])
                },
                    "inline": "def cur = 0; cur = (params.factor - doc['BS_START'].value); if (cur < 0) { cur = cur * -1 } else { cur = cur}" },
                "order" : "asc"
                }
            }
        }
        request.extend([req_head, req_body])
    resp = es.msearch(body=request)
    response = []
    for i in range(len(resp["responses"])):
        response.append(resp['responses'][i]['hits']["hits"][0]["_source"])
    return response

def gene_exon_sgrna_peek(bs_start,bs_stop,efficiency,specificity, binding_site,chr):
    pool_query = ThreadPool(processes=2)
    sgrna_start = pool_query.apply_async(sgrna, (bs_start, efficiency, specificity, chr))
    sgrna_stop = pool_query.apply_async(sgrna, (bs_stop, efficiency, specificity, chr))
    sgrna_start = sgrna_start.get()
    sgrna_stop = sgrna_stop.get()
    sgrna_final = []
    for i in range(len(bs_start)):
        if int(sgrna_start[i]["BS_START"]) - int(bs_start[i]) <= int(sgrna_stop[i]["BS_END"]) - int(bs_start[i]):
            sgrna_final.append(sgrna_start[i])
        else:
            sgrna_final.append(sgrna_stop[i])
    return sgrna_final

def scroll(id):
    res = requests.post("http://localhost:9200/_search/scroll?scroll=1m&scroll_id=DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAALFm1KZmlDa21yVE1PeThSM0oyaEV3RncAAAAAAAAADBZtSmZpQ2ttclRNT3k4UjNKMmhFd0Z3AAAAAAAAAA0WbUpmaUNrbXJUTU95OFIzSjJoRXdGdwAAAAAAAAAOFm1KZmlDa21yVE1PeThSM0oyaEV3RncAAAAAAAAADxZtSmZpQ2ttclRNT3k4UjNKMmhFd0Z3")
    return res.json()


bs = rna_bp("eif3d",0.3,50); pprint.pprint(bs)

#print(scroll(1))




