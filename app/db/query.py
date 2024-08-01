from datetime import datetime
from flask import cli
from sqlalchemy import text
from . import Cliente, Filiale, StoricoDirezione, db

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
    return [item for item in result.fetchall()]

def get_filiale_by_direttore_id(direttore_id):
    current_year = datetime.now().year
    
    # Retrieve the filiale using the Direttore ID
    filiale = db.session.query(Filiale).join(StoricoDirezione).filter(
        StoricoDirezione.direttore_id == direttore_id,
        StoricoDirezione.year == current_year
    ).first()
    
    return filiale

def get_most_spending_clients_for_filiale(filiale_id: int):
    query = text("""SELECT cc.cliente1_id, SUM(t.importo) AS total_importo
        FROM transazioni t
        JOIN transazioni_interne ti ON t.transazione_interna_id = ti.id
        JOIN conti_correnti cc ON ti.conto_corrente_id = cc.id
        WHERE cc.filiale_id = :filiale_id
        AND YEAR(t.data) = YEAR(CURDATE())
        AND MONTH(t.data) = MONTH(CURDATE())
        AND t.entrata = False
        GROUP BY cc.cliente1_id
        ORDER BY total_importo DESC
        LIMIT 5;""")
    
    stmt = db.session.execute(query, {'filiale_id': filiale_id})
    result = stmt.fetchall()
    
    # get a list of client ids from result
    client_ids = [row.cliente1_id for row in result]
    
    # get clients in the list
    clients = db.session.query(Cliente).filter(Cliente.id.in_(client_ids)).all()
    
    # add total_importo to each client
    for client in clients:
        for row in result:
            if row.cliente1_id == client.id:
                client.__setattr__("spesa_totale", row.total_importo)
                
    return clients
                