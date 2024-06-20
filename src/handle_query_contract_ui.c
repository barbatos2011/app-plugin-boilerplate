#include "plugin.h"

// EDIT THIS: Adapt / remove this function to your needs.
static bool set_transfer_ui(tronQueryContractUI_t *msg, context_t *context) {
    strlcpy(msg->title, "Transfer To", msg->titleLength);
    context->token_received[0] = ADD_PRE_FIX_BYTE_MAINNET;
    getBase58FromAddress(context->token_received, msg->msg, false);
    return true;
}

// Set UI for "Receive" screen.
// EDIT THIS: Adapt / remove this function to your needs.
static bool set_amount_ui(tronQueryContractUI_t *msg, const context_t *context) {
    strlcpy(msg->title, "Amount", msg->titleLength);

    uint8_t decimals = 0;
    const char *ticker = "TRX";

    return amountToString(context->amount_in,
                         sizeof(context->amount_in),
                         decimals,
                         ticker,
                         msg->msg,
                         msg->msgLength);
}

static bool set_amount_in_ui(tronQueryContractUI_t *msg, const context_t *context)
{
    strlcpy(msg->title, "Amount In", msg->titleLength);

    uint8_t decimals = 18;
    const char *ticker = context->ticker;

    // If the token look up failed, use the default network ticker along with the default decimals.
    if (!context->token_found)
    {
        decimals = 18;
        ticker = msg->network_ticker;
    }

    return amountToString(context->amount_in,
                          sizeof(context->amount_in),
                          decimals,
                          ticker,
                          msg->msg,
                          msg->msgLength);
}

static bool set_to_address_ui(tronQueryContractUI_t *msg, context_t *context)
{
    strlcpy(msg->title, "Address To", msg->titleLength);
    context->to_address[0] = ADD_PRE_FIX_BYTE_MAINNET;
    getBase58FromAddress(context->to_address, msg->msg, false);
    return true;
}

static bool set_amount_out_ui(tronQueryContractUI_t *msg, const context_t *context)
{
    strlcpy(msg->title, "Amount Out", msg->titleLength);

    uint8_t decimals = 18;
    const char *ticker = context->ticker;

    // If the token look up failed, use the default network ticker along with the default decimals.
    if (!context->token_found)
    {
        decimals = 18;
        ticker = msg->network_ticker;
    }

    return amountToString(context->amount_out,
                          sizeof(context->amount_out),
                          decimals,
                          ticker,
                          msg->msg,
                          msg->msgLength);
}

static bool set_token_received_ui(tronQueryContractUI_t *msg, context_t *context)
{
    strlcpy(msg->title, "Token From", msg->titleLength);
    context->token_received[0] = ADD_PRE_FIX_BYTE_MAINNET;
    getBase58FromAddress(context->token_received, msg->msg, false);
    return true;
}

void handle_query_contract_ui(tronQueryContractUI_t *msg) {
    context_t *context = (context_t *) msg->pluginContext;
    bool ret = false;

    // msg->title is the upper line displayed on the device.
    // msg->msg is the lower line displayed on the device.

    // Clean the display fields.
    memset(msg->title, 0, msg->titleLength);
    memset(msg->msg, 0, msg->msgLength);

    if (context->selectorIndex == TRANSFER) {
        switch (msg->screenIndex) {
            case 0:
                ret = set_transfer_ui(msg, context);
                break;
            case 1:
                ret = set_amount_ui(msg, context);
                break;
            // Keep this
            default:
                PRINTF("Received an invalid screenIndex\n");
        }
    }
    else if (context->selectorIndex == SWAP_EXACT_TOKENS_FOR_TOKENS)
    {
        switch (msg->screenIndex)
        {
        case 0:
            ret = set_amount_in_ui(msg, context);
            break;
        case 1:
            ret = set_amount_out_ui(msg, context);
            break;
        case 2:
            ret = set_to_address_ui(msg, context);
            break;
        case 3:
            ret = set_token_received_ui(msg, context);
            break;
            // Keep this
        default:
            PRINTF("Received an invalid screenIndex\n");
        }
    }
    msg->result = ret ? TRON_PLUGIN_RESULT_OK : TRON_PLUGIN_RESULT_ERROR;
}
