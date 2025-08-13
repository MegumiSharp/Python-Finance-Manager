# Observer Pattern Implementation Documentation


## Overview

This documentation describes the implementation of the **Observer Pattern** in the application. The pattern enables automatic UI updates when transaction data changes, creating a responsive and maintainable user interface.


The `home_view` is responsible for showing the transactions table and updating the summary. However, a problem I encountered is that the summary resides inside `home_view`, while the transactions are inside a virtual table, which is an instance of the class used in `home_view`.
This should be fine by passing a parameter of the summary labels to be changed inside the virtual table, but it wasn’t the best approach.

In this scenario, I usually ask AI — without asking for the actual solution — to give me a list of best approaches, and then I decide which one to implement.



## Design Pattern Fundamentals


The Observer Pattern defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.



1. **Subject (Observable)**: The object being watched for changes
2. **Observer**: Objects that want to be notified of changes
3. **Notification Mechanism**: Method to alert observers of state changes
4. **Callback Functions**: Functions executed when notifications are received

### Pattern Flow

```
[Data Change] → [Subject Notifies] → [Observers Update] → [UI Refreshes]
```

---

## Implementation Architecture



```
┌─────────────────┐    registers callback    ┌──────────────────┐
│   HomeView      │ ────────────────────────→│   VirtualTable   │
│   (Observer)    │                          │   (Subject)      │
├─────────────────┤                          ├──────────────────┤
│ - summary_labels│                          │ - summary_callback│
│ + on_summary_   │ ←────────────────────────│ + _notify_summary│
│   updated()     │    calls callback        │   _changed()     │
└─────────────────┘                          └──────────────────┘
```

### Data Flow Diagram

```
User Action (Filter/Delete/Search)
            ↓
VirtualTable Method (show_income, show_expenses, etc.)
            ↓
_notify_summary_changed()
            ↓
_calculate_summary() → Returns summary data
            ↓
Callback Function (on_summary_updated)
            ↓
UI Labels Updated in HomeView
```


## Code Structure



#### Observer Management
```python
class VirtualTable(BaseView):
    def __init__(self, parent, controller, data, user):
        super().__init__(parent)
        # ... existing initialization ...
        
        # Observer pattern: callback for summary updates
        self.summary_callback = None
        
    def register_summary_callback(self, callback_function):
        """Register a callback function to be called when summary needs updating"""
        self.summary_callback = callback_function
```

#### State Change Notification
```python
def _notify_summary_changed(self):
    """Calculate summary and notify observer"""
    if self.summary_callback:
        summary_data = self._calculate_summary()
        self.summary_callback(summary_data)
```

#### Data Calculation
```python
def _calculate_summary(self):
    income = 0
    expenses = 0
    transactions = 0

    for widget in self.widgets_list:
        if widget.winfo_manager():
            amount = float(widget.winfo_children()[1].cget("text").removesuffix(self.currency_sign))
            
            if amount > 0:
                income += amount
            else:
                expenses += amount
            
            transactions += 1

    return{
        KEY_SUM_TRANSACTIONS: transactions,
        KEY_SUM_INCOME: income,
        KEY_SUM_EXPENSES: expenses,
        KEY_SUM_BALANCE: (income + expenses)
    }
```

#### Integration with Existing Methods
```python
def show_income(self):
    ...
    self._notify_summary_changed()  # ← Added notification

def show_expenses(self):
    ...
    self._notify_summary_changed()  # ← Added notification

def show_searched(self, text):
    ...
    self._notify_summary_changed()  # ← Added notification

def _ok_event(self, frame, idx):
    ...
    self._notify_summary_changed()  # ← Added notification
```

### Observer Implementation (HomeView)

#### Observer Registration
```python
def setup_summary_panel(self):
    ...
    
    # Store label references as instance variables
    self.summary_labels = {
        KEY_SUM_TRANSACTIONS: transaction_value_label,
        KEY_SUM_INCOME: income_value_label,
        KEY_SUM_EXPENSES: expenses_value_label,
        KEY_SUM_BALANCE: balance_value_label
    }

    # Register the callback with VirtualTable
    self.transactions_table.register_summary_callback(self.on_summary_updated)
    
    # Initial update
    self.on_summary_updated(self.transactions_table._calculate_summary())
```

#### Callback Implementation
```python
def on_summary_updated(self, summary_data):
    """Callback function called when summary data changes"""
    self.summary_labels[KEY_SUM_TRANSACTIONS].configure(text=f"{summary_data[KEY_SUM_TRANSACTIONS]}")
    self.summary_labels[KEY_SUM_INCOME].configure(text=f"{summary_data[KEY_SUM_INCOME]:.2f}{self.currency_sign}")
    self.summary_labels[KEY_SUM_EXPENSES].configure(text=f"{summary_data[KEY_SUM_EXPENSES]:.2f}{self.currency_sign}")
    self.summary_labels[KEY_SUM_BALANCE].configure(text=f"{summary_data[KEY_SUM_BALANCE]:.2f}{self.currency_sign}")

    # Dynamic color updates based on balance
    if summary_data['balance'] >= 0:
        self.summary_labels[KEY_SUM_BALANCE].configure(
            text_color=COLOR_INCOME)
    else:
        self.summary_labels[KEY_SUM_BALANCE].configure(
            text_color=COLOR_EXPENSE)

```

## Conclusion

The Observer Pattern implementation provides a robust, maintainable solution for keeping UI components synchronized with data changes.  This pattern is particularly valuable in GUI applications where multiple UI components need to reflect the same underlying data state, ensuring consistency and reducing the likelihood of bugs related to stale or inconsistent UI states.

-------------