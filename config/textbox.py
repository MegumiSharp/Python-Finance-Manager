WELCOME_HEADER_TEXT = "Welcome in Expensia!"

INPUT_GUIDELINE_TEXT = "Input Guidelines"

WELCOME_TEXT = (
            "Your smart companion for tracking transactions and managing your finances.\n\n"
            "In this setup panel, you can:\n"
            "- Customize your currency symbol\n"
            "- Set your account name\n"
            "- Adjust your budget rule values to match your financial goals\n\n"
            "Take a moment to configure everything just the way you like.\n\n"
            "When you're ready, click Continue to get started!"
        )

BUDGET_RULE_INFO_TEXT= """
A smart way to help you track your expenses — Budget Rule

What is a Budget Rule? A Budget Rule helps you organize your spending by dividing your transactions into 3 simple labels:

1. Needs – Essentials like rent, food, and bills
2. Wants – Non-essentials like eating out or games
3. Savings – Money you set aside for the future or to pay off debt (calculated automatically)

You choose how much of your total income goes into each label. 50% for Needs, 30% for Wants, 20% for Savings

This is how it works:

• In the tag menu you can choose which tags are considered Wants and which are Needs. The Savings label is calculated by default based on what's left. 
• When you use the special built-in tag "Income", the app will divide that amount using your chosen percentages and apply it to your Budget Rule.
• By clicking Budget Rule in the sidebar, a dedicated tab opens where you can see how much you've spent in each label and when.

The app compares your spending with your rules and alerts you if you're going over in any area. 
You can stick to the classic 50/30/20 split or adjust the percentages to match your lifestyle.
        """

INPUT_GUIDE_TEXT = """
Before clicking continue, write a nickname to use in the welcome page, and chose your currency sign for the amount. 

If  no value are insered inside the needs wants saving field,  default value will be used, 50/30/20.

Valid Input Examples:
• Enter whole numbers only (1-99)
• Do not include the % symbol
• All three values must add up to 100"""

ERROR_VAL_RANGE_TEXT = "Values must be between 1 and 99"
ERROR_VAL_SUM_INCORRECT_TEXT = "Values must add up to 100% \n (currently:"
ERROR_VAL_WHOLE_TEXT = "Values must be whole numbers only"


IMPORT_EXPORT_MESSAGE = (
    "Here you can import or export the database. Below is the tutorial:\n\n"
    "EXPORT:\n"
    "- When pressing 'Export', a CSV file will be created in the 'export' folder.\n\n"
    "IMPORT:\n"
    "- To import a database, place the file named 'db_import.csv' inside the 'import' folder.\n"
    "- The formatting of the file should always be:\n"
    "  date,amount,tag,desc\n"
    "  date,amount,tag,desc\n"
    "  date,amount,tag,desc\n\n"
    "RULES:\n"
    "- The date must be in the format YYYY-MM-DD.\n"
    "- The amount must not include any currency sign. Use '-' for negative values only.\n"
    "- Each row in the CSV represents a row in the database.\n\n"
    "BACKUP:\n"
    "- The 'Backup' button creates a copy of the current database in the 'backup' folder.\n"
    "- The 'Revert Backup' button restores the database from the backup.\n"
    "- If there are any problems with CSV importing, you can use the 'Revert Backup' button."
)
