from sqlalchemy import text
from . import db

def get_conti_correnti_by_direttore_id(direttore_id):
    query = text("""
        SELECT cc.*
        FROM conti_correnti cc
        JOIN filiali f ON cc.filiale_id = f.id
        JOIN storico_direzione sd ON f.id = sd.filiale_id
        WHERE sd.direttore_id = :direttore_id
          AND sd.year = YEAR(CURDATE());
    """)
    result = db.session.execute(query, {'direttore_id': direttore_id})
    return result.fetchall()

def get_transazioni_by_conto_corrente_id(conto_corrente_id):
    query = text("""
        SELECT t.*
        FROM transazioni t
        JOIN transazioni_interne ti ON t.transazione_interna_id = ti.id
        WHERE ti.conto_corrente_id = :conto_corrente_id;
    """)
    result = db.session.execute(query, {'conto_corrente_id': conto_corrente_id})
    return result.fetchall()