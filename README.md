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

INTRODUZIONE
Si vuole realizzare un database con l’obiettivo di gestione di una banca online europea.
Di conseguenza, la base di dati dovrà immagazzinare informazioni relative ai clienti, ai bancari e al direttore di ciascuna filiale di cui la banca dispone. 
Questo sistema si propone di ottimizzare e automatizzare le operazioni bancarie quotidiane, fornendo un servizio sicuro ed efficiente sia per i dipendenti della banca (bancari e direttore) che per i clienti.


SPECIFICHE
Una banca europea gestisce diverse filiali, ciascuna con una propria sede e un saldo. Il personale delle filiali comprende bancari e direttori. In particolare, ogni filiale ha un solo direttore, dal mandato di un anno, il quale è l’unico tra i lavoratori autorizzato ad accettare prestiti, ad approvare richieste di mutui, ad autorizzare richieste di fido, oltre che visualizzare una panoramica dei conti correnti dei clienti della filiale. Infatti, il direttore della filiale ha responsabilità amministrative e di supervisione sulle filiali e sui bancari.
Oltre al direttore, i dipendenti della filiale sono i bancari, le cui mansioni principali riguardano le richieste di registrazione avanzate dai clienti, le relative aperture dei conti correnti ed eventuali approvazioni di richiesta di attivazione di carte prepagate. 
Ogni persona può diventare cliente della banca: si entra a far parte della clientela tramite una iniziale e gratuita richiesta di apertura di conto corrente, per mezzo dell’invio dei propri dati anagrafici. Una volta attivato il conto, il cliente riceve le credenziali d’accesso, con cui può consultare il proprio home banking. L’accesso ai servizi bancari online è vincolato dal processo di autenticazione dell’utente e dall’inserimento di un codice OTP (one-time password), il quale viene generato per le operazioni che richiedono una sicurezza aggiuntiva. Ogni OTP è  univoco, ha una data di scadenza e uno stato che indica se è stato utilizzato. È associato a un membro della banca (quindi, cliente, bancario o direttore).
I clienti possono essere suddivisi in due categorie principali: ordinari e private. I clienti private sono gestiti direttamente da un bancario assegnato. Un bancario può essere supervisore di un massimo di quattro clienti private. Questo ruolo di supervisore include la gestione delle richieste specifiche, l’offerta di consulenze personalizzate e la cura delle esigenze finanziarie complesse.
 
Tutti i clienti possono usufruire dei servizi forniti dalla banca. 
In primis, essi possono avanzare molteplici richieste, soggette poi all’approvazione dei bancari, tra cui la richiesta di apertura dei conti, la richiesta di attivazione di carta prepagata, richieste di prestito, mutuo e fido.
Inoltre, ciascun cliente può possedere uno o più conti; infatti, i conti possono essere co-intestati fino ad un massimo di due persone. Ciascun conto corrente ha un saldo utilizzabile per operazioni finanziarie, ricevere accrediti e fare addebiti, oltre a poter essere collegato a carte di debito e prepagate. Le carte di debito sono utilizzate per addebitare direttamente i conti dei clienti, mentre le carte prepagate sono ricaricabili con un saldo specifico.
Per i prestiti e i mutui, i clienti possono fornire delle garanzie a tutela del finanziatore qualora il cliente non riesca a rimborsare l’importo erogato dalla banca. I mutui offerti dalla banca prevedono delle rate che il cliente deve pagare periodicamente. La rateizzazione del mutuo è stabilita al momento della stipula del contratto, definendo l’importo di ciascuna rata e la frequenza dei pagamenti.
In più, i clienti hanno anche la possibilità di sottoscrivere polizze assicurative emesse da enti assicurativi, che fungono da strumento finanziario con l'obiettivo di risparmiare nel medio-lungo periodo o proteggere il capitale dall'inflazione e altri rischi finanziari con costi inferiori rispetto al deposito bancario. Tali polizze sono domiciliarizzate sul conto corrente del cliente, cioè i pagamenti periodici relativi vengono addebitati direttamente sul conto corrente del cliente presso la filiale. 
Da ultimo, i clienti possono partecipare al mercato azionario. Infatti, un cliente può disporre di un portafoglio azionario, che si compone di più posizioni in vari titoli, finanziato dal conto corrente proprio del cliente. 
Nell'ambito del sistema informativo in questione, una transazione rappresenta qualsiasi movimento finanziario che coinvolge i conti correnti dei clienti, come un bonifico effettuato verso un altro conto, il pagamento di un bollettino o la ricarica della propria carta prepagata. Le transazioni possono essere di vari tipi e possono essere classificate in più categorie a seconda della loro natura e destinazione.
Infatti, le transazioni possono essere interne, qualora riguardino conti correnti appartenenti alla stessa banca, o esterne, dunque dirette verso o provenienti da conti correnti non appartenenti alle filiali della banca, e che pertanto non sono gestite dal sistema informativo sviluppato.

