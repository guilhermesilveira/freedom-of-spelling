from freedom import freedom_search, English
from spaces import space_optimized

freedom_search(English(),
               space=space_optimized,
               generate_rules_only=True)
