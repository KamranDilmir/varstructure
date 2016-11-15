import flask
import sqlite3

app = flask.Flask(__name__)

DB = "PDB_Chain_Uniprot.db"

### database access
def db():
    db_instance = getattr(flask.g, '_database', None)
    if db_instance is None:
        db_instance = flask.g._database = sqlite3.connect(DB)
    return db_instance

def query_db(query, args=(), one=False):
    cur = db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def close_connection(exception):
    db_instance = getattr(flask.g, '_database', None)
    if db_instance is not None:
        db_instance.close()
def main():
    #print("This is hte python code which executes first")
    '''
        main entry point
    '''
    #if flask.request.method == 'POST':
        #print("in post")
        #return process()
    #else:
        #return flask.render_template('main.html', form=flask.request.form)

@app.route('/')
def index():
    '''
        analysis
    '''
    result = []
    con = sqlite3.connect("PDB_Chain_Uniprot.db")
    cur = con.cursor()
    cur.execute("SELECT a.Chrom,a.POS,a.Vep_ID,a.REF,a.ALLELE,a.Consequence,a.Protein_position, a.Amino_acids, \
                b.PDB,b.PDB_BEG,b.PDB_END,a.SIFT, a.PolyPhen,b.CHAIN,b.SP_Primary,b.Swissprot_id,max(b.Res_LEN) as RES_Length \
                FROM Input_VCF_CSQ AS a LEFT JOIN  PDB_Chain_Uniprot AS b ON a.SWISSPROT = b.Swissprot_Id \
                WHERE a.CANONICAL ='YES' AND Consequence= 'missense_variant' GROUP BY b.Swissprot_Id LIMIT 200;")
    matches= cur.fetchall()
    #matches = query_db(("SELECT * FROM Input_VCF_CSQ LIMIT 10"),"",one=True)
    errors = []
    #find matching genes
    #matches = query_db(("SELECT * FROM Input_VCF_CSQ AS a JOIN PDB_Chain_Uniprot AS b ON a.SWISSPROT=b.Swissprot_Id WHERE Consequence IS NOT NULL "),"",one=False)
    #print(matches)
    for match in matches:
    #if matches[1] is not None:
        print match
        result.append({'Chrom': str(match[0]), 'POS': str(match[1]), 'Id': str(match[2]), 'REF': str(match[3]),'ALLELE': str(match[4]),'Consequence': str(match[5]),
        'Protein_position': str(match[6]),'Amino_acids': str(match[7]),'PDB': str(match[8]),
        'PDB_BEG': str(match[9]),'PDB_END': str(match[10]),
        'SIFT': str(match[11])[str(match[11]).find("(") + 1:str(match[11]).find(")")],
        'SIFT_Description': str(match[11])[0:str(match[11]).find("(")],
        'PolyPhen': str(match[12])[str(match[12]).find("(") + 1:str(match[12]).find(")")],
        'PolyPhen_Description': str(match[12])[0:str(match[12]).find("(")],'CHAIN': str(match[13]),
        'SP_Primary': str(match[14]),'RES_Length': str(match[16])})
    #else:
        # gene is no good
        #warnings.append( 'Gene "{}" had no matches'.format(fields[0]))

    #if len(errors) == 0:
    return flask.render_template('index.html',result=result)

if __name__ == '__main__':
    #app.run(debug=False,host='127.0.0.0')
    #app.run()
    main()
    app.run()
