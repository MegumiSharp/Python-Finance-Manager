# Setup

Questa schermata appare solo la prima volta che si entra nel programma, tuttavia i settaggi sono modificabili nel file presente in `data/user_settings/user_settings.json`, basterá cambiare la prima voce `is_first_time": "false` a `is_first_time": "true`, e riavviando il programma la schermata di setup dovrebbe tornare. Qui é possibile inserire il proprio `nickname` utile nella schermata di benvenuto, scegliere il simbolo della valuta visibile nella tabella delle transazioni, ed infine scegliere le percentuali per la budget view. Cliccare  `continue` usa i valori di default, e come nickname imposta `User`. I limiti imposti di scrittura sono tutti presenti all'interno, quindi basta leggere.


# Welcome View

Una schermata per scegliere il tema, il tema verrá ricordato in `user_settings.json`, cliccare il menu a tendina e cliccare un altro tema porterá direttamente all'altra schermata, altrimenti premere continua per usare l'ultimo tema utilizzato.


# Dashboard

La Dashboard é composta da una sidebar (sulla sinistra) o menu di navigazione e dal contenuto o view selezionato dal suddetto menu di navigazione. Le tre opzioni disponibili sono home, selezionata di default, budget e import/export/. Cliccando uno delle tre voci il contenutno nella parte destra viene modificato mostrando il contenuto della rispettiva sezione.


# Dashboard > Budget

Durante il seutup é stato chiesto 3 percentuali che avrebbero dato le fondamenta per la budget rule. Brevemente, benché spiegato in altri luoghi, la budget rule é un metodo per tenere traccia delle proprie finanze, e l'applicativo tramite l'utilizzo di alcuni tag speciali, permette di farlo autonomamente. Mettiamo caso che l'utente abbia uno stupendio di 2000 euro, la budget rule, prevedere che il 50% venga utilizzato per le *necessitá* (ad esempio, bollette, cibo ecc...), il 30% per acquisti wants piú variegati possibili che non comprendono le necessitá (ad esempio uscite, takout, collezionismo ecc..) ed inifne il 20% viene messo come risparmio, il risparmio dovrebbe essere un qualcosa che conscenziosamente si tiene da parte per i grossi problemi della vita o anche solo per spese critiche spuntate dal nulla, ad esempio pagare la palestra personlamente é una necessitá, ma comprare dei libri non son delle necessitá. Se la macchina avesse un guasto saremmo legittimati ad usare i risparmi per pagare la riparazione. 

Le percentuali sono modificabili da dentro il file data/user_settings_user_settings.json oppure al primo avvio dell'applicativo. Il budget che viene mostrato riguarda il mese corrente e si resetta il mese successivo. Il motivo della scritta savings this month é per ricordarsi i soldi messi da parte quel mese, difatti la barra dei risparmi verrá riempita non appena verrá rilevato un salario, questo perché si da per scontato che quella parte dei soldi non verrá usufruita e rimmarrá nel conto in banca.

Ogni transazione avente i giusti tag ed essendo negative, andranno a mostrare una volta cliccato il pulsante save changes nella home, un aggiornamento della tabella di budget mostrando in tempo reale il budget rimasto e da poter consumare. Ogni primo del mese la tabella verrá resettata e finché non verrá inserito il salario quest'ultima sará vuota.
Una volta inserito il salario, il budget verrá modificato e verranno mostrati i valori. Tutti i soldi spesi in piu in necessitá o wants, saranno di fatto tolti dai risparmi, benché questo non venga mostrato nell'effettivo. Sae in un mese non si andranno a spendere tutti i soldi dei wants e dei needs, necessariamente i soldi in piú diverranno risparmi, difatti questi soldi rimanenti non verranno contati nel mese successivo.

I tag sono case sensitive e sono i seguenti:
- "Salaray" - Per lo stipendio, importante da aggiungere per far si che il budget calcoli le percentuali
- "Needs"  - Necessitá, rimuove dall abarra delle necessitá la dovuta somma monetaria
- "Wants" - Wants, rimuove dall abarra delle Wants la dovuta somma monetaria
- "Saving" - Risparmi, rimuove dall abarra dei risparmi la dovuta somma monetaria


# Dashboard > Import/Export

Qui sará possibile importare od esportare il database nonché fare un backup e utilizzarlo come punto di ristoro.Tutti questi tasti sono incredibilmente importanti e necessitano di un doppio click su una finestra di conferma per confermare quello che si sta facendo. 

Il tasto import, controlla nella cartella `import` un file con il nome `db_import.csv`. I file csv non sono troppo dissibili da dei file di testo, quindi l'utente puío creare un file di testo con le seguenti regole e poi cambiare l'estensione da .txt a .csv. Dentro il file ogni riga corrisponde ad una transazione, la formattazione é la seguente: 

2024-03-15,880.04,Rent_42,Flight to NYC #42
2024-12-29,605.37,Health_43,Monthly rent #43
2024-05-12,325.55,Travel_48,Monthly rent #48
2024-04-18,572.72,Travel_49,Pharmacy visit #49
2024-03-31,1083.26,Rent_50,New shoes #50

L'anno deve essere in formato YYYY-MM-DD, l'ammontare monetario deve avere il . al posto della virgola e sopratutto non deve avere il simbolo monnetario. Usare - per l'ammontare negativo. Ogni riga
va a capo una volta scritta la descrizione. Data,ammontare,Tag,Descrizione é il formato da rispettare. Se tutto questo é rispettato non ci saranno problemi altrimenti un prompt con l'errore nell indice del file verrá mostrato. Una volta importato, la schermata si riavvierá e la tabella delle transizioni verrá sostituita con il file importato. Al momento il file SOSTITUISCE la tabella e quindi non permette di aggiungere voci singole, un modo per ovviare a questo problema é esportare il file in formato csv e poi aggiungere le righe che vogliamo se molteplici e poi farglielo importare una volta cambiato nome.

Il tasto export, CREA nella caretella `export` un file con il nome `db_export.csv` avente tutta la tabella di transazioni traslata in csv. I file devono essere formattati come per il file importato. Il file db_export.csv potrá essere utilizzato dall'utente qual'ora voglia modificare molte righe del codice o eliminarne alcune non di suo interesse o altre cose che a lui potrebbe interesaare fare.


Il tasto `Backup Current` Crea un backup dell'attuale tabella di transazioni sotto forma di vero e proprio database, questo viene salvato nella cartella `backup` sotto il nome di `transactions_backup.db`. Il tasto `Restore BaCKUP` usa quello stesso file, senza nessuna modifica di nome per sostituire la tabella di transazioni presente, parliamo sempre di database.


Questa parte dell'applicazione é il modo perfetto per permettere all'utente di gestire i suoi dati senza paura che accada qualcosa ad essi, tecnicamente é possibile anche resettare l'applicativo importando un file csv vuoto.


# Dashboard > Home

Il cuore pulsante dell'applicativo. Questa zona permette di gestire le prorpie finanze come transaioni monetarie dotate di data, ammontare monetario, tag e descrizione. Oltre a diversi tasti per filtrare le transazioni vi é anche una barra di ricerca in alto che se cliccata e scritta filtra in tempo reale tutta la tabella
![alt text](user_guide_images/needs_search_bar.png)

 Vediamo un attimo tutti i tasti.



- Il tasto Date se cliccato ordina in modo cronologico ascendente o discendente le transazioni nella tabella, ricliccarlo cambia il modo visualizzato
- Il tasto aAmount se cliccato ordina in modo cronologico ascendente o discendente le transazioni in base alla quanit'ta monetaria quindi dal valore maggiore al minore o vicevera, ricliccarlo cambia la modalitá visualizzata.
- Il tasto nella colonna action con la matita, é il tasto arancione edit, che permette di modificare la transazione selezionata, in questo menu pop-up é possibile cambiare ogni parte della transazione



- Il tasto rosso con la x indica il delete button, un bottone per eliminare la transizione, un messaggio di confemra richiedera l'ok da parte dell'utente