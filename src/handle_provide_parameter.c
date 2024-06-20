#include "plugin.h"


static void handle_transfer(tronPluginProvideParameter_t *msg, context_t *context) {
    switch (context->next_param) {
        case TO_ADDRESS:
            copy_address(context->token_received, msg->parameter, sizeof(context->token_received));
            context->next_param = AMOUNT_UINT256;
            break;
        case AMOUNT_UINT256:
            copy_parameter(context->amount_in, msg->parameter, sizeof(context->amount_in));
            context->next_param = UNEXPECTED_PARAMETER;
            break;
        // Keep this
        default:
            PRINTF("Param not supported: %d\n", context->next_param);
            msg->result = TRON_PLUGIN_RESULT_ERROR;
            break;
    }
}

static void handle_swap_exact_tokens_for_tokens(tronPluginProvideParameter_t *msg, context_t *context)
{
    if (context->go_to_offset)
    {
        if (msg->parameterOffset != context->offset + SELECTOR_SIZE)
        {
            return;
        }
        context->go_to_offset = false;
    }

    switch (context->next_param)
    {
    case AMOUNT_IN: // amountIn_uint256
        copy_parameter(context->amount_in,
                       msg->parameter,
                       sizeof(context->amount_in));
        context->next_param = AMOUNT_OUT_MIN;
        break;
    case AMOUNT_OUT_MIN: // amountOutMin_uint256
        copy_parameter(context->amount_out,
                       msg->parameter,
                       sizeof(context->amount_out));
        context->next_param = PATH_OFFSET;
        break;
    case PATH_OFFSET: // path
        context->offset = U2BE(msg->parameter, PARAMETER_LENGTH - 2);
        context->next_param = TO_ADDRESS;
        break;
    case TO_ADDRESS: // to
        copy_address(context->to_address, msg->parameter, sizeof(context->to_address));
        context->next_param = PATH_LENGTH;
        context->go_to_offset = true;
        break;
    case PATH_LENGTH:
        context->offset = msg->parameterOffset - SELECTOR_SIZE + PARAMETER_LENGTH;
        context->go_to_offset = true;
        context->next_param = TOKEN_RECEIVED;
        break;
    case TOKEN_RECEIVED: // path[1] -> contract address of token received
        copy_address(context->token_received, msg->parameter, sizeof(context->token_received));
        context->next_param = UNEXPECTED_PARAMETER;
        break;
    // Keep this
    default:
        PRINTF("Param not supported: %d\n", context->next_param);
        msg->result = TRON_PLUGIN_RESULT_ERROR;
        break;
    }
}

    void handle_provide_parameter(tronPluginProvideParameter_t * msg)
    {
        context_t *context = (context_t *)msg->pluginContext;
        // We use `%.*H`: it's a utility function to print bytes. You first give
        // the number of bytes you wish to print (in this case, `PARAMETER_LENGTH`) and then
        // the address (here `msg->parameter`).
        PRINTF("plugin provide parameter: offset %d\nBytes: %.*H\n",
               msg->parameterOffset,
               PARAMETER_LENGTH,
               msg->parameter);

        msg->result = TRON_PLUGIN_RESULT_OK;

        // EDIT THIS: adapt the cases and the names of the functions.
        switch (context->selectorIndex)
        {
        case TRANSFER:
            handle_transfer(msg, context);
            break;
        case SWAP_EXACT_TOKENS_FOR_TOKENS:
            handle_swap_exact_tokens_for_tokens(msg, context);
            break;
        default:
            PRINTF("Selector Index not supported: %d\n", context->selectorIndex);
            msg->result = TRON_PLUGIN_RESULT_ERROR;
            break;
    }
}
