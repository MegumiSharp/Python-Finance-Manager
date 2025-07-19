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




## Scelte Progettuali

Ho scelto di utilizzare SQLite come sistema di gestione dei dati per questo progetto perché offre una soluzione robusta, efficiente e scalabile, pur mantenendo una configurazione semplice e leggera. Rispetto a un approccio basato su file CSV, SQLite garantisce una maggiore integrità dei dati, permettendomi di definire tipi, vincoli e query complesse in modo sicuro e performante. Questo mi consente di ordinare, filtrare e gestire le transazioni in maniera molto più efficiente, evitando la necessità di implementare logiche manuali in Python per operazioni comuni. Inoltre, SQLite è facilmente integrabile nel progetto senza richiedere dipendenze esterne, mantenendo la portabilità e la facilità d’uso, ma con la solidità necessaria per supportare future espansioni come l’introduzione di più tabelle, categorie o statistiche.