import json
import os
import unicodedata

escape_chars=["\n","\r","\t","\\","\'","\"","\a","\b","\f","\v"]


def check_escape_chr(ch):
    if ch in escape_chars or ch.isspace():
        return False
    else:
        return True

import os
rootdir = '../../../data/corpus-bioarxiv-250-plus-gold-annotations'
rootdir2='../../../data/corpus-bioarxiv-250-plus-gold'
target_file='input_file.txt'
target_string=""
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file!=".DS_Store":
            path=os.path.join(subdir, file)
            path2=os.path.join(rootdir2,file[:-12],"textgrid.json")
            print path
            print path2

            with open(path,'r') as f:
                ip=json.load(f)

            with open(path2,'r') as f2:
                page_size=json.load(f2)

            pgs=page_size['pages']
            for pgs_ele in pgs:
                page_x,page_y=pgs_ele['pageGeometry'][2],pgs_ele['pageGeometry'][3]

            final_string=""

            annotation=ip['annotations']
            page_records={}
            all_tokens=[]
            all_pages=[]
            for annot in annotation:
                off_labels={}
                body=annot['body']
                if body:
                    labels=body['labels']
                    clabels=labels['cellLabels']
                    tmp_arr=[]
                    offsets=[]
                    # curr_page=annot['page']
                    if len(clabels)>0:
                        for c in clabels:
                            c2=c[1]
                            #print c[0]

                            if len(c2)>0:
                                for i in c2:
                                    tmp=i[0]
                                    #print tmp[0],tmp[1],tmp[2]
                                    tmp_arr+=["I-"+tmp[0]]*(tmp[2])
                                    offsets+=xrange(tmp[1],tmp[1]+tmp[2])
                                    #print offsets
                                    #print tmp_arr
                            else:
                                tmp_arr+=["I-"+c[0][0]]*(c[0][2])
                                offsets+=xrange(c[0][1],c[0][1]+c[0][2])
                            #print len(tmp_arr)
                            #print len(tmp_arr)==(c[0][2])
                            off_labels={offsets[i]:tmp_arr[i] for i in range(len(tmp_arr))}
                            #print off_labels

                        rows=body['rows']
                        for r in rows:
                            offset_local=r['offset']
                            token_local=''

                            loci_local=r['loci']
                            curr_token=0
                            # for l in loci_local:
                            #     if "g" in l:
                            #
                            #         token_local[curr_token]+=l['g'][0][0]
                            #     else:
                            #         curr_token+=1
                            start_x,start_y,end_x,end_y=0,0,0,0
                            for l in range(len(loci_local)):
                                # if l==len(loci_local)-1:
                                #     print "last"
                                # if l==0 and "g" in loci_local[l]:
                                #     start_x,start_y=loci_local[l]['g'][0][2][0],loci_local[l]['g'][0][2][1]
                                #     local_page=loci_local[l]['g'][0][1]
                                if "g" in loci_local[l]:

                                    #print "character:",loci_local[l]['g'][0][0]

                                    if check_escape_chr(loci_local[l]['g'][0][0]):
                                        token_local+=loci_local[l]['g'][0][0]
                                        token_local=unicodedata.normalize("NFKD",token_local)
                                        if start_x==0 and start_y==0:
                                            start_x,start_y=loci_local[l]['g'][0][2][0],loci_local[l]['g'][0][2][1]
                                            local_page=loci_local[l]['g'][0][1]
                                    # token_local=token_local.replace(u'\xa0',u' ')
                                    #print token_local
                                if ("i" in loci_local[l]):
                                    # print token_local
                                    #print "character:",loci_local[l]['i'][0][0]
                                    # print "elif",token_local
                                    if "g" in loci_local[l-1]:
                                        end_x=loci_local[l-1]['g'][0][2][0]+loci_local[l-1]['g'][0][2][2]
                                        end_y=loci_local[l-1]['g'][0][2][1]+loci_local[l-1]['g'][0][2][3]


                                        if offset_local in off_labels:
                                            label_local=off_labels[offset_local]
                                        else:
                                            label_local="0"
                                        all_tokens.append((token_local,start_x,start_y,end_x,end_y,label_local,local_page))
                                        start_x,start_y=0,0
                                        token_local=''
                                elif (l==(len(loci_local)-1)):
                                    # print token_local
                                    #print "character:",loci_local[l]['i'][0][0]
                                    # print "elif",token_local
                                    # if len(token_local)>1:
                                    #     end_x=loci_local[l-1]['g'][0][2][0]+loci_local[l-1]['g'][0][2][2]
                                    #     end_y=loci_local[l-1]['g'][0][2][1]+loci_local[l-1]['g'][0][2][3]
                                    # else:

                                    end_x=loci_local[l]['g'][0][2][0]+loci_local[l]['g'][0][2][2]
                                    end_y=loci_local[l]['g'][0][2][1]+loci_local[l]['g'][0][2][3]

                                    if offset_local in off_labels:
                                        label_local=off_labels[offset_local]
                                    else:
                                        label_local="0"
                                    all_tokens.append((token_local,start_x,start_y,end_x,end_y,label_local,local_page))
                                    start_x,start_y=0,0
                                    token_local=''

                    else:
                        label=annot['label']
                        rows=body['rows']
                        for r in rows:
                            offset_local=r['offset']
                            token_local=''

                            loci_local=r['loci']
                            curr_token=0
                            # for l in loci_local:
                            #     if "g" in l:
                            #
                            #         token_local[curr_token]+=l['g'][0][0]
                            #     else:
                            #         curr_token+=1
                            start_x,start_y,end_x,end_y=0,0,0,0
                            for l in range(len(loci_local)):
                                # if l==len(loci_local)-1:
                                #     print "last"
                                # if l==0:
                                #     start_x,start_y=loci_local[l]['g'][0][2][0],loci_local[l]['g'][0][2][1]
                                #     local_page=loci_local[l]['g'][0][1]
                                if "g" in loci_local[l]:
                                    #print "character:",loci_local[l]['g'][0][0]

                                    if check_escape_chr(loci_local[l]['g'][0][0]):
                                        token_local+=loci_local[l]['g'][0][0]
                                        token_local=unicodedata.normalize("NFKD",token_local)
                                        if start_x==0 and start_y==0:
                                            start_x,start_y=loci_local[l]['g'][0][2][0],loci_local[l]['g'][0][2][1]
                                            local_page=loci_local[l]['g'][0][1]
                                    #print token_local
                                if ("i" in loci_local[l]):
                                    # print token_local
                                    #print "character:",loci_local[l]['i'][0][0]
                                    # print "elif",token_local
                                    if "g" in loci_local[l-1]:
                                        end_x=loci_local[l-1]['g'][0][2][0]+loci_local[l-1]['g'][0][2][2]
                                        end_y=loci_local[l-1]['g'][0][2][1]+loci_local[l-1]['g'][0][2][3]

                                    # if offset_local in off_labels:
                                    #     label_local=off_labels[offset_local]
                                    # else:
                                    #     label_local="0"
                                        label_local="I-"+annot['label']
                                        all_tokens.append((token_local,start_x,start_y,end_x,end_y,label_local,local_page))
                                        start_x,start_y=0,0
                                        token_local=''
                                elif (l==(len(loci_local)-1)):
                                    # print token_local
                                    #print "character:",loci_local[l]['i'][0][0]
                                    # print "elif",token_local

                                    end_x=loci_local[l]['g'][0][2][0]+loci_local[l]['g'][0][2][2]
                                    end_y=loci_local[l]['g'][0][2][1]+loci_local[l]['g'][0][2][3]

                                    # if offset_local in off_labels:
                                    #     label_local=off_labels[offset_local]
                                    # else:
                                    #     label_local="0"
                                    label_local="I-"+annot['label']
                                    all_tokens.append((token_local,start_x,start_y,end_x,end_y,label_local,local_page))
                                    start_x,start_y=0,0
                                    token_local=''

            page_wise={}
            for ele in all_tokens:
                if ele[6] not in all_pages:
                    all_pages.append(ele[6])
                    page_wise[ele[6]]=[]
                    page_wise[ele[6]].append(list(ele)[:-1])
                else:
                    page_wise[ele[6]].append(list(ele)[:-1])

            for pg in all_pages:
                target_string+=path
                target_string+="\n"
                tmp="0:0:"+str(page_x)+":"+str(page_y)+"\n"
                target_string+=tmp
                tokens=page_wise[pg]
                for ele in tokens:
                    target_string+=(ele[0].encode('utf-8')+" "+str(ele[1])+":"+str(ele[2])+":"+str(ele[3])+":"+str(ele[4])+" * "+str(ele[5]))
                    target_string+="\n"
                target_string+="\n"

            f=open(target_file,'a')
            f.write(target_string)
            f.close()
            target_string=""
