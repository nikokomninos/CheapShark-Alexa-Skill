# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CheapSharkIntentHandler(AbstractRequestHandler):
    """
    Handler for CheapShark Intent.
    Presents the user with the top five game deals based 
    on deal rating, as returned by the CheapShark API.
    """
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CheapSharkIntent")(handler_input)
        
    def handle(self, handler_input):
        deals = self.getDeals()
        speak_output = "Here are the top five best current Steam game deals based on deal rating: "
        
        for deal in deals[:5]:
            speak_output += deal['title'] + " is currently " + deal['savings'] + "% off for a price of $" + deal['salePrice'] + ". "
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )
        
    def getDeals(self):
        """Retrieve deals from CheapShark using API
        
        Returns:
            sorted_deals: A dictionary of deals sorted by the deal's rating
        """
        
        #API communication
        response = requests.get("https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15")
        deals = response.json()
        
        #Round deal percent to nearest whole number
        for deal in deals:
            deal['savings'] = str(round(float(deal['savings'])))
            
        #Sort deals by deal rating
        sorted_deals = sorted(deals, key=lambda x: x['dealRating'], reverse=True)
    
        return sorted_deals
        
class CheapSharkPercentFilterIntentHandler(AbstractRequestHandler):
    """
    Handler for CheapShark Percent Filter Intent.
    Presents the user with five deals whose savings are
    above a user inputted percent off. If there are less than
    five, present the user with all deals that match the
    inputted percent off.
    """
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CheapSharkPercentFilterIntent")(handler_input)
        
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        salePercent = int(slots['salePercent'].value)
        deals = self.getDeals(salePercent)
        speak_output = ""
        
        #Handles case in which there are not enough deals to show
        if len(deals) >= 5:
            speak_output = f"Here are five Steam game deals above {salePercent}%: "
            for deal in deals[:5]:
                speak_output += deal['title'] + " is currently " + deal['savings'] + "% off for a price of $" + deal['salePrice'] + ". "
        else:
            speak_output = f"Here are all Steam game deals above {salePercent}%: "
            for deal in deals:
                speak_output += deal['title'] + " is currently " + deal['savings'] + "% off for a price of $" + deal['salePrice'] + ". "   
          
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )
        
    def getDeals(self, salePercent):
        """Retrieve deals from CheapShark using API
        
        Returns:
            sorted_deals: A dictionary of deals sorted by the deal's savings
        """
        
        #API communication
        response = requests.get("https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15")
        deals = response.json()  
        
        #Round deal percent to nearest whole number
        for deal in deals:
            deal['savings'] = str(round(float(deal['savings'])))
        
        #Filters deals dictionary to only contain deals above
        #a user-indicated percent
        filtered_deals = [
            deal for deal in deals if int(deal['savings']) >= salePercent
        ]
            
        #Sorts deals by percent off
        sorted_deals = sorted(filtered_deals, key=lambda x: x['savings'], reverse=True)
    
        return sorted_deals
        
class CheapSharkScoreFilterIntentHandler(AbstractRequestHandler):
    """
    Handler for CheapShark Score Filter Intent.
    Presents the user with the top five game deals based 
    on Metacritic rating, as returned by the CheapShark API.
    """
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CheapSharkScoreFilterIntent")(handler_input)
        
    def handle(self, handler_input):
        deals = self.getDeals()
        speak_output = "Here are the top five best current Steam game deals based on Metacritic score: "
        
        for deal in deals[:5]:
            speak_output += deal['title'] + " has a Metacritic score of " + deal['metacriticScore'] + " and is currently " + deal['savings'] + "% off for a price of $" + deal['salePrice'] + ". "
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )
        
    def getDeals(self):
        """Retrieve deals from CheapShark using API
        
        Returns:
            sorted_deals: A dictionary of deals sorted by the deal's Metacritic score
        """
        
        #API communication
        response = requests.get("https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15")
        deals = response.json()
        
        #Round deal percent to nearest whole number
        for deal in deals:
            deal['savings'] = str(round(float(deal['savings'])))
            
        #Sort deals by deal rating
        sorted_deals = sorted(deals, key=lambda x: x['metacriticScore'], reverse=True)
    
        return sorted_deals        
        
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = """Welcome, this skill returns deals for video games on the Steam marketplace. 
        You can say anything that has to do with deals for: cheap shark, steam, pc games, etc."""

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(CheapSharkIntentHandler())
sb.add_request_handler(CheapSharkPercentFilterIntentHandler())
sb.add_request_handler(CheapSharkScoreFilterIntentHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()