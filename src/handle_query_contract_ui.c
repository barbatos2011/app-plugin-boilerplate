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

    return amountToString(context->amount_received,
                         sizeof(context->amount_received),
                         decimals,
                         ticker,
                         msg->msg,
                         msg->msgLength);
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
    msg->result = ret ? TRON_PLUGIN_RESULT_OK : TRON_PLUGIN_RESULT_ERROR;
}
