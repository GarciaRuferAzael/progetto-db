# Progetto Basi di Dati 
## a.a. 2023/2024
Sito per la gestione di una banca online
Si vuole realizzare un sistema informativo di gestione di una banca online europea. 
La banca dispone di un proprio saldo dal quale attingere per erogare prestiti. I dipendenti che vi lavorano sono i bancari e il direttore. 
Ciascun cliente può diventare tale tramite una iniziale e gratuita richiesta di apertura di conto corrente, per mezzo dell’invio dei propri dati anagrafici, che deve essere approvata da un bancario. Una volta attivato il conto, il cliente riceverà le credenziali d’accesso, con cui potrà consultare il proprio home banking, già provvisto di un bonus di 100€ fornito dalla banca.

Per semplicità, le transazioni dirette verso conti correnti non registrati all’interno della banca saranno lasciate in sospeso, nell’ottica di una gestione di terze parti. Inoltre, non saranno gestiti flussi in entrata dall’esterno.
In particolare, si ricorda che l’unica valuta ammessa è l’Euro.

Le funzionalità offerte dalla piattaforma per il cliente sono le seguenti:
- consultazione saldo conto corrente;
- consultazione storico operazioni;
- consultazione/aggiornamento informazioni anagrafiche;
- aggiornamento password;
- richiesta prestito;
- richiesta di aggiunta di carta prepagata;
- visualizzazione delle statistiche del conto bancario:
  - entrate medie mensili;
  - uscite medie mensili;
- consultazione carte prepagate:
  - storico transazioni;
  - visualizzazione pin;
  - impostazione limite di spesa singola;
  - impostazione limite di spesa mensile;
  - blocco carta prepagata;
- effettuare transazioni/operazioni (su cui si applica una commissione percentuale fissa): 
  - bonifici;
  - ricarica carta prepagata;
- chiusura conto.

Le funzionalità offerte dalla piattaforma per il direttore sono le seguenti:
- approvazione richieste di prestito;
- visualizzazione conti correnti;
- blocco conto;
- blocco carta prepagata.

Le funzionalità offerte dalla piattaforma per il bancario sono le seguenti:
- approvazione richiesta di registrazione cliente e apertura conto;
- approvazione richiesta di attivazione di carta prepagata.

Informazioni aggregate:
- Visualizzazione della lista ordinata di bancari e del relativo numero di richieste di apertura di conto approvate;
- visualizzazione dell’elenco dei prestiti in scadenza nell’arco di 30/60/90 giorni;
- visualizzazione del cliente più alto spendente;
- visualizzazione del numero di prestiti attivi, da approvare ed estinti.
