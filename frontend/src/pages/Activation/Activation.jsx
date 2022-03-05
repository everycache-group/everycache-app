import React, {
  useEffect
} from "react";
import {
  Redirect
} from "react-router";
import {
  useSelector,
  useDispatch
} from "react-redux";
import {
  useSnackbar
} from "notistack";
import {
  alertGenericErrors,
} from "../../services/errorMessagesService"

import {
  activateUser, getUser
} from "../../redux/slices/userSlice"

function ActivationPage({
  match
}) {
  const dispatch = useDispatch();
  const snackBar = useSnackbar();
  const userId = useSelector((state) => state.user.id);

  useEffect(() => {
    const activation_token = match?.params?.token;
    if (activation_token) {
      dispatch(activateUser(activation_token))
        .unwrap()
        .then(() => {
          snackBar.enqueueSnackbar("User activated successfully.", {
            variant: "success"
          });
          if (userId){
            dispatch(getUser(userId));
          }
        })
        .catch((payload) => {
          alertGenericErrors(payload, snackBar);
        });
    }
  });


  return <Redirect to = "/" / > ;
}

export default ActivationPage;
