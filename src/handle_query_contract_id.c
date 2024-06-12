#include "plugin.h"

// Sets the first screen to display.
void handle_query_contract_id(tronQueryContractID_t *msg) {
    const context_t *context = (const context_t *) msg->pluginContext;
    // msg->name will be the upper sentence displayed on the screen.
    // msg->version will be the lower sentence displayed on the screen.

    // For the first screen, display the plugin name.
    strlcpy(msg->name, APPNAME, msg->nameLength);

    // EDIT THIS: Adapt the cases by modifying the strings you pass to `strlcpy`.
    if (context->selectorIndex == TRANSFER) {
        strlcpy(msg->version, "Transfer", msg->versionLength);
        msg->result = TRON_PLUGIN_RESULT_OK;
    }  else {
        PRINTF("Selector index: %d not supported\n", context->selectorIndex);
        msg->result = TRON_PLUGIN_RESULT_ERROR;
    }
}
