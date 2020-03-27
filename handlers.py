import coronaapi

def parse_api_data(data, status):
    try:
        final = ""
        for i in data:
            final = "[{date}] : {val} {status}.\n".format(date=i["Date"].split('T')[0], val=i["Cases"], status=status)
        return final
    except:
        return "Error: Could not parse API data."

def parse_summary(data):
    try:
        final = ""
        for i in data["Countries"]:
            if(i["Country"]):
                final += "{country} --> {confirmed} confirmed, {recovered} recovered, {deaths} deaths.\n".format(country=i["Country"], confirmed=i["TotalConfirmed"], recovered=i["TotalRecovered"], deaths=i["TotalDeaths"])
        return final
    except KeyError as e:
        print(e)
        return "Error: Could not parse API data."

def send_message_chunked(update, context, message):
    msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
    for text in msgs:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def assert_args_and_send(update, context, message, target_args=0):
    if(len(context.args) != target_args):
        send_message_chunked(update, context, "Error: Refer to /help.")
        return False
    send_message_chunked(update, context, message)

def start_handler(update, context):
    START_MSG = "Welcome to CoronaBot!\nType /help for info."

    assert_args_and_send(update, context, START_MSG)

def help_handler(update, context):
    HELP_MSG = """Request info using the following queries:
    /summary - Fetch a stat summary.
    /countries - Fetch a list of countries. Use the country as seen in this response for the following queries.
    /stats COUNTRYHERE - Returns a list of all statistics for country COUNTRYHERE.
    /confirmed COUNTRYHERE - Returns a list of confirmed cases for country COUNTRYHERE.
    /recovered COUNTRYHERE - Returns a list of recovered cases for country COUNTRYHERE.
    /deaths COUNTRYHERE - Returns a list of deaths for country COUNTRYHERE."""

    assert_args_and_send(update, context, HELP_MSG)

def countries_handler(update, context):
    assert_args_and_send(update, context, coronaapi.fetch_countries())

def summary_handler(update, context):
    assert_args_and_send(update, context, parse_summary(coronaapi.fetch_summary()))

def confirmed_handler(update, context):
    assert_args_and_send(update, context, parse_api_data(coronaapi.fetch_confirmed(context.args[0].lower()), "confirmed"), target_args=1)

def recovered_handler(update, context):
    assert_args_and_send(update, context, parse_api_data(coronaapi.fetch_recovered(context.args[0].lower()), "recovered"), target_args=1)

def deaths_handler(update, context):
    assert_args_and_send(update, context, parse_api_data(coronaapi.fetch_deaths(context.args[0].lower()), "deaths"),target_args=1)

def stats_handler(update, context):
    confirmed_handler(update, context)
    recovered_handler(update, context)
    deaths_handler(update, context)