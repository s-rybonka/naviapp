from rest_framework.views import exception_handler


def default_exception_handler(exc, context):
    response = exception_handler(exc, context)
    use_default_error_keys = ['non_field_errors', 'status_code']

    if response is not None:
        customized_response = {}
        default_error_detail = response.data.pop('detail', {})
        non_field_errors = response.data.pop('non_field_errors', {})

        if non_field_errors:
            customized_response['non_field_errors'] = non_field_errors

        else:
            if default_error_detail:
                customized_response['detail'] = default_error_detail

            else:
                fields_errors = response.data.items()

                if fields_errors:
                    customized_response['field_errors'] = {}

                    for key, value in fields_errors:
                        if key not in use_default_error_keys and value:
                            customized_response['field_errors'][key] = value

        response.data = customized_response

    return response
