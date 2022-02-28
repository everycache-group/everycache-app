import React, { useState } from "react";
import * as Style from "./style";
import TextField from "@mui/material/TextField";
import LoadingButton from "@mui/lab/LoadingButton";
import useForm from "../../../hooks/useForm";
import { loginUser } from "./../../../redux/slices/authSlice";
import { getUser } from "./../../../redux/slices/userSlice";
import { useDispatch, useSelector } from "react-redux";
import { useSnackbar } from "notistack";
import { alertGenericErrors, prepareErrors } from "../../../services/errorMessagesService"

function Login() {
  const [registering, setRegistering] = useState(false);

  const dispatch = useDispatch();
  const snackBar = useSnackbar();

  const { handleFormSubmit, handleUserInput, formValues, errors } = useForm(
    {
      email: "",
      password: "",
    },
    () => {
      const { email, password } = formValues;
      dispatch(loginUser({ email, password }))
        .unwrap()
        .then((result) => {
          const {userId} = result;
          dispatch(getUser(userId))
            .unwrap()
            .then((result) => {})
            .catch((payload) => {
              alertGenericErrors(payload, snackBar);
            });
        })
        .catch((payload) => {
          alertGenericErrors(payload, snackBar);
        });
    }
  );

  return (
    <Style.LoginForm>
      <TextField
        size="small"
        id="email"
        error={!!errors.email}
        helperText={prepareErrors(errors.email)}
        onChange={handleUserInput}
        type="email"
        name="email"
        label="Email"
      />
      <TextField
        size="small"
        id="password"
        error={!!errors.password}
        helperText={prepareErrors(errors.password)}
        onChange={handleUserInput}
        type="password"
        name="password"
        label="Password"
      />

      <LoadingButton
        onClick={handleFormSubmit}
        loading={registering}
        variant="contained"
        color="success"
        type="submit"
      >
        Log in
      </LoadingButton>
    </Style.LoginForm>
  );
}

export default Login;
