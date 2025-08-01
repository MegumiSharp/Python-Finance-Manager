"""Expensia Application Settings - Centralized configuration"""
from pathlib import Path

# ============================================================================
# PATHS AND DIRECTORIES
# ============================================================================

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
SRC_ROOT = PROJECT_ROOT / "src"
CONFIG_ROOT = PROJECT_ROOT / "config"
ASSETS_ROOT = PROJECT_ROOT / "assets"
DATA_ROOT = PROJECT_ROOT / "data"

# Specific paths
THEMES_PATH = ASSETS_ROOT / "themes"
BACKGROUND_PATH = ASSETS_ROOT / "images" / "backgrounds"
ICONS_PATH = ASSETS_ROOT / "images" / "icons"
DATABASE_PATH = DATA_ROOT / "database" / "transactions.db"
USER_SETTINGS_PATH = DATA_ROOT / "user_settings" / "user_settings.json"


# Files Names
BACKGROUND_FILE_NAME = "background.jpg"


# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

APP_NAME = "Expensia"
APP_VERSION = "0.0.1"
APP_DESCRIPTION = "Personal Finance Tracker with Budget Rules"

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# ============================================================================
# THEME SETTINGS
# ============================================================================

THEMES_TYPE = {
    "NightTrain" : "NightTrain.json",
    "Default" : "Default.json",
    "Orange" : "Orange.json",
    "SweetKind" : "Sweetkind.json",
}

DEFAULT_THEME = "Default"
DEFAULT_APPEARANCE_MODE = "dark"
    

# Default budget rule percentages (50/30/20 rule)
DEFAULT_BUDGET_NEEDS = 50
DEFAULT_BUDGET_WANTS = 30  
DEFAULT_BUDGET_SAVINGS = 20

# Validation ranges for budget percentages
BUDGET_PERCENTAGE_MIN = 1
BUDGET_PERCENTAGE_MAX = 99

# ============================================================================
# CURRENCY SETTINGS
# ============================================================================

AVAILABLE_CURRENCIES = ["€", "$", "£"]

# ============================================================================
# DATABASE SETTINGS
# ============================================================================

# SQLite database configuration
DB_TIMEOUT = 30.0  # seconds
DB_CHECK_SAME_THREAD = False

# Table names
TRANSACTIONS_TABLE = "transactions"
BUDGET_RULES_TABLE = "budget_rules"
SETTINGS_TABLE = "user_settings"

# ============================================================================
# UI SETTINGS
# ============================================================================

# Colors
COLOR_EXPENSE = "#ff6b6b"  # Red for expenses
COLOR_INCOME = "#51cf66"   # Green for income
COLOR_ERROR = "#D61A3C"    # Error messages

# Fonts
DEFAULT_FONT_SIZE = 14
HEADER_FONT_SIZE = 16
TITLE_FONT_SIZE = 20

# Table settings
DEFAULT_ROWS_PER_PAGE = 30
MAX_DESCRIPTION_LENGTH = 100

# ============================================================================
# VALIDATION SETTINGS
# ============================================================================

# Transaction validation
MAX_AMOUNT = 999999.99
MIN_AMOUNT = -999999.99
MAX_DESCRIPTION_LENGTH = 100  # Maximum length for transaction descriptions
MAX_TAG_LENGTH = 15           # Maximum length for tags

# Date format
DATE_FORMAT = "%d-%m-%Y" # Example: 31-12-2025

# ============================================================================
# FILE SETTINGS
# ============================================================================

# Allowed file extensions for imports
ALLOWED_CSV_EXTENSIONS = ['.csv']
ALLOWED_JSON_EXTENSIONS = ['.json']

# ============================================================================
# DEFAULT USER SETTINGS
# ============================================================================

# Writing keys as a costants prevents typos and makes it easier to manage
KEY_IS_FIRST_TIME = "is_first_time"
KEY_NICKNAME = "nickname"
KEY_CURRENCY_SIGN = "currency_sign"
KEY_THEME = "theme"
KEY_BUDGET_NEEDS = "budget_rule_needs"
KEY_BUDGET_WANTS = "budget_rule_wants"
KEY_BUDGET_SAVING = "budget_rule_saving"

VALUE_TRUE = "true"
VALUE_FALSE = "false"

DEFAULT_NICKNAME = "User"
DEFAULT_CURRENCY = "€"

# Default user settings
DEFAULT_USER_SETTINGS = {
    KEY_IS_FIRST_TIME: VALUE_TRUE,
    KEY_NICKNAME: DEFAULT_NICKNAME,
    KEY_CURRENCY_SIGN: DEFAULT_CURRENCY,
    KEY_THEME: DEFAULT_THEME,
    KEY_BUDGET_NEEDS: DEFAULT_BUDGET_NEEDS,
    KEY_BUDGET_WANTS: DEFAULT_BUDGET_WANTS,
    KEY_BUDGET_SAVING: DEFAULT_BUDGET_SAVINGS,
}

# ============================================================================
# FRAMES AND VIEWS COSTANTS
# ============================================================================

WELCOME_FRAME = "welcome_frame"
NAVIGATION_FRAME = "navigation_frame"
DASHBOARD_FRAME = "dashboard_frame"

# ============================================================================
# END OF SETTINGS