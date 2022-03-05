export function prepareErrors(errors_field) {
  return < > {
      errors_field?.map((err) => < > {
          err
        } < br / > < />)}</ > ;
      }

      export function prepareErrorPayload(response, generic_error_message) {
        return response?.data ?? {
          "message": generic_error_message
        };
      }

      export function alertFormErrors(payload, setErrors) {
        setErrors(payload.errors ?? {})
      }

      export function alertGenericErrors(payload, snackBar) {
        if (payload?.message !== undefined){
          snackBar.enqueueSnackbar(payload?.message, {
            variant: "error"
          });
        }
      }
