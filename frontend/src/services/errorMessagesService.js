
export function prepareErrors(errors_field) {
    return <>{errors_field?.map((err) => <>{err}<br/></>)}</>;
}

export function prepareErrorPayload(response, generic_error_message) {
  return response?.data ?? {"message": [generic_error_message]};
}

export function alertFormErrors(payload, setErrors) {
  setErrors(payload.errors ?? {})
}

export function alertGenericErrors(payload, snackBar) {
    const genericErrorMessages = payload?.message;
    if (genericErrorMessages){
      for(const msg of genericErrorMessages) {
        snackBar.enqueueSnackbar(msg, {variant: "error"});
      }
    }
}
