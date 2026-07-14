class EngineException(Exception):

    """
    
    Base engine exception.
    
    """

    pass


class EngineConfigurationError(EngineException):

    """
    
    Raised when the engine is assembled with an invalid configuration.
    
    """

    pass


class DuplicateToolError(EngineException):

    """
    
    Raised when a tool name is registered more than once.
    
    """

    pass


class ToolNotFoundError(EngineException):

    """
    
    Raised when a requested tool is not present in the registry.
    
    """

    pass


class ToolExecutionError(EngineException):

    """
    
    Raised when a tool fails or times out while executing.
    
    """

    pass


class ReasoningError(EngineException):

    """
    
    Raised when the reasoner fails to produce a valid action.
    
    """

    pass


class StepLimitExceededError(EngineException):

    """
    
    Raised when a run consumes its step budget while halting is enforced.
    
    """

    pass
