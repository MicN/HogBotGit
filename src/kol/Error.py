__i = 0
LOGIN_FAILED_GENERIC = __i; __i += 1
LOGIN_FAILED_BAD_PASSWORD = __i; __i += 1
NIGHTLY_MAINTENANCE = __i; __i += 1
NOT_LOGGED_IN = __i; __i += 1
REQUEST_GENERIC = __i; __i += 1
REQUEST_FATAL = __i; __i += 1
INVALID_ACTION = __i; __i += 1
INVALID_LOCATION = __i; __i += 1
ITEM_NOT_FOUND = __i; __i += 1
SKILL_NOT_FOUND = __i; __i += 1
EFFECT_NOT_FOUND = __i; __i += 1
RECIPE_NOT_FOUND = __i; __i += 1
WRONG_KIND_OF_ITEM = __i; __i += 1
USER_IN_HARDCORE_RONIN = __i; __i += 1
USER_IS_IGNORING = __i; __i += 1
USER_IS_DRUNK = __i; __i += 1
USER_IS_FULL = __i; __i += 1
USER_IS_LOW_LEVEL = __i; __i += 1
NOT_ENOUGH_ADVENTURES = __i; __i += 1
NOT_ENOUGH_MEAT = __i; __i += 1
LIMIT_REACHED = __i; __i += 1
ALREADY_COMPLETED = __i; __i += 1
BOT_REQUEST = __i; __i += 1

class Error(Exception):
    "Base class for KoL Exceptions."
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

################
# Login Errors #
################
class LoginError(Error):
    "A generic exception raised during login."
    def __init__(self, message, timeToWait=60):
        self.message = message
        self.timeToWait = timeToWait

class IncorrectPasswordError(Error):
    "An exception raised when a user tries to login with a bad password."
    def __init__(self, message):
        self.message = message

class NightlyMaintenanceError(Error):
    "An exception raised when Nightly Maintenance is occurring."
    def __init__(self, message):
        self.message = message

class NotLoggedInError(Error):
    "An exception raised if the session thinks it is logged in when in reality it isn't."
    def __init__(self, message):
        self.message = message

##################
# Generic Errors #
##################
class RequestError(Error):
    "An exception raised during requests."
    def __init__(self, message):
        self.message = message

###################
# Database Errors #
###################
class ItemNotFoundError(Error):
    "An exception raised when an item can not be found in the item database."
    def __init__(self, message):
        self.message = message

class SkillNotFoundError(Error):
    "An exception raised when a skill could not be found."
    def __init__(self, message):
        self.message = message

##############
# Bot Errors #
##############
class ParseMessageError(Error):
    "An exception used by bots raised when a kmail message can not be understood correctly."

#######################
# Item-Related Errors #
#######################
class NotEnoughItemsError(Error):
    "An exception raised when the user tries to perform an action on an item they don't have enough of."
    def __init__(self, message):
        self.message = message

class UnableToPulverizeItemError(Error):
    "An exception raised when a user tried to pulverize an item that can not be pulverized."
    def __init__(self, message):
        self.message = message

class NotEnoughHermitPermitsError(Error):
    "An exception raised when a user tries to barter without enough Hermit Permits"
    def __init__(self, message):
        self.message = message

class NotSoldHereError(Error):
    "An exception raised when a user tries to buy/barter something that isn't available there"
    def __init__(self, message):
        self.message = message

#######################
# User-Related Errors #
#######################
class UserInHardcoreRoninError(Error):
    """
    An exception raised when an action can not be performed because either the current user or
    the target user is in hardcore or ronin.
    """
    def __init__(self, message):
        self.message = message

class UserIsIgnoringError(Error):
    "An exception raised when the target user is ignoring the current user."
    def __init__(self, message):
        self.message = message

######################
# Adventuring Errors #
######################
class UserShouldNotBeHereError(Error):
    "An exception raised when a user tries to adventure in a location where they should not be, yet."

class TooDrunkError(Error):
    "An exception raised when a user attempts to do something they are too drunk to do."

class TooFullError(Error):
    "An exception raised when a user attempts to eat food they do not have room for."

#################
# Effect Errors #
#################
class DontHaveEffectError(Error):
    "An exception raised when the user doesn't have a particular effect."
    def __init__(self, message):
        self.message = message

###############
# Misc Errors #
###############
class InvalidActionError(Error):
    "An exception raised when the user tries to perform an invalid action."
    def __init__(self, message):
        self.message = message

class InvalidRecipeError(Error):
    "An exception raised when the user tries to construct something using an invalid recipe."
    def __init__(self, message):
        self.message = message

class SkillMissingError(Error):
    "An exception raised when the user fails to perform an action because they are missing a skill."
    def __init__(self, message):
        self.message = message

class NotEnoughAdventuresLeftError(Error):
    """
    An exception raised then the user attempts to perform an action and they don't have enough
    adventures left to complete it.
    """
    def __init__(self, message):
        self.message = message

class NotEnoughMeatError(Error):
    """
    An exception raised when the user tries to do something without enought meat
    on hand to successfully perform the action.
    """
    def __init__(self, message):
        self.message = message

class NotAStoreError(Error):
    """
    An exception raised when the user tries to visit a store that doesn't exist
    """
    def __init__(self, message):
        self.message = message
        
class MallLimitError(Error):
    """
    An exception raised when the user tries to purchase an item in a mall store and hits the limit.
    """
    def __init__(self, message):
        self.message = message

class InvalidMonsterError(Error):
    def __init__(self, message):
        self.message = message    
            
class InvalidClanError(Error):
    def __init__(self, message):
        self.message = message        

