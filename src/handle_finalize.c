#include "plugin.h"

void handle_finalize(tronPluginFinalize_t *msg) {
    context_t *context = (context_t *) msg->pluginContext;
    msg->uiType = TRON_UI_TYPE_GENERIC;

    switch (context->selectorIndex) {
        case TRANSFER:
            msg->numScreens = 2;
            break;
        default:
            PRINTF("Selector Index not supported: %d\n", context->selectorIndex);
            msg->result = TRON_PLUGIN_RESULT_ERROR;
            break;
    }

    msg->result = TRON_PLUGIN_RESULT_OK;
}
