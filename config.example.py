TOKEN = "nuh uh you dont get to see my token"

BOT_PREFIX = "."

IMPOSSIBLE_GAMES = False

CAT_API_KEY = "you dont get to"
DOG_API_KEY = "see my api keys either"
GENAI_API_KEY = "why are you still looking for keys jesus"

FACTS_ROUTE = "https://uselessfacts.jsph.pl/api/v2/facts/random"
CATS_ROUTE = "https://api.thecatapi.com/v1/images/search"
DOGS_ROUTE = "https://api.thedogapi.com/v1/images/search"
MEMES_ROUTE = "https://meme-api.com/gimme"
TRUTH_ROUTE = "https://api.truthordarebot.xyz/v1/truth"
DARE_ROUTE = "https://api.truthordarebot.xyz/api/dare"
WOULD_YOU_RATHER_ROUTE = "https://api.truthordarebot.xyz/api/wyr"
NEVER_HAVE_I_EVER_ROUTE = "https://api.truthordarebot.xyz/api/nhie"


def nsfw_route(category: str, content_type: str) -> str:
    return f"https://purrbot.site/api/img/nsfw/{category}/{content_type}"
