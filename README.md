# Personal Finance Tracker with AI Insights (Work in Progress)

A comprehensive personal finance management application built in Python that helps you track expenses, visualize spending patterns, and get AI-powered insights about your financial habits.

## 🚀 Features

### Current Features
- Project Started

### Planned Features
- **Expense Management**: Add, edit, and delete transactions with ease
- **Local Data Storage**: Secure SQLite database for all your financial data
- **Category Organization**: Automatic and manual expense categorization
- **Data Visualization**: Interactive charts showing spending trends and patterns
- **Budget Tracking**: Set monthly budgets and track your progress
- **Smart Analytics**: Get insights into your spending habits
- **AI-Powered Categorization**: Automatic expense categorization using machine learning
- **Predictive Analytics**: Forecast future expenses and savings opportunities
- **Multi-Account Support**: Track multiple bank accounts and payment methods
- **Recurring Transactions**: Templates for regular bills and income
- **Export Capabilities**: CSV and PDF report generation
- **Desktop GUI**: User-friendly graphical interface

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **SQLite**: Local database for data persistence
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Plotly**: Data visualization and charts
- **Tkinter**: GUI framework (planned)
- **Hugging Face Transformers**: AI-powered text classification (planned)



### Basic Commands
- **Add Expense**: Record a new transaction
- **View Expenses**: Display transaction history
- **Monthly Summary**: Get spending overview for specific months
- **Category Analysis**: Breakdown expenses by category
- **Budget Management**: Set and track monthly budgets

## 📊 Screenshots

*Screenshots will be added as features are implemented*


## 📝 Development Roadmap

### Phase 1: Core Foundation ✅
- [ ] Basic CLI interface
- [ ] SQLite database setup
- [ ] CRUD operations for transactions
- [ ] Data validation and error handling

### Phase 2: Data Analysis 🚧
- [ ] Pandas integration for data manipulation
- [ ] Basic reporting features
- [ ] CSV import/export functionality

### Phase 3: Visualization 📅
- [ ] Matplotlib chart generation
- [ ] Spending trend analysis
- [ ] Category breakdown visualizations

### Phase 4: AI Integration 📅
- [ ] Manual categorization system
- [ ] Keyword-based auto-categorization
- [ ] Machine learning categorization
- [ ] Spending pattern insights

### Phase 5: GUI Development 📅
- [ ] Tkinter desktop interface
- [ ] User-friendly forms and displays
- [ ] Interactive charts integration



## 📦 Requirements

- Python 3.10 o superiore
- pip
- `tkinter` (installabile via apt)
- Supporto GUI (WSLg o X Server)

---

## 🚀 Installazione

### 1. Clona il repository

```bash
git clone https://github.com/tuo-username/nome-del-progetto.git
cd nome-del-progetto
```
### Installa le dipendenze
```bash
pip install -r requirements.txt
pip install customtkinter


sudo apt update
sudo apt install python3-tk
```

Su windows 11

```bash
python3 src/gui.py
```


## 🐛 Known Issues

- None currently reported

---

themes are from https://github.com/a13xe/CTkThemesPack?tab=readme-ov-file
and from customtkinter theme builder by...


## Scelte Progettuali

Ho scelto di utilizzare SQLite come sistema di gestione dei dati per questo progetto perché offre una soluzione robusta, efficiente e scalabile, pur mantenendo una configurazione semplice e leggera. Rispetto a un approccio basato su file CSV, SQLite garantisce una maggiore integrità dei dati, permettendomi di definire tipi, vincoli e query complesse in modo sicuro e performante. Questo mi consente di ordinare, filtrare e gestire le transazioni in maniera molto più efficiente, evitando la necessità di implementare logiche manuali in Python per operazioni comuni. Inoltre, SQLite è facilmente integrabile nel progetto senza richiedere dipendenze esterne, mantenendo la portabilità e la facilità d’uso, ma con la solidità necessaria per supportare future espansioni come l’introduzione di più tabelle, categorie o statistiche.


Dopo i primi 30 commit, e dopo aver creato di fatto la schermata di settaggi dell'utente, una schermata per la scelta del tema, e la home, si é deciso di fare refactoring.
Per migliorare la scalabilità del programma, nonché la facilità di lettura e comprensione, si è deciso di effettuare un refactoring tempestivo del codice, concentrandosi sulla compartimentalizzazione e l’estrapolazione dei componenti che rendevano i file troppo lunghi. Un esempio emblematico di questo problema è il file app.py, che gestisce la GUI e rappresenta quindi la struttura portante dell’interfaccia grafica.

A causa della natura di customtkinter (o di tkinter stesso), il file contiene un numero relativamente cospicuo di righe di codice pur includendo tre frame. Per migliorarne ulteriormente la leggibilità, i prossimi step del refactoring prevedono l’estrazione di questi frame in file separati, così da ottenere un codice — sebbene più dispersivo per via dell’aumento del numero di file — più pulito, semplice da leggere e coerente con la professionalità attesa da un applicativo proprietario.


Determinate volte mi sono trovato a decidere se inserire dei commenti o meno, ma ho cercato di rendere il mio codice il piú comprensibile possibile, quindi molte volte ho optato per evitare di commentare funzioni comprensibili. Per quanto riguarda custom tkinter, piú di quello che ho scritto mi é stato impossibile farlo, le librerie grafiche ui di python da quello che ho visto 
non sono ottimizzate e richiedono un enorme quantita di linee di codice per cose anche semplici in altri environment tipo web development. Per questo motivo, molto del lavoro sulla gui
é stato un trial and error con un aiuto esterno da parte di cloude sonnet, il quale é stato essenziale visto la poca documentazione di custom tkinter rispetto al suo derivante.

Una scelta progettuale che probabilmente potrebbe risultare impopolare é su come ho gestito settings.py, un elenco di costanti che vengono utilizzate all'interno di tutto il programma e che permettono di modificare in qualsiasi momento l'andamento del programma comodamente da un solo file. Credo e spero che questo non sia motivo di diatribe, ma come ho gestito il default user settings, creando costanti sia per le chiavi che per i valori di default potrebbe sembrare al quanto strano. La motivazione dietro a questa scelta é semplicemente il voler evitare probelmi di typo nel codice, usando costanti che vengono riconosciute e segnalate subito. A fine progetto vorró fare dei test di velocitá per comprendere se questo abbia rallentato l'applicativo, ma per ora, credo sia un giusto compromesso per la leggibilitá e la comprensione del codice, obbitettivo che io ho deciso di mettere al primo posto.

Parliamoci chiaro, questo progetto a livello logico é al quanto semplice, é un applicativo CRUD (cREATE, READ, update and delete) e la parte piú difficile é concepire la resterizzazione della GUI, tuttavia il mio desiderio di mostrare la mia determinazione nell'imparare, comprendere ed applicare metodologie di lavoro serie e professionali, sia quello che contraddistingue questo progetto.  Molte delle scelte effettuate non erano necessarie a ficnhe il progetto fosse funzionante e facesse quello che deve fare, ma la fiamma di mostrare e presentare un progetto con una documentazione, struttura file, e scrittura del codice pulito mi ha spinto a creare il progetto come qui mostrato. Sono al corrente di non esserci riuscito in pieno, e magari di aver fatto tanti sbagli, ma essendo il mio primo progetto al di fuori dell'universitá, su argomenti che in uni non sono mai stati trattati, o trattati troppo superficialmente, be, mi rende orgoglioso di quello che ho fatto.