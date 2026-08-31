import os 
from dotenv import load_dotenv

load_dotenv('API.env')

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# API Configuration
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Greek Stop Words for Keyword Extraction
GREEK_STOP_WORDS = {
    # 1. Articles & Prepositions
    "και", "κι", "ή", "το", "τα", "τη", "την", "της", "των", "του", "τους",
    "στο", "στη", "στην", "στους", "στις", "στα", "από", "για", "με", "σε",
    "που", "πως", "ότι", "ως", "προς", "κατά", "μετά", "διότι", "εάν", "αν", 
    "τις", "τους", "οι", "ο", "η", "ένας", "μία", "μια", "ένα", "ενός", "μιας",

    # 2. Negations & Logical Connectives
    "δεν", "μην", "μη", "ουτε", "αλλά", "όμως", "επίσης",

    # 3. Common User Intent Verbs ("I want", "tell me", "is happening")
    "θέλω", "θελω", "μάθω", "μαθω", "μάθουμε", "γίνεται", "γινεται", "γίνουν",
    "ξέρω", "ξερω", "πες", "βρες", "δείξε", "δειξε", "έχω", "εχω", "έχει",
    "είναι", "ειναι", "ήταν", "ηταν", "θα", "να", "κάνω", "κανω", "ειπες",

    # 4. Question & Filler Words
    "τι", "ποιος", "ποια", "ποιο", "ποιοι", "ποιες", "πού", "που", "πότε",
    "ποτέ", "πώς", "πως", "γιατί", "γιατι", "πόσο", "ποσο",

    # 5. Pronouns & Demonstratives
    "αυτό", "αυτη", "αυτή", "αυτά", "αυτα", "αυτός", "αυτος", "εγώ", "εγω",
    "εσύ", "εσυ", "εμείς", "εμεις", "εσείς", "εσεις", "μου", "σου", "του",
    "της", "μας", "σας", "τους", "όλα", "ολα", "κάτι", "κατι"
}

# Source Categories / Leanings for Distribution Calculation
MEDIA_BIAS_MAP = {
    # Left / Center-Left
    "efsyn.gr": "Left / Center-Left",
    "efimerida ton syntakton": "Left / Center-Left",
    "avgi.gr": "Left",
    "rizospastis.gr": "Far-Left",
    
    # Center / Public
    "in.gr": "Center",
    "ert.gr": "State / Center",
    "ertnews.gr": "State / Center",
    "tovima.gr": "Center / Center-Left",
    "naftemporiki.gr": "Center (Financial)",
    "amna.gr": "State News Agency",
    
    # Center-Right / Right
    "kathimerini.gr": "Center-Right",
    "ekathimerini.com": "Center-Right",
    "protothema.gr": "Center-Right",
    "iefimerida.gr": "Center-Right",
    "skai.gr": "Center-Right",
    "eleftherostypos.gr": "Center-Right",
    "pronews.gr": "Right-wing / Alternative",
    
    # Blogs & Platforms
    "blogspot.com": "Independent Blog (Varies)"
}